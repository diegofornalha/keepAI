import multiprocessing

bind = "0.0.0.0:5000"
workers = 3
worker_class = "sync"
reload = True
reload_engine = "auto"
reload_extra_files = ["templates/", "static/"]
timeout = 120
keepalive = 5
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True
daemon = False
pidfile = None
umask = 0
user = None
group = None
