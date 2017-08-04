import unittest2

from globomap_driver_napi.settings import MAP_FUNC


class TestSettings(unittest2.TestCase):

    def test_map(self):

        keys = MAP_FUNC.keys()
        expected = [
            'Equipamento',
            'NetworkIPv4',
            'NetworkIPv6',
            'ServerPool',
            'ServerPoolMember',
            'VipRequest',
            'VipRequestPortPool',
        ]

        self.assertListEqual(sorted(keys), sorted(expected))


if __name__ == '__main__':
    unittest2.main()
