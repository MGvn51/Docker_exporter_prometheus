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
	#logger.setLevel(env['LOG_LEVEL'])
	logger.setLevel(logging.DEBUG)
	return logger

# Start logger
log = log_docker_exporter()

# Main program
if __name__ == '__main__':

	# Initialize docker socket connection
	client = docker.DockerClient(base_url='unix://var/run/docker.sock')

	# Create metrics (startup only)
	metrics = prom_metrics.make_metrics()

	# Start prometheus server
	start_http_server(11211)

	# Start automatic updates
	while True:
		# Save start time
		start_time = time.perf_counter()
		for container in client.containers.list():
			prom_metrics.update_metrics(container, metrics)

		# Wait until 5s have passed from the updates
		log.debug('Metric update time = ' + str(time.perf_counter() - start_time))
		time.sleep(5 -(time.perf_counter() - start_time))

	