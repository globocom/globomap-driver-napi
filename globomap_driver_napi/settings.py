
import os

NETWORKAPI_ENDPOINT = os.getenv('NETWORKAPI_ENDPOINT')
NETWORKAPI_USER = os.getenv('NETWORKAPI_USER')
NETWORKAPI_PASSWORD = os.getenv('NETWORKAPI_PASSWORD')
NETWORKAPI_RMQ_USER = os.getenv('NETWORKAPI_RMQ_USER')
NETWORKAPI_RMQ_PASSWORD = os.getenv('NETWORKAPI_RMQ_PASSWORD')
NETWORKAPI_RMQ_HOST = os.getenv('NETWORKAPI_RMQ_HOST')
NETWORKAPI_RMQ_PORT = int(os.getenv('NETWORKAPI_RMQ_PORT', 5672))
NETWORKAPI_RMQ_VIRTUAL_HOST = os.getenv('NETWORKAPI_RMQ_VIRTUAL_HOST')
NETWORKAPI_RMQ_QUEUE = os.getenv('NETWORKAPI_RMQ_QUEUE')
GLOBOMAP_LOADER_ENDPOINT = os.getenv('GLOBOMAP_LOADER_ENDPOINT')

MAP_FUNC = {
    'VipRequest': [
        {
            'name': 'vip',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'vip',
            'provider': 'napi',
            'type': 'collections'
        }
    ],
    # TODO: Method vip_port to changes in port
    # 'VipRequestPort': [
    #     {
    #         'name': 'vip',
    #         'package': 'globomap_driver_napi.kind',
    #         'class': 'Kind',
    #         'method': 'vip_port',
    #         'provider': 'napi',
    #         'type': 'collections'
    #     }
    # ],
    'VipRequestPortPool': [
        {
            'name': 'port',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'port',
            'provider': 'napi',
            'type': 'edges'
        }
    ],
    'ServerPool': [
        {
            'name': 'pool',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'pool',
            'provider': 'napi',
            'type': 'collections'
        }
    ],
    'ServerPoolMember': [
        {
            'name': 'pool_comp_unit',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'pool_comp_unit',
            'provider': 'napi',
            'type': 'edges'
        }
    ],
    'Equipamento': [
        {
            'name': 'comp_unit',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'comp_unit',
            'provider': 'globomap',
            'type': 'collections'
        }
    ],
    'IpEquipamento': [
        {
            'name': 'network_comp_unit',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'network_v4_comp_unit',
            'provider': 'napi',
            'type': 'edges'
        }
    ],
    'Ipv6Equipament': [
        {
            'name': 'network_comp_unit',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'network_v6_comp_unit',
            'provider': 'napi',
            'type': 'edges'
        }
    ],
    'NetworkIPv4': [
        {
            'name': 'network',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'network_v4',
            'provider': 'napi',
            'type': 'collections'
        },
        {
            'name': 'vlan_network',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'vlan_network_v4',
            'provider': 'napi',
            'type': 'edges'
        }
    ],
    'NetworkIPv6': [
        {
            'name': 'network',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'network_v6',
            'provider': 'napi',
            'type': 'collections'
        },
        {
            'name': 'vlan_network',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'vlan_network_v6',
            'provider': 'napi',
            'type': 'edges'
        }
    ],
    'Vlan': [
        {
            'name': 'vlan',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'vlan',
            'provider': 'napi',
            'type': 'collections'
        },
        {
            'name': 'environment_vlan',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'environment_vlan',
            'provider': 'napi',
            'type': 'edges'
        }
    ],
    'Environment': [
        {
            'name': 'environment',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'environment',
            'provider': 'napi',
            'type': 'collections'
        },
        {
            'name': 'father_environment',
            'package': 'globomap_driver_napi.kind',
            'class': 'Kind',
            'method': 'father_environment',
            'provider': 'napi',
            'type': 'edges'
        }
    ],
}

ACTIONS = {
    'Alterar': 'UPDATE',
    'Cadastrar': 'CREATE',
    'Remover': 'DELETE'
}
