"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
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
