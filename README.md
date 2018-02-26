# Mbed Cloud Time-series Database Tutorial

## Introduction
A retail chain wants more insight in how product placement correlates to customer interaction. 
Each shelf tracks how many items it contains, and should send this information to a server every time an item is added or removed.
Note: The retailer does not care about how many products are sold to customers as this is trivially found from checkout systems. 
Instead they want metrics on how much customers interact with products in stores before deciding to purchase or return an item to the shelves.
![Shopping](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/cola/docs/images/shopping.png)

## Structuring the workflow

### Scoping

### Capturing the structure in Docker

### High level overview of the proxy sampling application

## Setup and run

1. Add your Mbed Cloud `API_KEY` to `webapp/settings/development.py`.
1. Add your `id_rsa` and `mbed_cloud_dev_credentials.c` file to the mbed-cloud-client-example directory
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
  - ALIAS BY: `Product $tag_product_id`

This metric roughly translates as follows: First count the number of interactions with a product (product taken, product returned) during a 1 second interval. This can be thought of as the magnitude of the product activity, which is useful in understanding how much activity a particular shelf has. However, additionally computing the non-negative difference between these magnitudes yields insight into how consistent these magnitudes are and roughly translates to the *velocity* of product activity on a shelf. 

![Grafana Dash](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/cola/docs/images/grafana-cola.png)
