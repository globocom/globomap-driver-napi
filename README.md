# globomap-driver-napi
Python library for globomap-driver-napi to get data from GloboNetworkAPI/RabbitMQ of GloboNetworkAPI

## Plugin environment variables configuration
All of the environment variables below must be set for the plugin to work properly.

| Variable                       |  Description                 | Example                                    |
|--------------------------------|------------------------------|--------------------------------------------|
| NETWORKAPI_ENDPOINT            | Network API URL              | http://networkapi.domain.com:8080          |
| NETWORKAPI_USER                | Network user                 | user                                       |
| NETWORKAPI_PASSWORD            | Network password             | password                                   |
| GLOBOMAP_LOADER_API_URL        | GloboMap Loader API endpoint | http://api.globomap.loader.domain.com:8080 |
| GLOBOMAP_LOADER_API_USER       | GloboMap Loader API user     | user                                       |
| GLOBOMAP_LOADER_API_PASSWORD   | GloboMap Loader API password | password                                   |
| NETWORKAPI_RMQ_HOST            | RabbitMQ host                | rabbitmq.yourdomain.com                    |
| NETWORKAPI_RMQ_PORT            | RabbitMQ port                | 5672 (default)                             |
| NETWORKAPI_RMQ_USER            | RabbitMQ user                | user-name                                  |
| NETWORKAPI_RMQ_PASSWORD        | RabbitMQ password            | password                                   |
| NETWORKAPI_RMQ_VIRTUAL_HOST    | RabbitMQ virtual host        | /networkapi                                |
| NETWORKAPI_RMQ_QUEUE           | RabbitMQ queue name          | networkapi-updates                         |
| SENTRY_DSN                     | Destination Sentry server.   | https://user:password@sentry.io/test       |
| SCHEDULER_FREQUENCY_EXEC       | Frequency of execution       | 0-23                                       |
| ZBX_PASSIVE_MONITOR_SCHEDULER  | Zabbix monitor               | passive_abc_monitor_scheduler              |


### Environment variables configuration from external libs
All of the environment variables below must be set for the application to work properly.

[globomap-monitoring](https://github.com/globocom/globomap-monitoring)

## Example of use

```python
from globomap_driver_napi.driver import Napi
driver = Napi()
driver.process_updates(print)
```

## Example of implementation
[Examples](https://github.com/globocom/globomap-driver-napi/tree/master/doc/examples)
