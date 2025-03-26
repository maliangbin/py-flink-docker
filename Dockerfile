FROM  openjdk:11-jdk

# 安装 Flink
ENV FLINK_VERSION=1.20.1
ENV FLINK_HOME=/opt/flink
ENV PATH=$FLINK_HOME/bin:$PATH

WORKDIR /opt

RUN apt-get update && apt-get install -y wget

RUN wget https://www.apache.org/dyn/closer.lua/flink/flink-1.20.1/flink-1.20.1-bin-scala_2.12.tgz

RUN tar -zxvf flink-1.20.1-bin-scala_2.12.tgz \
    && rm -rf flink-1.20.1-bin-scala_2.12.tgz \
    && mv flink-1.20.1 flink

# 安装 Python 和 pip
RUN apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN pip install google-cloud-bigquery-storage

# #pip 镜像换成国内源
# RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 安装 apache-flink Python 包
RUN python -m pip install apache-flink==1.20.1

COPY ./opt/lib/flink-connector-kafka-3.4.0-1.20.jar /opt/flink/lib/flink-connector-kafka-3.4.0-1.20.jar
COPY ./opt/lib/kafka-clients-3.4.0.jar /opt/flink/lib/kafka-clients-3.4.0.jar

RUN export JAVA_OPTS="-Dcom.sun.management.jmxremote=false -XX:-UseContainerSupport"  # 添加 JAVAOPTS 环境变量

RUN export KAFKA_OPTS="-Dcom.sun.management.jmxremote=false -XX:-UseContainerSupport"