from setuptools import setup

VERSION = __import__('globomap_driver_napi').VERSION

setup(
    name='globomap-driver-napi',
    version=VERSION,
    description='Python library for globomap-driver to get data from '
                'GloboNetworkAPI',
    author='Ederson Brilhante',
    author_email='ederson.brilhante@corp.globo.com',
    install_requires=[
        'pika==0.10.0',
        'GloboNetworkAPI==0.7.2',
    ],
    url='https://github.com/globocom/globomap-driver-napi',
    packages=['globomap_driver_napi'],
)
