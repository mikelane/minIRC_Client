#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Short description

Long description
"""

# Imports
import asyncio
import sys
import argparse
import configparser

from minIRC_Client import log
from minIRC_Client.client import Client

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"

logger = log.setup_custom_logger('root.test', level=5)

parser = argparse.ArgumentParser(description='Run a client test')
parser.add_argument(
    'name',
    type=str,
    nargs=1,
    help='Username to use for the tests. Required.'
)
parser.add_argument(
    '--local',
    help='Run using local host',
    action='store_true'
)
parser.add_argument(
    '--filetxfr',
    help='Run a file transfer test',
    action='store_true'
)

args = parser.parse_args()

if args.local:
    HOST = '127.0.0.1'
    PORT = 10101
else:
    configs = configparser.ConfigParser()
    configs.read('settings.ini')
    HOST = configs['SERVER']['HOST']
    PORT = configs['SERVER']['PORT']

channels = set()
users = {}

loop = asyncio.get_event_loop()
client = Client(loop, name=args.name[0], test=True, file_transfer_test=args.filetxfr)
coro = loop.create_connection(lambda: client, HOST, PORT)

try:
    logger.debug(f'Trying to establish a connection to minIRC server on host: {HOST} port: {PORT}.')
    loop.run_until_complete(coro)
except ConnectionRefusedError:
    logger.debug(f'Connection refused. host: {HOST} port: {PORT}')
    loop.close()
    sys.exit(1)

try:
    logger.debug('Connected to minIRC Server. Listening for data.')
    loop.run_forever()
except KeyboardInterrupt:
    logger.info('Keyboard interrupt detected. Stopping client.')
finally:
    loop.close()
