import datetime
import time

import requests
from dateutil import relativedelta

from RedisQueue import remove_key, redis_connection


class Timer:
    def __init__(self, hours, minutes, seconds, url):
        self.__hours = hours
        self.__minutes = minutes
        self.__seconds = seconds
        self.__webURL = url
        self.__createdAtTimestamp = time.time()
        self.__id = None

    def set_time(self, hours, minutes, seconds):
        self.__hours = hours
        self.__minutes = minutes
        self.__seconds = seconds

    def set_id(self, id):
        self.__id = id

    def get_timer_duration(self):
        seconds = self.__hours * 3600 + self.__minutes * 60 + self.__seconds
        return seconds

    def get_url(self):
        return self.__webURL

    def get_id(self):
        return self.__id

    def get_timer_difference(self):
        current_time = time.time()
        timer_time = self.__createdAtTimestamp
        dt1 = datetime.datetime.fromtimestamp(current_time)
        dt2 = datetime.datetime.fromtimestamp(timer_time)
        rd = relativedelta.relativedelta(dt1, dt2)
        seconds = rd.hours * 3600 + rd.minutes * 60 + rd.seconds
        return seconds

    def get_remaining_time(self):
        time_passed = self.get_timer_difference()
        time_difference = self.get_timer_duration() - time_passed
        if time_difference < 0:
            print("Time is up by", -1 * time_difference)
            return 0
        else:
            return time_difference

    def valid_timer(self):
        hours = self.__hours
        minutes = self.__minutes
        seconds = self.__seconds
        if hours == 0 and minutes == 0 and seconds == 0:
            return False
        if not hours >= 0 or not hours < 24:
            return False
        if not minutes >= 0 or not minutes < 60:
            return False
        if not seconds >= 0 or not seconds < 60:
            return False
        return True


def generate_webhook(url, timer_id):
    try:
        new_url = url + "/" + str(timer_id)
        response = requests.post(new_url)
        if response.status_code == timer_id:
            print("Webhook generated for id:", timer_id)
            remove_key(redis_connection, timer_id)
    except Exception as ex:
        print("webhook could not be generated", ex)


def start_timer(url, timer_id):
    print("Started timer for: ", timer_id)
    generate_webhook(url, timer_id)


def get_readable_format(epoch_timestamp):
    return time.ctime(epoch_timestamp)
