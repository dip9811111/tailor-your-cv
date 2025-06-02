import configparser
import os


api_key_value = ""
if os.path.exists("config.ini"):
    config = configparser.ConfigParser()
    config.read("config.ini")
    if "OPENAI" in config and "API_KEY" in config["OPENAI"]:
        api_key_value = config.get('OPENAI', 'API_KEY')

if not os.path.exists("output"):
    os.makedirs("output")
