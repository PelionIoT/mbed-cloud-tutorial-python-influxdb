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
import sys
import logging
import time
import threading


from datetime import datetime
from importlib import import_module
from influxdb import InfluxDBClient

from os import environ

from flask import Flask

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

# Note we don't use flask in our web app but you could easily build something
# with this framework
app = Flask(__name__)

# Get settings
settings = import_module("settings." + environ["ENV"])
app.config.from_object(settings.Config)

# Override params with CLI inputs
if args.api_key_val:
    app.config["API_KEY"] = args.api_key_val

if args.host_val:
    app.config["API_HOST"] = args.host_val


WEBHOOK_URL = "%s/api/webhook" % app.config["API_BASE_URL"]
PRODUCT_ID_PATH = "/10341/0/26341"
PRODUCT_CURR_COUNT_PATH = "/10341/0/26342"

# Instatiate cloud connect
api_config = {"api_key": app.config["API_KEY"], "host": app.config["API_HOST"]}
connectApi = ConnectAPI(api_config)
# This should be required, why is it breaking things
connectApi.start_notifications()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Instantiate the database client on Table named 'example'
# Set the username and password to root
db = InfluxDBClient("influxdb",
                    app.config["INFLUX_PORT"],
                    'root', 'root', 'example')

id_num_db = {}

def get_async(device_id, resource_path):
    while True:
        async_resp = connectApi.get_resource_value_async(
                device_id, resource_path)

        # Busy wait - block the thread and wait for the response to finish.
        while not async_resp.is_done:
            time.sleep(0.1)

        # Check if we have a async error response, and abort if it is.
        if async_resp.error:
            raise Exception("Got async error response: %r" % async_resp.error)

        # Get the value from the async response, as we know it's done
        return async_resp.value

def get_async_time(device_id, resource_path, timeout=0):
    deferred = connectApi.get_resource_value_async(device_id, resource_path)
    return deferred.wait(timeout)


def handleSubscribe(device_id, path, current_value):
    """On change in subscribed resource, dump data to InfluxDB."""
    logging.error("HERE %s" % device_id)
    now = datetime.utcnow()
    id_num = id_num_db[device_id]
    logging.error("DONE GETTING VALUE %s %s" % (device_id, id_num))

    json_body = [
        {
            "measurement": "product_count",
            "tags": {
                "deviceId": device_id,
                "resource": path,
                "product_id": id_num
                },
            "time": now,
            "fields": {
                "count": current_value
            }
        }
    ]

    logging.error("Writing to DB")
    db.write_points(json_body)


def subscribe_to_all():
    """Find all devices with button resources and subscribe to them."""
    time.sleep(5)
    logging.warning("Looking for devices")
    print("Looking for devices")
    for device in connectApi.list_connected_devices(order='desc'):
        resources = []
        try:
            # check if accessible
            connectApi.get_resource_value(device.id,
                                          "/3/0/2",
                                          timeout=5)
            resources = connectApi.list_resources(device.id)
        except:
            logging.warning("Failed to get resources for %s, likely offline" % device.id)
            continue
        for resource in resources:
            if PRODUCT_CURR_COUNT_PATH == resource.path:
                # Actually handle the subscription
                logging.warning("Found device %s" % device.id)
                id_num_db[device.id] = connectApi.get_resource_value(device.id, PRODUCT_ID_PATH, timeout=5)
                connectApi.add_resource_subscription_async(device.id,
                                                           PRODUCT_CURR_COUNT_PATH,
                                                           handleSubscribe)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.info('Web app listening at %s:%s' % (app.config["API_BASE_URL"], app.config["PORT"]))
    logging.getLogger().setLevel(logging.WARNING)

    db.create_database('example')

    #t = threading.Thread(target=subscribe_to_all)
    #t.start()
    subscribe_to_all()

    while True:
        continue
