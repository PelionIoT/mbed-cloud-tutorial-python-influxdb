# Mbed Cloud Time-series Database Tutorial

## Introduction
A retail chain wants more insight in how product placement correlates to customer interaction. 
Each shelf tracks how many items it contains, and should send this information to a server every time an item is added or removed.
Note: The retailer does not care about how many products are sold to customers as this is trivially found from checkout systems. 
Instead they want metrics on how much customers interact with products in stores before deciding to purchase or return an item to the shelves.
![Shopping](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/cola/docs/images/shopping.png)

## Structuring the workflow

### Scoping
For now, lets assume the data streams are readily available from cloud. In other words, there exist some devices connected to Mbed Cloud that provide the following in addition to the standard LWM2M objects:

* Product ID    (String) example, "Cheese", "Apples", "Beer", "Bread", "Milk"
* Product count (integer)

It is important to note that multiple shelves can share the same product ID so we need to capture this in our final metric through some aggregation stage.
Obviously, we want to keep track of the product counts for each product ID over time so we should probably store these readings in a time series database.
Additionally, we need to present these readings in a meaningful way to the analysts through some form of visualization.
Here we arbitrarily pick InfluxDB for storing our time series values and Grafana for visualization, but we could have chosen from any combination of time series databases and visualization platforms.
The third, and final, piece we need is a custom proxy application to take the data streams from Mbed Cloud and push them into the time series database.


![Platform overview](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/cola/docs/images/cola-overview.png)

### Capturing the structure in microservices

Microservice architectures are modular applications where subcomponents are built up as loosely coupled, and reusable, services. Given a standard interface, for example, the same description for a SQL database microservice can be used in just about any application. Furthermore microservice architectures benefit additionally from straightforward deployment scenarios and controllable service scaling. 

Docker is one of many solutions for building microservice based applications. Microservices themselves are described using `Dockerfile`s, which include information such as how to build and run a specific service, and what ports are needed to connect to it. This application has two `Dockerfile`s, one for the proxy web application and one for a locallinux client found in `webapp/Dockerfile` and `mbed-cloud-client-example/Dockerfile` respectively. 
Docker captures application structure in `docker-compose.yml` files, which declare which microservices are needed in an application and how to connect them. For example, we can directly map the Platform Overview Diagram from the `Scoping` section to a Docker application with the following compose script:

```
version: "3"

services:
    linux_client:
        build: mbed-cloud-client-example

    app:
        build: webapp
        ports:
            - "3000:8080"
        volumes:
            - ./webapp:/usr/src/app
        links:
            - influxdb
            - linux_client
        environment:
            - ENV=development

    # We can refer to the influxdb url with http://influxdb:8086
    influxdb:
        image: influxdb:1.4-alpine
        expose:
            - "8086"

    grafana:
        image: grafana/grafana
        ports:
            - "3001:3000"
        links:
            - influxdb
```

This file declares 4 services: a proxy web app, InfluxDB, Grafana, and an mbed Cloud Client Linux example. For InfluxDB and Grafana, we specify which images to grab from DockerHub. Note the project structure is evident in the `links` keyword. For example, the `app` service depends on both the `influxdb` service and `linux_client` service. Likewise, the `grafana` service pulls data from the `influxdb` service. Finally, the `grafana` service is visible on port 3001.

### Writing a proxy sampling application based on subscriptions

```python
# Subscribe to all devices at runtime
def Initialize():
    for each device in connected_devices():
        if has_product_count_resource(device):
            add_resource_subscription(device, PRODUCT_COUNT_PATH, product_count_callback)

# Push current value and product_id to the database
def product_count_callback(device_id, path, current_value):
    TimeSeriesDatabase.push((device_id, current_value, get_product_id(device_id)))
```

## Setup and run

1. Add your Mbed Cloud `API_KEY` to `webapp/settings/development.py`.
1. Add your `id_rsa` and `mbed_cloud_dev_credentials.c` file to the mbed-cloud-client-example directory. [Generate id_rsa](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#platform-windows) and be sure to add it to Github. You can get `mbed_cloud_dev_credentials.c` from the cloud portal. *NOTE*: please make sure `id_rsa` is not password protected.

1. Now run the following:

```
docker-compose build
docker-compose up --scale linux_client=3
```

This will spin up 4 items:

1. 3 linux client instances, each generating a data stream
1. InfluxDB instance
1. Grafana
1. The web application for pushing the data stream from Mbed Cloud to InfluxDB


Grafana will be accessible at `http://localhost:3001`. The login credentials are admin, admin.
![Grafana landing page](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/master/docs/images/grafana-login.png)

You can add the Influx db data source:
* Select InfluxDB from dropdown
* URL: http://influxdb:8086 <--- Docker automatically handles the resolution from InfluxDB to its url according to its label in the docker-compose script
* DB: example
* Username: root
* Pass: root

![Grafana Dash](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/master/docs/images/grafana-data-source.png)

Finally we can add a dashboard

1. Create a graph
1. Select edit on graph title
1. Go to metrics and add the following:
  - FROM: `default product_count`
  - SELECT: `field(count) count() non_negative_difference()`
  - GROUP BY: `time(1s) tag(product_id) fill(previous)`
  - ALIAS BY: `$tag_product_id`

This metric roughly translates as follows: First count the number of interactions with a product (product taken, product returned) during a 1 second interval. This can be thought of as the magnitude of the product activity, which is useful in understanding how much activity a particular shelf has. However, additionally computing the non-negative difference between these magnitudes yields insight into how consistent these magnitudes are and roughly translates to the *velocity* of product activity on a shelf. 

![Grafana Dash](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/cola/docs/images/grafana-cola.png)

## Discussion

## References

* [Mbed Cloud](https://cloud.mbed.com/docs/v1.2/introduction/index.html)
* [InluxDB](https://www.influxdata.com/time-series-platform/influxdb/)
* [Grafana](https://grafana.com/)
