'''
 Prometheus metrics creation and update
'''
from prometheus_client import Gauge
import docker
import logging
from time import perf_counter

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



def report_file_warning(FILE_PATH):
	log_docker_exporter().warning(f'Unable to open file at path : "{FILE_PATH}"')



def make_metrics(METRICS_PREFIX = 'docker_exporter', METRICS_DETAILS = 'standard'):
	# Chart of details levels
	DETAILS_LEVELS = {'minimal' : 0, 'standard' : 1, 'extended' : 2}
	# Create prometheus metrics
	metrics_dict = {}
	
	# Minimal
	#   Memory
	metrics_dict['mem_usage'] = Gauge(METRICS_PREFIX + '_mem_usage', 'Amount of memory used by the container.', ['name', 'id'])
	metrics_dict['mem_max_usage'] = Gauge(METRICS_PREFIX + '_mem_max_usage', 'Maximum amount of memory used by the container.', ['name', 'id'])
	#metrics_dict['mem_limit'] = Gauge(METRICS_PREFIX + '_mem_limit', 'Maximum amount of memory the container can use.', ['name', 'id'])
	#metrics_dict['mem_percent'] = Gauge(METRICS_PREFIX + '_mem_percent', 'Percentage of memory used by the container.', ['name', 'id'])
	#   CPU
	#metrics_dict['cpu_percent'] = Gauge(METRICS_PREFIX + '_cpu_percent', 'Percentage of cpu used by the container.', ['name', 'id'])
	metrics_dict['cpu_cpus'] = Gauge(METRICS_PREFIX + '_cpu_cpus', 'Number of online CPUs.', ['name', 'id'])
	#   Block I/O
	metrics_dict['blkio_bytes_read_tot'] = Gauge(METRICS_PREFIX + '_blkio_bytes_read_tot', 'Total amount of bytes read by the cointainer.', ['name', 'id'])
	metrics_dict['blkio_bytes_write_tot'] = Gauge(METRICS_PREFIX + '_blkio_bytes_write_tot', 'Total amount of bytes written by the cointainer.', ['name', 'id'])
	#   Network
	#metrics_dict['_network_tx_bytes_tot'] = Gauge(METRICS_PREFIX + '_network_sent_bytes_tot', 'Total amount of bytes sent by the container.', ['name', 'id'])
	#metrics_dict['_network_rx_bytes_tot'] = Gauge(METRICS_PREFIX + '_network_received_bytes_tot', 'Total amount of bytes received by the container.', ['name', 'id'])
	#   Others
	metrics_dict['update_time_seconds'] = Gauge(METRICS_PREFIX + '_update_time_seconds', 'Time it took to update the metrics of the container.', ['name', 'id'])

	# Standard
	if DETAILS_LEVELS[METRICS_DETAILS] >= DETAILS_LEVELS['standard']:
		# Memory
		metrics_dict['mem_cache'] = Gauge(METRICS_PREFIX + '_mem_cache', 'The amount of memory used by the processes of this control group that can be associated precisely with a block on a block device.', ['name','id'])
		metrics_dict['mem_rss'] = Gauge(METRICS_PREFIX + '_mem_rss', 'The amount of memory that doesn’t correspond to anything on disk: stacks, heaps, and anonymous memory maps.', ['name','id'])
		metrics_dict['mem_mapped_file'] = Gauge(METRICS_PREFIX + '_mem_mapped_file', 'Indicates the amount of memory mapped by the processes in the control group.', ['name','id'])
		metrics_dict['mem_pgfault'] = Gauge(METRICS_PREFIX + '_mem_pgfault', 'Indicate the number of times that a process of the cgroup triggered a “page fault”.', ['name','id'])
		metrics_dict['mem_pgmajfault'] = Gauge(METRICS_PREFIX + '_mem_pgmajfault', 'Indicate the number of times that a process of the cgroup triggered a “major fault”.', ['name','id'])
		metrics_dict['mem_active_anon'] = Gauge(METRICS_PREFIX + '_mem_active_anon', 'The amount of anonymous memory that has been identified as active by the kernel.', ['name','id'])
		metrics_dict['mem_inactive_anon'] = Gauge(METRICS_PREFIX + '_mem_inactive_anon', 'The amount of anonymous memory that has been identified as inactive by the kernel.', ['name','id'])
		metrics_dict['mem_active_file'] = Gauge(METRICS_PREFIX + '_mem_active_file', 'The amount of cache memory that has been identified as active by the kernel.', ['name','id'])
		metrics_dict['mem_inactive_file'] = Gauge(METRICS_PREFIX + '_mem_inactive_file', 'The amount of cache memory that has been identified as inactive by the kernel.', ['name','id'])
		metrics_dict['mem_unevictable'] = Gauge(METRICS_PREFIX + '_mem_unevictable', 'The amount of memory that cannot be reclaimed.', ['name','id'])
		# CPU
		metrics_dict['cpu_user_seconds'] = Gauge(METRICS_PREFIX + '_cpu_user_seconds', 'Amount of time a process has direct control of the CPU, executing process code.', ['name','id'])
		metrics_dict['cpu_system_seconds'] = Gauge(METRICS_PREFIX + '_cpu_system_seconds', 'Amount of time the kernel is executing system calls on behalf of the process.', ['name','id'])
		#metrics_dict['cpu_total_usage_seconds'] = Gauge(METRICS_PREFIX + '_cpu_total_usage_seconds', 'Total amount of time the container is using the CPU', ['name', 'id'])
		#metrics_dict['cpu_system_cpu_usage_seconds'] = Gauge(METRICS_PREFIX + '_cpu_system_cpu_usage_seconds', 'Total amount of time the CPU has been executing code.', ['name', 'id'])
		# Block I/O
		metrics_dict['blkio_bytes_read'] = Gauge(METRICS_PREFIX + '_blkio_bytes_read', 'Number of bytes read.', ['name', 'id', 'device'])
		metrics_dict['blkio_bytes_write'] = Gauge(METRICS_PREFIX + '_blkio_bytes_write', 'Number of bytes written.', ['name', 'id', 'device'])
		metrics_dict['blkio_io_read'] = Gauge(METRICS_PREFIX + '_blkio_io_read', 'Number of reads.', ['name', 'id', 'device'])
		metrics_dict['blkio_io_write'] = Gauge(METRICS_PREFIX + '_blkio_io_write', 'Number of writes.', ['name', 'id', 'device'])
		# Network
		#metrics_dict['network_rx_bytes'] = Gauge(METRICS_PREFIX + '_network_received_bytes', 'Total amount of received bytes from container interface.', ['name', 'id', 'interface'])
		#metrics_dict['network_tx_bytes'] = Gauge(METRICS_PREFIX + '_network_sent_bytes', 'Total amount of sent bytes from container interface.', ['name', 'id', 'interface'])

	# Extended
	if DETAILS_LEVELS[METRICS_DETAILS] >= DETAILS_LEVELS['extended']:
		# Memory
		metrics_dict['mem_dirty'] = Gauge(METRICS_PREFIX + '_mem_dirty', '', ['name', 'id'])
		metrics_dict['mem_hierarchical_memory_limit'] = Gauge(METRICS_PREFIX + '_mem_hierarchical_memory_limit', '', ['name', 'id'])
		#metrics_dict['mem_hierarchical_memsw_limit'] = Gauge(METRICS_PREFIX + '_mem_hierarchical_memsw_limit', '', ['name', 'id'])
		metrics_dict['mem_pgpgin'] = Gauge(METRICS_PREFIX + '_mem_pgpgin', '', ['name', 'id'])
		metrics_dict['mem_pgpgout'] = Gauge(METRICS_PREFIX + '_mem_pgpgout', '', ['name', 'id'])
		metrics_dict['mem_rss_huge'] = Gauge(METRICS_PREFIX + '_mem_rss_huge', '', ['name', 'id'])
		metrics_dict['mem_total_active_anon'] = Gauge(METRICS_PREFIX + '_mem_total_active_anon', '', ['name', 'id'])
		metrics_dict['mem_total_active_file'] = Gauge(METRICS_PREFIX + '_mem_total_active_file', '', ['name', 'id'])
		metrics_dict['mem_total_cache'] = Gauge(METRICS_PREFIX + '_mem_total_cache', '', ['name', 'id'])
		metrics_dict['mem_total_dirty'] = Gauge(METRICS_PREFIX + '_mem_total_dirty', '', ['name', 'id'])
		metrics_dict['mem_total_inactive_anon'] = Gauge(METRICS_PREFIX + '_mem_total_inactive_anon', '', ['name', 'id'])
		metrics_dict['mem_total_inactive_file'] = Gauge(METRICS_PREFIX + '_mem_total_inactive_file', '', ['name', 'id'])
		metrics_dict['mem_total_mapped_file'] = Gauge(METRICS_PREFIX + '_mem_total_mapped_file', '', ['name', 'id'])
		metrics_dict['mem_total_pgfault'] = Gauge(METRICS_PREFIX + '_mem_total_pgfault', '', ['name', 'id'])
		metrics_dict['mem_total_pgmajfault'] = Gauge(METRICS_PREFIX + '_mem_total_pgmajfault', '', ['name', 'id'])
		metrics_dict['mem_total_pgpgin'] = Gauge(METRICS_PREFIX + '_mem_total_pgpgin', '', ['name', 'id'])
		metrics_dict['mem_total_pgpgout'] = Gauge(METRICS_PREFIX + '_mem_total_pgpgout', '', ['name', 'id'])
		metrics_dict['mem_total_rss'] = Gauge(METRICS_PREFIX + '_mem_total_rss', '', ['name', 'id'])
		metrics_dict['mem_total_rss_huge'] = Gauge(METRICS_PREFIX + '_mem_total_rss_huge', '', ['name', 'id'])
		metrics_dict['mem_total_unevictable'] = Gauge(METRICS_PREFIX + '_mem_total_unevictable', '', ['name', 'id'])
		metrics_dict['mem_total_writeback'] = Gauge(METRICS_PREFIX + '_mem_total_writeback', '', ['name', 'id'])
		metrics_dict['mem_writeback'] = Gauge(METRICS_PREFIX + '_mem_writeback', '', ['name', 'id'])

		# CPU
		metrics_dict['cpu_percpu_usage_seconds'] = Gauge(METRICS_PREFIX + '_cpu_percpu_usage_seconds', '', ['name', 'id', 'cpu'])
		metrics_dict['cpu_throttling_periods'] = Gauge(METRICS_PREFIX + '_cpu_throttling_periods', '', ['name', 'id'])
		metrics_dict['cpu_throttled_periods'] = Gauge(METRICS_PREFIX + '_cpu_throttled_periods', '', ['name', 'id'])
		metrics_dict['cpu_throttled_time'] = Gauge(METRICS_PREFIX + '_cpu_throttled_time', '', ['name', 'id'])

		# Block I/O
		metrics_dict['blkio_bytes_sync'] = Gauge(METRICS_PREFIX + '_blkio_bytes_sync', 'Number of syncronous I/O.', ['name', 'id', 'device'])
		metrics_dict['blkio_bytes_async'] = Gauge(METRICS_PREFIX + '_blkio_bytes_async', 'Number of asyncronous I/O.', ['name', 'id', 'device'])
		metrics_dict['blkio_bytes_discard'] = Gauge(METRICS_PREFIX + '_blkio_bytes_discard', '', ['name', 'id', 'device'])
		metrics_dict['blkio_bytes_total'] = Gauge(METRICS_PREFIX + '_blkio_bytes_total', '', ['name', 'id', 'device'])
		metrics_dict['blkio_io_sync'] = Gauge(METRICS_PREFIX + '_blkio_io_sync', 'Number of syncronous R/W.', ['name', 'id', 'device'])
		metrics_dict['blkio_io_async'] = Gauge(METRICS_PREFIX + '_blkio_io_async', 'Number of asyncronous R/W.', ['name', 'id', 'device'])
		metrics_dict['blkio_io_discard'] = Gauge(METRICS_PREFIX + '_blkio_io_discard', '', ['name', 'id', 'device'])
		metrics_dict['blkio_io_total'] = Gauge(METRICS_PREFIX + '_blkio_io_total', '', ['name', 'id', 'device'])

		# Network
		#metrics_dict['network_rx_packets'] = Gauge(METRICS_PREFIX + '_network_rx_packets', 'Total number of received packets from container interface.', ['name', 'id', 'interface'])
		#metrics_dict['network_rx_errors'] = Gauge(METRICS_PREFIX + '_network_rx_errors', 'Total number of errored received packets from container interface.', ['name', 'id', 'interface'])
		#metrics_dict['network_rx_dropped'] = Gauge(METRICS_PREFIX + '_network_rx_dropped', 'Total number of dropped received packets from container interface', ['name', 'id', 'interface'])
		#metrics_dict['network_tx_packets'] = Gauge(METRICS_PREFIX + '_network_tx_packets', 'Total number of transmitted packets from container interface.', ['name', 'id', 'interface'])
		#metrics_dict['network_tx_errors'] = Gauge(METRICS_PREFIX + '_network_tx_errors', 'Total number of errored transmitted packets from container interface.', ['name', 'id', 'interface'])
		#metrics_dict['network_tx_dropped'] = Gauge(METRICS_PREFIX + '_network_tx_dropped', 'Total number of dropped transmitted packets from container interface.', ['name', 'id', 'interface'])

	# Return dictionary
	return metrics_dict



