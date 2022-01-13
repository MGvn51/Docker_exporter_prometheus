# [Docker_exporter_prometheus](https://github.com/MGvn51/Docker_exporter_prometheus.git)

Docker runtime metrics exporter for Prometheus written in python 3.

## Docker
For pre-built images check [docker hub](https://hub.docker.com/r/mgvn51/docker_exporter_prometheus)

### Docker-compose\*
In order to use docker-compose copy the following code to a file called `docker-compose.yml` and run the command `docker-compose up`
```yml
version: "2.1"
services:
  docker-exporter:
  image: mgvn51/docker_exporter_prometheus:0.1.0
  container_name: docker_exporter_prometheus
  environment:
    - LOG_LEVEL=info
	- CGROUP=cgroupfs_v2
	- UPDATE_SECONDS=5
	- METRICS_PREFIX=docker_exporter
  volumes:
    - /path/to/cgroup/memory/docker:/host_docker/memory
	- /path/to/cgroup/cpuacct/docker:/host_docker/cpuacct
	- /path/to/cgroup/blkio/docker:/host_docker/blkio
	- /var/run/docker.sock:/var/run/docker.sock
  ports:
    - 8080:11211
  restart: unless-stopped
```

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
  mgvn51/docker_exporter_prometheus:0.1.0
```

### Build image
Clone the [repository](https://github.com/MGvn51/Docker_exporter_prometheus.git) and run the command `docker build -t docker_exporter_prometheus:0.1.0 .` to create the image
```dockerfile
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
|  `-v /path/to/cgroup/memory/docker:/host_docker/memory` | Path to the docker memory cgroup |
| `-v /path/to/cgroup/cpuacct/docker:/host_docker/cpuacct` | Path to the docker cpuacct cgroup|
|  `-v /path/to/cgroup/blkio/docker:/host_docker/blkio` | Path to the docker blkio cgroup |

## Missing features
Due to the program still being incomplete network metrics are not available, also there might be slight problems depending on the kind of cgroup used due to them being untested.
For reporting issues use the [github](https://github.com/MGvn51/Docker_exporter_prometheus.git) page.

---
### Notes
Features marked with '\*' are not fully tested yet