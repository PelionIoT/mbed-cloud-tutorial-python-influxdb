# Copyright ARM Limited 2017
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import sys
import logging
import os
import time
import threading


from datetime import datetime
from importlib import import_module
from influxdb import InfluxDBClient

from os import environ

from flask import Flask
from flask import request
from flask import Response

from flask_socketio import SocketIO
from mbed_cloud.connect import ConnectAPI

# Allow for command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--apiKey",
                    help="Provide an api key directly",
                    action="store", dest="api_key_val")
parser.add_argument("--host",
                    help="Specify the host Mbed Cloud instance to connect to.",
                    action="store", dest="host_val")

args = parser.parse_args()

# Use 'threading' async_mode, as we don't use greenlet threads for background
# threads in SDK - and thus we can't use eventlet or gevent.
async_mode = 'threading'

app = Flask(__name__)

# Get settings
settings = import_module("settings." + environ["ENV"])
app.config.from_object(settings.Config)

#socket = SocketIO(app, async_mode=async_mode, logger=False, engineio_logger=False)

# Override params with CLI inputs

if args.api_key_val:
    app.config["API_KEY"] = args.api_key_val

if args.host_val:
    app.config["API_HOST"] = args.host_val


WEBHOOK_URL = "%s/api/webhook" % app.config["API_BASE_URL"]
BUTTON_RESOURCE_PATH = "/3200/0/5501"

# Instatiate cloud connect
api_config = {"api_key": app.config["API_KEY"], "host": app.config["API_HOST"]}
connectApi = ConnectAPI(api_config)
# This should be required, why is it breaking things
connectApi.start_notifications()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Instantiate the database client
db = InfluxDBClient("influxdb", app.config["INFLUX_PORT"], 'root', 'root', 'example')

def handle_device_webhook(data):
    # find all data samples in notification queue

    # put data in influxdb

    if r.ok == False:
        logging.error("LOG FAIL", r.status_code,  data)

@app.route('/handle_webhook', methods=['PUT'])
def device_webhook():
    """If a new device gets added make sure a subscription 
    is added to eagle owl.
    """
    data = json.loads(request.data)
    handle_device_webhook(data)

    # It's ok to drop samples
    # Cloud expects a return code of 200, else it will Queue up all the samples
    return Response(status=200)

def handleSubscribe(device_id, path, current_value):
    logging.warning("GOT THING")
    json_body = [
    {
        "measurement": "button_presses",
        "tags": {
            "deviceId": device_id,
            "resource": path
        },
        "time": datetime.utcnow(),
        "fields": {
            "count": current_value
        }
    }
    ]

    db.write_points(json_body)

def subscribe_to_all():
    time.sleep(2)
    logging.warning("Looking for devices")
    print("Looking for devices")
    for device in connectApi.list_connected_devices():
        try:
            resources = connectApi.list_resources(device.id)
            for resource in resources:
                if BUTTON_RESOURCE_PATH == resource.path:
                    # Actually handle the subscription
                    logging.warning("Found device %s" % device.id)
                    connectApi.add_resource_subscription_async(device.id, BUTTON_RESOURCE_PATH, handleSubscribe)

                    # Go ahead and store current value
                    handleSubscribe(device.id, resource.path, connectApi.get_resource_value(device.id, resource.path))

        except:
            logging.warning("Failed to get resources for %s, likely offline" % device.id)

if __name__ == "__main__":

    logging.getLogger().setLevel(logging.INFO)
    logging.info('Web app listening at %s:%s' % (app.config["API_BASE_URL"], app.config["PORT"]))
    logging.getLogger().setLevel(logging.WARNING)

    db.create_database('example')

    t = threading.Thread(target=subscribe_to_all)
    t.start()

    while True:
        pass
    #socket.run(app, host='0.0.0.0', port=app.config["PORT"])
