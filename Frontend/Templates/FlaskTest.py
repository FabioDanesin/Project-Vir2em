import json
import os
import re
from typing import Dict

from flask import Flask, render_template, redirect, request
import requests

separator = os.sep
templates = os.path.abspath('WebInterface/Templates')

post = "POST"
get = "GET"

app = Flask("testapp", template_folder=templates)

tabledata = [
    {
        'Name': 'Objectname',
        'Value': 123,
        'Writeable': False
    },
    {
        'Name': '2Objectname',
        'Value': 456,
        'Writeable': True
    }
]
debugdata = [templates, app]


@app.route('/')
def b():
    return datatest(tabledata)


@app.route("/<data>/post", methods=[get, post])
def datatest(data):
    json_data = json.dumps(data, indent=4)
    return json_data


@app.route("/<data>/get", methods=[get, post])
def dataget(data):
    url = f'http://{data}/post'
    unparseddata = requests.get(url)
    print("req=" + str(unparseddata))
    # unparseddata = requests.get('https://api.stackexchange.com/2.0/users?order=desc&sort=reputation&inname=fuchida&site=stackoverflow')
    json_response = json.loads(unparseddata.json())

    print(json_response)
    return json_response


@app.route("/testget")
def testget():
    return dataget("tabledata")


if __name__ == '__main__':
    app.run(debug=True)
