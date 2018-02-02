# Mbed Cloud timeseries database tutorial

First add your `API_KEY` to `webapp/settings/developement.py`
Second add `id_rsa.pub` and `mbed_cloud_dev_credentials.c` file to mbed-cloud-client-example directory

```
docker-compose build
docker-compose up
```

This will spin up 4 things:

1. A linux client which generates a data stream
1. InfluxDB instance
1. Grafana
1. Our webapp for pushing the data stream from Mbed Cloud to InfluxDB


Grafana will be accessible at `http://localhost:3001`. The login credentials are admin, admin.
![Grafana landing page](https://github.com/ARMmbed/mbed-cloud-tutorial-python-influxdb/blob/master/docs/images/grafana-login.png)
