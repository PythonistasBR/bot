import multiprocessing
import os

workers = os.environ.get("WEB_CONCURRENCY", (multiprocessing.cpu_count() * 2) + 1)

# A path string. "-" means log to stdout.
accesslog = os.environ.get("ACCESS_LOG_PATH", "-")
errorlog = os.environ.get("ERROR_LOG_PATH", "-")
loglevel = "info"
