import multiprocessing

# Worker Processes
workers = 2
worker_class = 'sync'

# Logging
logfile = '/home/ubuntu/Log/yourkotaichi.log'
loglevel = 'info'
logconfig = None

#bind
bind = "0.0.0.0:9877"

#socket
#socket_path = 'unix:/tmp/hellportal.sock'
#bind = socket_path
