import configparser
import os

# When set to True, the application will use provided test files and enable a "testing environment".
# Set to False for "production" use.

TESTING = False
if TESTING:
    openai_api_key_value = "fake-api-key"
    gemini_api_key_value = "fake-api-key"
    dest_dir = "test"
else:
    dest_dir = "output"
    openai_api_key_value = ""
    gemini_api_key_value = ""
    if os.path.exists("config.ini"):
        config = configparser.ConfigParser()
        config.read("config.ini")
        if "OPENAI" in config and "API_KEY" in config["OPENAI"]:
            openai_api_key_value = config.get('OPENAI', 'API_KEY')
        if "GEMINI" in config and "API_KEY" in config["GEMINI"]:
            gemini_api_key_value = config.get('GEMINI', 'API_KEY')

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

