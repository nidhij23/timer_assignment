from flask import Flask, request

from src.MultiProcessingController import spawn_new_process
from src.RedisQueue import *
from src.Timer import start_timer, Timer
from src.utils import *

FLASK_APP_PORT = configuration["flask_app_port"]
FLASK_APP_HOST = configuration["flask_app_host"]

app = Flask(__name__)


@app.route('/timers/<int:timer_id>', methods=['GET'])
def get_timer(timer_id):
    timer = redis_connection.get(timer_id)
    time_left = redis_connection.ttl(timer_id)
    print("timer", timer)
    if time_left < 0:
        time_left = 0
    return {'id': timer_id, 'timer_left': time_left}


@app.route('/timers/', methods=['POST'])
def set_timer():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        new_timer = Timer(json['hours'], json['minutes'], json['seconds'], json['url'])
        if new_timer.valid_timer():
            new_id = generate_id()
            while check_if_exists(redis_connection, new_id):
                new_id = generate_id()
            timer_duration = new_timer.get_timer_duration()
            new_timer.set_id(new_id)
            set_key(redis_connection, new_id, new_timer.get_url())
            set_expiration(redis_connection, new_id, timer_duration)
            timer_data = {"url": new_timer.get_url(), "timer_id": new_timer.get_id()}
            spawn_new_process(push_to_queue, args=[timer_duration, start_timer, timer_data])
            print("Queued timer for: ", new_id)
            return {"id": new_id}
        else:
            return 'Invalid timer format, It should contain hours(0-23), minutes(0-59) and seconds(0-59) and be ' \
                   'greater than 0 seconds '
    else:
        return 'Content-Type not supported!'


if __name__ == '__main__':
    cleanup_finished_jobs(redis_queue)
    # retry_expired_jobs(redis_connection, 0, start_timer)
    app.run(host=FLASK_APP_HOST, port=FLASK_APP_PORT)

