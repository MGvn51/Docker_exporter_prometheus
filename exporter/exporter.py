'''
Docker metrics exporter for prometheus
'''
# Required modules
import docker
from prometheus_client import start_http_server
from os import getenv
import logging
import time
import custom_modules.get_env as get_env
import custom_modules.prom_metrics as prom_metrics

# Load environment variables
env = get_env.fetch_env()

# Configuring logger
def log_docker_exporter():
	logger = logging.getLogger(__name__)
	handler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s [%(levelname)-7s] %(name)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.setLevel(env['LOG_LEVEL'])
	return logger

# Start logger
log = log_docker_exporter()

# Main program
if __name__ == '__main__':

	# Initialize docker socket connection
	client = docker.DockerClient(base_url='unix://var/run/docker.sock')

	# Create metrics (startup only)
	metrics = prom_metrics.make_metrics(env['METRICS_PREFIX'], env['METRICS_DETAILS'])

	# Start prometheus server
	start_http_server(11211)

	# Start automatic updates
	container_reload_time = time.perf_counter()
	containers_list = client.containers.list()
	while True:
		# Save start time
		start_time = time.perf_counter()
		# Update containers metrics
		for container in containers_list:
			c_time = time.perf_counter()
			prom_metrics.update_metrics(container, metrics, env['METRICS_DETAILS'])
			# Update the metric for update time
			metrics['update_time_seconds'].labels(container.name, container.id).set(time.perf_counter()-c_time)

		# Check if it's time to reload containers
		if time.perf_counter() >= container_reload_time + 60:
			container_reload_time = time.perf_counter()
			containers_list = []
			# Reload containers (renew docker sdk cache)
			for container in client.containers.list():
				container.reload()
				containers_list.append(container)
			# Clean old dontainers metrics
			prom_metrics.clean_old_metrics(containers_list, metrics)

		# Wait until it's time to update the metrics again
		log.debug('Metric update time = ' + str(time.perf_counter() - start_time))
		try:
			time.sleep(5 -(time.perf_counter() - start_time))
		except ValueError:
			log.warning(f'Metrics update took more than {env[UPDATE_SECONDS]} seconds')
			pass
		
		