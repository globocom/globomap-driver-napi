import unittest2

from globomap_driver_napi.settings import MAP_FUNC


class TestSettings(unittest2.TestCase):

    def test_map(self):

        keys = MAP_FUNC.keys()
        expected = [
            'VipRequest',
            'VipRequestPortPool',
            'ServerPool',
            'ServerPoolMember',
            'Equipamento',
            'IpEquipamento',
            'Ipv6Equipament',
            'NetworkIPv4',
            'NetworkIPv6',
            'Vlan',
            'Environment'
        ]

        self.assertListEqual(sorted(keys), sorted(expected))
