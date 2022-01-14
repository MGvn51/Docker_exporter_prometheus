'''
 Prometheus metrics creation and update
'''
from prometheus_client import Gauge
import logging

def make_metrics(METRICS_PREFIX = 'docker_exporter'):
	# Create prometheus metrics
	metrics_dict = {}
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
	
	# Block I/O
	metrics_dict['blkio_bytes_read'] = Gauge(METRICS_PREFIX + '_blkio_bytes_read', 'Number of bytes read.', ['name', 'id', 'device'])
	metrics_dict['blkio_bytes_write'] = Gauge(METRICS_PREFIX + '_blkio_bytes_write', 'Number of bytes written.', ['name', 'id', 'device'])
	metrics_dict['blkio_bytes_sync'] = Gauge(METRICS_PREFIX + '_blkio_bytes_sync', 'Number of syncronous I/O.', ['name', 'id', 'device'])
	metrics_dict['blkio_bytes_async'] = Gauge(METRICS_PREFIX + '_blkio_bytes_async', 'Number of asyncronous I/O.', ['name', 'id', 'device'])
	metrics_dict['blkio_io_read'] = Gauge(METRICS_PREFIX + '_blkio_io_read', 'Number of reads.', ['name', 'id', 'device'])
	metrics_dict['blkio_io_write'] = Gauge(METRICS_PREFIX + '_blkio_io_write', 'Number of writes.', ['name', 'id', 'device'])
	metrics_dict['blkio_io_sync'] = Gauge(METRICS_PREFIX + '_blkio_io_sync', 'Number of syncronous R/W.', ['name', 'id', 'device'])
	metrics_dict['blkio_io_async'] = Gauge(METRICS_PREFIX + '_blkio_io_async', 'Number of asyncronous R/W.', ['name', 'id', 'device'])
	
	# Network

	# Return dictionary
	return metrics_dict



def update_metrics(CONTAINER, metrics_dict):
	# Container data
	# For short ID use first 12 characters
			
	# Path to resources
	MEM_PATH = f'/host_docker/memory/{CONTAINER.id}/memory.stat'
	CPU_PATH = f'/host_docker/cpuacct/{CONTAINER.id}/cpuacct.stat'
	BLK_IO_PATH = f'/host_docker/blkio/{CONTAINER.id}/blkio.throttle.io_serviced'
	BLK_BYTES_PATH = f'/host_docker/blkio/{CONTAINER.id}/blkio.throttle.io_service_bytes'
	
	# Updates prometheus metrics
	tmp_mem_file = ''
	tmp_cpu_file = ''
	tmp_blk_io_file = ''
	tmp_blk_bytes_file = ''

	# Get memory data from MEM_PATH
	try:
		with open(MEM_PATH, 'r') as f:
			tmp_mem_file = f.read()
	except FileNotFoundError:
		logging.warning(f'WARNING : Unable to find memory file - {MEM_PATH}')
	except OSError:
		logging.warning(f'WARNING : Unable to open memory file - {MEM_PATH}')
	
	# Set the values for the corresponding keys in metrics_dict
	if tmp_mem_file != '':
		tmp_mem_list = tmp_mem_file.split()
		for i in range(0, len(tmp_mem_list), 2):
			try:
				#print('mem_' + tmp_mem_list[i] + ' : ' + tmp_mem_list[i+1])
				metrics_dict['mem_' + tmp_mem_list[i]].labels(CONTAINER.name, CONTAINER.id).set(int(tmp_mem_list[i+1]))
			except KeyError:
				pass

	# Get cpu data from CPU_PATH
	try:
		with open(CPU_PATH, 'r') as f:
			tmp_cpu_file = f.read()
	except FileNotFoundError:
		logging.warning(f'WARNING : Unable to find cpu file - {CPU_PATH}')
	except OSError:
		logging.warning(f'WARNING : Unable to open cpu file - {CPU_PATH}')

	# Set the values for the corresponding keys in metrics_dict
	if tmp_cpu_file != '':
		tmp_cpu_list = tmp_cpu_file.split()
		for i in range(0, len(tmp_cpu_list), 2):
			try:
				#print('cpu_' + tmp_cpu_list[i] + ' : ' + str(int(tmp_cpu_list[i+1])/100))
				metrics_dict['cpu_' + tmp_cpu_list[i] + '_seconds'].labels(CONTAINER.name, CONTAINER.id).set(int(tmp_cpu_list[i+1])/100)
			except KeyError:
				pass
	
	

	# Get block I/O data from BLK_IO_PATH and BLK_BYTES_PATH
	#  I/O data
	try:
		with open(BLK_IO_PATH, 'r') as f:
			tmp_blk_io_file = f.read()
	except FileNotFoundError:
		logging.warning(f'WARNING : Unable to find block I/O file - {BLK_IO_PATH}')
	except OSError:
		logging.warning(f'WARNING : Unable to open block I/O file - {BLK_IO_PATH}')

	# Set the values for the corresponding keys in metrics_dict
	if tmp_blk_io_file != '':
		tmp_blk_io_list = tmp_blk_io_file.split()
		for i in range(0, len(tmp_blk_io_list)-2, 3):
			try:
				#print('blkio_io_' + tmp_blk_io_list[i+1].lower() + ' : ' + tmp_blk_io_list[i+2] + ' - ' + tmp_blk_io_list[i])
				metrics_dict['blkio_io_' + tmp_blk_io_list[i+1].lower()].labels(CONTAINER.name, CONTAINER.id, tmp_blk_io_list[i]).set(int(tmp_blk_io_list[i+2]))		
			except KeyError:
				pass
	
	#  bytes data
	try:
		with open(BLK_BYTES_PATH, 'r') as f:
			tmp_blk_bytes_file = f.read()
	except FileNotFoundError:
		logging.warning(f'WARNING : Unable to find block bytes file - {BLK_BYTES_PATH}')
	except OSError:
		logging.warning(f'WARNING : Unable to open block bytes file - {BLK_BYTES_PATH}')

	# Set the values for the corresponding keys in metrics_dict
	if tmp_blk_bytes_file != '':
		tmp_blk_bytes_list = tmp_blk_bytes_file.split()
		for i in range(0, len(tmp_blk_bytes_list)-2, 3):
			try:
				#print('blkio_bytes_' + tmp_blk_bytes_list[i+1].lower() + ' : ' + tmp_blk_bytes_list[i+2] + ' - ' + tmp_blk_bytes_list[i])
				metrics_dict['blkio_bytes_' + tmp_blk_bytes_list[i+1].lower()].labels(CONTAINER.name, CONTAINER.id, tmp_blk_bytes_list[i]).set(int(tmp_blk_bytes_list[i+2]))	
			except KeyError:
				pass



# Test container_metrics
if __name__ == '__main__':
	import docker
	# Initialize docker socket connection
	client = docker.DockerClient(base_url='unix://var/run/docker.sock')
	# Make new class istance
	test_metric = make_metrics()
	update_metrics(client.containers.list()[0], test_metric)