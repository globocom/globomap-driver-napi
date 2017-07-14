from setuptools import setup


setup(
    name='globomap-driver-napi',
    version='0.1',
    description='Python library for globomap-driver to get data from '
                'GloboNetworkAPI',
    author='Ederson Brilhante',
    author_email='ederson.brilhante@corp.globo.com',
    install_requires=[
        'GloboNetworkAPI==0.7.2',
        'pika==0.10.0',
    ],
    url='https://github.com/globocom/globomap-loader-napi',
    packages=['globomap_driver_napi'],
)
