import multiprocessing

bind = "0.0.0.0:3000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"  # Mudando para worker sync do Flask
timeout = 120
keepalive = 5
errorlog = "-"
accesslog = "-"
capture_output = True 