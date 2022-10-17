import json

CONFIG_PATH = "../config.json"
config_file = open(CONFIG_PATH)
configuration = json.load(config_file)
config_file.close()

