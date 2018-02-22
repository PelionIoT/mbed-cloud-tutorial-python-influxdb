# Mbed Cloud Time-series Database Tutorial

## Setup

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
  - FROM: `default button_presses`
  - SELECT: `field(count)`
  - GROUP: `tag(deviceId)`

![Grafana Dash](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/master/docs/images/grafana-dash.png)
