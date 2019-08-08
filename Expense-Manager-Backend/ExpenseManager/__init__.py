#create app context and configure it

from sys import exit
from json import load
from flask import Flask

#loading config.json file
config = None
try:
    with open('config.json') as _config:
        config = load(_config)
except Exception as e:
    print(e)
    exit('Error loading config.json. Make sure that it is present in root folder and is in proper format')

app = Flask(__name__)

app.config['SECRET_KEY'] = config['app_secret_key']
