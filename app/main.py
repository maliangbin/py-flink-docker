from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from src.service.clean_service import CleanService
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink
from pyflink.datastream.connectors.kafka import (
    KafkaOffsetsInitializer,
    DeliveryGuarantee,
    KafkaRecordSerializationSchema,
)
from pyflink.common import WatermarkStrategy
from pyflink.common.configuration import Configuration
from pyflink.datastream.checkpoint_config import CheckpointingMode
from pyflink.datastream.connectors.kafka import KafkaOffsetResetStrategy
from pyflink.datastream.formats.json import JsonRowSerializationSchema


def data_etl(env: StreamExecutionEnvironment):
    # 创建消费者
    kafka_consumer = (
        KafkaSource.builder()
        .set_bootstrap_servers("kafka:9092")
        .set_topics("stat-topic")
        .set_group_id("flink-stat-local")
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())
        # .set_starting_offsets(
        #     KafkaOffsetsInitializer.committed_offsets(
        #         offset_reset_strategy=KafkaOffsetResetStrategy.EARLIEST,
        #     )
        # )
        .set_value_only_deserializer(SimpleStringSchema())
        .set_properties(
            {
                # 精确消费控制
                "enable.auto.commit": "false",  # 关闭自动提交（默认true），由checkpoint控制
                "isolation.level": "read_committed",  # 确保精确一次消费
                # 吞吐量优化
                "fetch.min.bytes": "65536",  # 每次拉取最小数据量（64KB）
                "fetch.max.bytes": "52428800",
                "max.poll.records": "500",  # 单次拉取最大记录数
                "max.partition.fetch.bytes": "1048576",
                # IO 优化
                "fetch.max.wait.ms": "500",  # 拉取等待超时时间
                "receive.buffer.bytes": "65536",  # Socket接收缓冲区64KB
                "send.buffer.bytes": "131072",  # Socket发送缓冲区128KB
                # 消费者组稳定性
                "session.timeout.ms": "45000",  # 会话超时
                "heartbeat.interval.ms": "3000",  # 心跳间隔（建议≤session.timeout.ms/3）
                "max.poll.interval.ms": "120000",  # 处理消息超时
            }
        )
        .build()
    )

    # 添加数据源
    ds = env.from_source(
        kafka_consumer, WatermarkStrategy.no_watermarks(), "Kafka Source"
    )

    # 数据清洗
    clean_service = CleanService()
    with_type_info = clean_service.get_type_info()
    ds = (
        ds.map(clean_service.clean)
        .filter(lambda x: x is not None)
        .map(clean_service.dict_to_row, output_type=with_type_info)
    )

    # 创建生产者
    kafka_producer = (
        KafkaSink.builder()
        .set_bootstrap_servers("kafka:9092")
        .set_delivery_guarantee(DeliveryGuarantee.AT_LEAST_ONCE)
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
            .set_topic("clean-topic")
            .set_value_serialization_schema(
                JsonRowSerializationSchema.builder()
                .with_type_info(with_type_info)
                .build()
            )
            .build()
        )
        .build()
    )

    ds.sink_to(kafka_producer)

    # 执行
    env.execute("Read from Kafka -> Clean -> Write to Kafka")


if __name__ == "__main__":
    # 创建流式环境
    env = StreamExecutionEnvironment.get_execution_environment()

    # 启用自适应调度器（关键配置）
    config = Configuration()
    config.set_string("jobmanager.scheduler", "adaptive")  # 启用自适应调度器
    config.set_integer("jobmanager.adaptive-scheduler.min-parallelism", 1)  # 最小并行度
    config.set_string(
        "jobmanager.adaptive-scheduler.resource-stabilization-timeout", "10s"
    )  # 资源稳定超时

    # 设置并行度
    env.set_parallelism(1)

    env.enable_checkpointing(5000)  # 启用检查点
    env.get_checkpoint_config().set_checkpointing_mode(CheckpointingMode.EXACTLY_ONCE)

    data_etl(env)
