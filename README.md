# Mbed Cloud timeseries database tutorial

First add your `API_KEY` to `webapp/settings/developement.py`
Second add `id_rsa` private key file and `mbed_cloud_dev_credentials.c` file to mbed-cloud-client-example directory

```
docker-compose build
docker-compose up --scale linux_client=3
```

This will spin up 4 things:

1. 3 linux client instances, each generating a data stream
1. InfluxDB instance
1. Grafana
1. Our webapp for pushing the data stream from Mbed Cloud to InfluxDB


Grafana will be accessible at `http://localhost:3001`. The login credentials are admin, admin.
![Grafana landing page](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/master/docs/images/grafana-login.png)

You can add the Influx db data source:
* Select influxdb from dropdown
* URL: http://influxdb:8086 <--- Docker automatically handles the resolution from influxdb to its url according to its label in the docker-compose script
* DB: example
* Username: root
* Pass: root

![Grafana Dash](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/master/docs/images/grafana-data-source.png)

Finally we can add a dashboard

1. create a graph
1. select edit on graph title
1. go to metrics
1. `from default button_presses`
1. `select field(count)`
1. `group by tag(deviceId)`

![Grafana Dash](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/master/docs/images/grafana-dash.png)
