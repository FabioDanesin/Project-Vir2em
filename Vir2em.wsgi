#! /usr/bin/python3.6

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/username/ExampleFlask/')
from Frontend.MainPage import app as application
application.secret_key = 'anything you wish'
