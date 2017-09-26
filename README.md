# globomap-driver-napi
Python library for globomap-core-loader to get data from GloboNetworkAPI

## Plugin environment variables configuration
All of the environment variables below must be set for the plugin to work properly.

| Variable                    |  Description            | Example                             |
|-----------------------------|-------------------------|-------------------------------------|
| NETWORKAPI_ENDPOINT         | Network API URL         | http://networkapi.domain.com:8080   |
| NETWORKAPI_USER             | Network user            | user                                |
| NETWORKAPI_PASSWORD         | Network password        | password                            |
| NETWORKAPI_RMQ_HOST         | RabbitMQ host           | rabbitmq.yourdomain.com             |
| NETWORKAPI_RMQ_PORT         | RabbitMQ port           | 5672 (default)                      |
| NETWORKAPI_RMQ_USER         | RabbitMQ user           | user-name                           |
| NETWORKAPI_RMQ_PASSWORD     | RabbitMQ password       | password                            |
| NETWORKAPI_RMQ_VIRTUAL_HOST | RabbitMQ virtual host   | /networkapi                         |
| NETWORKAPI_RMQ_QUEUE        | RabbitMQ queue name     | networkapi-updates                  |

## Example of use

```python
from globomap_driver_napi.driver import Napi
driver = Napi()
driver.updates()
```

## Example of implementation
[Examples](https://github.com/globocom/globomap-driver-napi/doc/examples)