def update_metrics(CONTAINER, metrics_dict, METRICS_DETAILS):
	# Chart of details levels
	DETAILS_LEVELS = {'minimal' : 0, 'standard' : 1, 'extended' : 2}

	# Files path
	MEM_STAT_PATH = f'/host_docker/memory/{CONTAINER.id}/memory.stat'
	MEM_USAGE_PATH = f'/host_docker/memory/{CONTAINER.id}/memory.usage_in_bytes'
	MEM_MAX_PATH = f'/host_docker/memory/{CONTAINER.id}/memory.max_usage_in_bytes'
	CPU_PATH = f'/host_docker/cpuacct/{CONTAINER.id}/cpuacct.stat'
	CPU_PERCPU_PATH = f'/host_docker/cpuacct/{CONTAINER.id}/cpuacct.usage_percpu'
	CPU_TROTTLE_PATH = f'/host_docker/cpuacct/{CONTAINER.id}/cpu.stat'
	BLK_IO_PATH = f'/host_docker/blkio/{CONTAINER.id}/blkio.throttle.io_serviced'
	BLK_BYTES_PATH = f'/host_docker/blkio/{CONTAINER.id}/blkio.throttle.io_service_bytes'

	# Minimal
	#   Memory usage
	try:
		with open(MEM_USAGE_PATH, 'r') as f:
			metrics_dict['mem_usage'].labels(CONTAINER.name, CONTAINER.id).set(int(f.read()))
	except FileNotFoundError:
		report_file_warning(MEM_USAGE_PATH)
	#   Memory usage max
	try:
		with open(MEM_MAX_PATH, 'r') as f:
			metrics_dict['mem_max_usage'].labels(CONTAINER.name, CONTAINER.id).set(int(f.read()))
	except FileNotFoundError:
		report_file_warning(MEM_MAX_PATH)
	
	#   CPU cpus + CPU per CPU statistics (for minimal and extended)
	try:
		with open(CPU_PERCPU_PATH, 'r') as f:
			cpu_list = f.read().split()
			n_cpus = 0
			for j in range(len(cpu_list)):
				if cpu_list[j] != '0':
					try:
						metrics_dict['cpu_percpu_usage_seconds'].labels(CONTAINER.name, CONTAINER.id, j).set(int(cpu_list[j])/1000000000)
					except KeyError:
						pass
					n_cpus = n_cpus + 1
			metrics_dict['cpu_cpus'].labels(CONTAINER.name, CONTAINER.id).set(n_cpus)
	except FileNotFoundError:
		report_file_warning(CPU_PERCPU_PATH)
	
	#   Blkio total R/W bytes + per device bytes stats (minimal + standard + extended)
	try:
		with open(BLK_BYTES_PATH, 'r') as f:
			tmp_list = f.read().split()
			tot_read = 0
			tot_write = 0
			for j in range(0, len(tmp_list)-2, 3):
				try:
					metrics_dict['blkio_bytes_' + tmp_list[j+1].lower()].labels(CONTAINER.name, CONTAINER.id, tmp_list[j]).set(int(tmp_list[j+2]))
					if tmp_list[j+1] == 'Read':
						tot_read = tot_read + int(tmp_list[j+2])
					elif tmp_list[j+1] == 'Write':
						tot_write = tot_write + int(tmp_list[j+2])
				except KeyError:
					pass
			metrics_dict['blkio_bytes_read_tot'].labels(CONTAINER.name, CONTAINER.id).set(tot_read)
			metrics_dict['blkio_bytes_write_tot'].labels(CONTAINER.name, CONTAINER.id).set(tot_write)
	except FileNotFoundError:
		report_file_warning(BLK_BYTES_PATH)

	# Standard
	if DETAILS_LEVELS[METRICS_DETAILS] >= DETAILS_LEVELS['standard']:
		# Memory statistics (contains both standard and extended)
		try:
			with open(MEM_STAT_PATH, 'r') as f:
				tmp_list = f.read().split()
				for j in range(0, len(tmp_list), 2):
					try:
						metrics_dict['mem_' + tmp_list[j]].labels(CONTAINER.name, CONTAINER.id).set(int(tmp_list[j+1]))
					except KeyError:
						pass
		except FileNotFoundError:
			report_file_warning(MEM_STAT_PATH)

		# CPU statistics
		try:
			with open(CPU_PATH, 'r') as f:
				cpu_stats_list = f.read().split()
				metrics_dict['cpu_user_seconds'].labels(CONTAINER.name, CONTAINER.id).set(int(cpu_stats_list[1])/100)
				metrics_dict['cpu_system_seconds'].labels(CONTAINER.name, CONTAINER.id).set(int(cpu_stats_list[3])/100)
		except FileNotFoundError:
			logging.warning(f'Unable to open file : "{CPU_PATH}"')
		
		# Block I/O (standard + extended)
		try:
			with open(BLK_IO_PATH, 'r') as f:
				tmp_list = f.read().split()
				for j in range(0, len(tmp_list)-2, 3):
					try:
						metrics_dict['blkio_io_' + tmp_list[j+1].lower()].labels(CONTAINER.name, CONTAINER.id, tmp_list[j]).set(int(tmp_list[j+2]))
					except KeyError:
						pass
		except FileNotFoundError:
			report_file_warning(BLK_IO_PATH)
	

	# Extended
	if DETAILS_LEVELS[METRICS_DETAILS] >= DETAILS_LEVELS['extended']:
		# Memory (processed along standard)
		
		# CPU trottling
		try:
			with open(CPU_TROTTLE_PATH, 'r') as f:
				tmp_list = f.read().split()
				metrics_dict['cpu_throttling_periods'].labels(CONTAINER.name, CONTAINER.id).set(tmp_list[1])
				metrics_dict['cpu_throttled_periods'].labels(CONTAINER.name, CONTAINER.id).set(tmp_list[3])
				metrics_dict['cpu_throttled_time'].labels(CONTAINER.name, CONTAINER.id).set(tmp_list[5])
		except FileNotFoundError:
			report_file_warning(CPU_TROTTLE_PATH)

		# Block I/O



# Test container_metrics
if __name__ == '__main__':
	import docker
	# Initialize docker socket connection
	client = docker.DockerClient(base_url='unix://var/run/docker.sock')
	# Test metrics
	test_metrics = make_metrics(METRICS_DETAILS='extended')
	update_metrics(client.containers.list()[0], test_metrics, 'extended')
	#
	for net in client.networks.list(greedy=True):
		get_net_info(net)
