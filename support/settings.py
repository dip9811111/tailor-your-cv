import configparser
import os


TESTING = False
if TESTING:
    api_key_value = "fake-api-key"
    dest_dir = "test"
else:
    dest_dir = "output"
    api_key_value = ""
    if os.path.exists("config.ini"):
        config = configparser.ConfigParser()
        config.read("config.ini")
        if "OPENAI" in config and "API_KEY" in config["OPENAI"]:
            api_key_value = config.get('OPENAI', 'API_KEY')

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
