'''
 Module to fetch environment variables
'''
from os import getenv
import logging
from warnings import warn
from re import match

def _warn_env(ENV_VAR):
	warn(f'Incorrect value of {ENV_VAR}', category=SyntaxWarning)

def _dict_form(DICT):
	form = 'Environment variables : \n'
	for j,i in DICT.items():
		form = form + j + ':' + str(i) + '\n'

def fetch_env():
	_env = {}
	
	# Logging level
	#   Refer to docker logging level (https://docs.python.org/3/howto/logging.html)
	log_level = getenv('LOG_LEVEL', 'info') # Defaults to info level
	log_levels_dict = {'debug' : logging.DEBUG, 'info' : logging.INFO, 'warning' : logging.WARNING, 'error' : logging.ERROR, 'critical' : logging.CRITICAL}
	try:
		_env['LOG_LEVEL'] = log_levels_dict[log_level]
	except KeyError:
		_warn_env('LOG_LEVEL')
		_env['LOG_LEVEL'] = log_levels_dict['info']


	# Docker cgroup type
	#   Refer to docker runtime metrics (https://docs.docker.com/config/containers/runmetrics/)
	_env['CGROUP'] = 'cgroupfs_v2' # Only cgroupfs_v2 is supported for now
	'''
	cgroup = getenv('CGROUP', 'cgroupfs_v2') # Defaults to cgroupfs v2
	if cgroup not in ['cgroupfs_v2', 'cgroupfs_v1', 'systemd_v2', 'systemd_v1']:
		_env['CGROUP'] = 'cgroupfs_v2'
	else:
		warn_env('CGROUP')
		 _env['CGROUP'] = cgroup
	'''
	
	# Interval between prometheus metrics update
	update_seconds = getenv('UPDATE_SECONDS', '5') # Defaults to 5 seconds
	try:
		_env['UPDATE_SECONDS'] = int(update_seconds)
	except ValueError:
		_warn_env('UPDATE_SECONDS')
		_env['UPDATE_SECONDS'] = 5

	# Metrics prefix
	metrics_prefix = getenv('METRICS_PREFIX', 'docker_exporter') # Defaults to 'docker_exporter'
	if match('^[a-zA-Z_]*$', metrics_prefix):
		_env['METRICS_PREFIX'] = metrics_prefix
	else:
		_warn_env('METRICS_PREFIX')

	# Metrics detail
	metrics_details = getenv('METRICS_DETAILS', 'standard') # Defaults to 'standard'
	if metrics_details in ['minimal', 'standard', 'extended']:
		_env['METRICS_DETAILS'] = metrics_details
	else:
		_warn_env('METRICS_DETAILS')
	
	# Containers reload seconds
	containers_reload_seconds = getenv('CONTAINERS_RELOAD_SECONDS', '60') # Defaults to '60'
	try:
		_env['CONTAINERS_RELOAD_SECONDS'] = int(containers_reload_seconds)
	except ValueError:
		_warn_env('CONTAINERS_RELOAD_SECONDS')
		_env['CONTAINERS_RELOAD_SECONDS'] = 60

	# If logging is set to debug level print a human readable version of the envirnment variables
	logging.debug(_dict_form(_env))
	# Return the environment variables
	return _env