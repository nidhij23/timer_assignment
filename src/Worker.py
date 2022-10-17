from rq import Worker, Queue, Connection

from ConfigurationController import configuration
from src.RedisQueue import redis_connection
from ExceptionHandlers import failed_job_handler

QUEUE_LIST = configuration["queues_prefix"]

if __name__ == '__main__':
    with Connection(redis_connection):
        worker = Worker(queues=list(map(Queue, QUEUE_LIST)), exception_handlers=[failed_job_handler],
                        disable_default_exception_handler=True)
    worker.work(with_scheduler=True)
