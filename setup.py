import pathlib
from setuptools import setup

setup(
    name='pushy-python',
    version='1.0.11',
    description='The official Pushy SDK for Python apps.',
    long_description='The official Pushy SDK for Python apps.',
    long_description_content_type='text/plain',
    url='https://github.com/pushy/pushy-python',
    author='Pushy',
    author_email='support@pushy.me',
    license='Apache 2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['pushy', 'pushy.lib', 'pushy.util'],
    install_requires=['paho-mqtt==1.6.1', 'requests', 'pathlib']
)
