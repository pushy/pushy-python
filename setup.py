import pathlib
from setuptools import setup

setup(
    name='pushy-python',
    version='1.0.9',
    description='The official Pushy SDK for Python apps.',
    long_description=(pathlib.Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/pushy-me/pushy-python',
    author='Pushy',
    author_email='support@pushy.me',
    license='Apache 2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['pushy', 'pushy.lib', 'pushy.util'],
    install_requires=['paho-mqtt']
)