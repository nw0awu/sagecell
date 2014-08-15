import os.path

# location of a sage executable
sage = ""

# defaults if sage isn't set above
if sage == "":
    if 'SAGE_ROOT' in os.environ:
        # assume that the untrusted worker should run the same copy of sage
        # that is used to run the web server
        sage = os.path.join(os.environ["SAGE_ROOT"],"sage")
    else:
        # assume both the web server and the untrusted workers have sage in their paths
        sage = "sage"

#db = "sqlalchemy"
#db_config = {"uri": "sqlite:///sqlite.db"}

db = "web"
db_config = {"uri": "https://sagecell.sagemath.org/permalink"}
# db = "web"
# db_config = {"uri": "http://localhost:8889"}

requires_tos = True

permalink_server = {
    'db': 'sqlalchemy',
    'db_config': {'uri': 'sqlite:///sqlite.db'}
}

max_kernel_timeout = 60*90 # 90 minutes, for interacts
pid_file='/home/{server}/sagecell.pid'

computers = []
_default_config = {"host": "localhost",
                  "username": "{worker}",
                  "python": sage + " -python",
                  "location": os.path.dirname(os.path.abspath(__file__)),
# The keys to resource_limits can be any available resources
# for the resource module. See http://docs.python.org/library/resource.html
# for more information (section 35.13.1)

# Note: RLIMIT_NPROC doesn't really work
# Note: RLIMIT_AS is more of a suggestion than a hard limit in Mac OS X
# Note: All other resource limits seem to be working, but besides RLIMIT_CPU and
# RLIMIT_AS they don't actually kill off offending processes
                  "resource_limits": {"RLIMIT_CPU": 120, # CPU time in seconds
                                      "RLIMIT_AS": 3*(2**30), #Maximum address space in bytes; this sets 3 GB
                                     },
# The log file will be in the home directory of the untrusted account
                  "log_file": "sagecell.log",
                  "max_kernels": 30,
                  "preforked_kernels": 5,
# These set paramaters for a heartbeat channel checking whether a given kernel is alive.
# Setting first_beat lower than 1.0 may cause javascript errors.
                  "beat_interval": 0.5,
                  "first_beat": 1.0}

for i in range(4):
    computers.append(_default_config)

import logging
from logging.handlers import SysLogHandler
h = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_LOCAL3)
h.setFormatter(logging.Formatter('%(asctime)s %(name)s %(process)d: %(message)s'))
logging.getLogger('sagecell.stats').addHandler(h)

systemlog_handler = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_LOCAL4)
systemlog_handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(process)d: %(message)r'))
logging.getLogger("tornado.application").addHandler(systemlog_handler)
logging.getLogger('sagecell.system').addHandler(systemlog_handler)
