from datetime import timedelta

from redis import Redis
from rq import Queue
from rq.registry import BaseRegistry
from rq_scheduler import Scheduler

from ConfigurationController import configuration

QUEUE_LIST = configuration["queues_prefix"]
REDIS_HOST = configuration["redis_host"]
REDIS_PORT = configuration["redis_port"]

# export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
redis_connection = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
redis_queue = Queue(QUEUE_LIST[0], connection=redis_connection)
scheduler = Scheduler(queue=redis_queue, connection=redis_connection)


def set_key(redis: Redis, key: int, value):
    redis.set(key, value)
    return True


def set_expiration(redis: Redis, key: int, ttl: int):
    redis.expire(key, ttl)
    return True


def check_if_exists(redis: Redis, key: int):
    return redis.exists(key)


def remove_key(redis: Redis, key: int):
    return redis.delete(key)


def push_to_queue(delay, func, args):
    return redis_queue.enqueue_in(timedelta(seconds=delay), func, kwargs=args)


def print_jobs(registry: BaseRegistry):
    for job in registry:
        print(job)


def flush_registry(registry: BaseRegistry):
    for job in registry:
        print("Cleaning up job: ", job)
        registry.remove(job)


# def retry_failed_jobs(registry: BaseRegistry):
#     for job in registry:
#         redis_queue.enqueue(job)

def requeue_jobs(redis: Redis, delay, func):
    for key in redis.scan_iter():
        delay = redis.ttl(key)
        if delay < 0:
            delay = 0
        timer_url = redis.get(key)
        timer_id = key
        timer_data = {"url": timer_url, "timer_id": timer_id}
        push_to_queue(delay, func, args=timer_data)


def cleanup_finished_jobs(queue):
    finished_jobs = queue.finished_job_registry.get_job_ids()
    flush_registry(finished_jobs)
    return True


def get_jobs_status(queue: Queue):
    print("finished_job")
    print_jobs(queue.finished_job_registry.get_job_ids())
    print("failed_job")
    print_jobs(queue.failed_job_registry.get_job_ids())
    print("scheduled_job")
    print_jobs(queue.scheduled_job_registry.get_job_ids())


if __name__ == "__main__":
    get_jobs_status(redis_queue)
