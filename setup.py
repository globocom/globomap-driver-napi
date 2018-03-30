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
from setuptools import setup

VERSION = __import__('globomap_driver_napi').__version__

setup(
    name='globomap-driver-napi',
    version=VERSION,
    description='Python library for globomap-driver to get data from '
                'GloboNetworkAPI',
    author='Ederson Brilhante',
    author_email='ederson.brilhante@corp.globo.com',
    install_requires=[
        'pika==0.10.0',
        'GloboNetworkAPI==0.8.5',
    ],
    url='https://github.com/globocom/globomap-driver-napi',
    packages=['globomap_driver_napi'],
)
