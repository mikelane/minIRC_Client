from nose import tools
import minIRC_Client
from minIRC_Client import log
from minIRC_Client.client import Client
import asyncio
import sys

logger = log.setup_custom_logger('root.tests', level=5)

HOST = '127.0.0.1'
PORT = 10101

channels = set()
users = {}


def setup():
    loop = asyncio.get_event_loop()
    client = Client(loop, name='Admin')
    coro = loop.create_connection(lambda: client, HOST, PORT)

    try:
        logger.debug(f'Trying to establish a connection to minIRC server on host: {HOST} port: {PORT}.')
        loop.run_until_complete(coro)
    except ConnectionRefusedError:
        logger.debug(f'Connection refused. host: {HOST} port: {PORT}')
        loop.close()
        sys.exit(1)

def teardown():
    print("TEAR DOWN!")

def test_basic():
    print("I RAN!")
