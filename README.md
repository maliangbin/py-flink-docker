# py-flink-docker
py-flink-docker

1. flink version : 1.20.1
2. python version : 3.8
3. flink-connector-kafka version : flink-connector-kafka-3.4.0-1.20

## Build
```shell
docker build -t py-flink:latest .
```

## Run
```shell
docker run -it --rm --name py-flink-docker py-flink:latest -p 8081:8081 bash
```

## docker compose
```shell
docker-compose up
```