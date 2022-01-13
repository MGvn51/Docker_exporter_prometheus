# Docker_exporter_prometheus

Docker runtime metrics exporter for Prometheus written in python

## Docker
For pre-built images check [docker hub]

### Docker-compose

### Docker cli
To create the container using the docker cli use the following command : 
```bash
docker run -d \
  --name=docker_exporter_prometheus \
  -e LOG_LEVEL=info `#optional` \
  -e CGROUP=cgropfs_v2 `#optional` \
  -e UPDATE_SECONDS=5 `#optional` \
  -e METRICS_PREFIX=docker_exporter `#optional` \
  -p 8080:11211 \
  -v /path/to/cgroup/memory/docker:/host_docker/memory \
  -v /path/to/cgroup/cpuacct/docker:/host_docker/cpuacct \
  -v /path/to/cgroup/blkio/docker:/host_docker/blkio \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --restart unless-stopped \
  MGvn51/docker_exporter_prometheus:0.1.0
```

### Build image
Clone the repository and run the command `docker build -t docker_exporter_prometheus:0.1.0 .` to create the image
```Docker
FROM python:3.8.10-slim

WORKDIR /python_app

RUN pip install --no-cache-dir docker
RUN pip install --no-cache-dir prometheus_client

COPY ./exporter/ /python_app/

CMD python3 exporter.py
```

## Setup
Deploy the container directly or build your own, environmet variables are available to customize the container.

## Parameters
Container images are configured using parameters passed at runtime.

| Parameter | Function |
| :---: | --- |
| `-e LOG_LEVEL=info` | [Logging level](https://docs.python.org/3/howto/logging.html#when-to-use-logging) |
| `-e CGROUP=cgroupfs_v2` | [cgroup type](https://docs.docker.com/config/containers/runmetrics/#find-the-cgroup-for-a-given-container) |
| `-e UPDATE_SECONDS=5` | Seconds between metrics updates |
| `-e METRICS_PREFIX=docker_exporter` | Prefix for the metrics |
| `-p 8080:11211` | Metrics port |

---
### Notes
Features marked with '\*' are not fully tested yet