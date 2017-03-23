from setuptools import setup

setup(
    name='icdb',
    description='The Internet Movie DataBase',
    version='0.0.1',
    packages=['icdb', 'Movies'],
    install_requires=[
        'django==1.4.18',
        'nose',
        'mock',
    ]
)
