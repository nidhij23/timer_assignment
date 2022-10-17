import datetime
import math
from random import random

import requests


from ConfigurationController import configuration

ID_RANGE = configuration['id_range']


def have_fun(name):
    print("Have fun",name)





def generate_id():
    value = math.floor(random() * ID_RANGE)
    return value
