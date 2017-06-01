#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""An Example minIRC client"""

import asyncio
import base64
import functools
import json
import os
import random
import sys

from minIRC_Client import log

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"

HOST = '127.0.0.1'
PORT = 10101

logger = log.setup_custom_logger('root.client', level=5)

example_rooms = ['test1', 'test2', 'test3', 'Main', 'Funny', 'Random', 'Music', 'Sports', 'Weather', 'News',
                 'Programming', 'Networking']


class Client(asyncio.Protocol):
    def __init__(self, loop, name, test=False, file_transfer_test=False):
        self.loop = loop
        self.name = name
        self.test = test
        self.file_transfer_test = file_transfer_test
        self.loop.add_reader(sys.stdin, self.process_input)

    def connection_made(self, transport):
        try:
            self.transport = transport
            self.peername = transport.get_extra_info('peername')
            logger.debug(f'{self.peername}: Connection established.')

            self.loop.call_soon(self.login)

            if self.test:
                if self.name == 'Admin':
                    logger.debug('Setting up Admin rooms')
                    self.loop.call_later(0.1, self.create_channel, 'test1')
                    self.loop.call_later(0.2, self.create_channel, 'test2')
                    self.loop.call_later(0.3, self.create_channel, 'test3')
                    logger.debug('Setting up the server to KICK user Mike')
                    self.loop.call_later(15, functools.partial(self.send_message, NICKS='Mike',
                                                               MESSAGE='Testing ability to kick!'), 'KICK')
                else:
                    logger.debug('Running tests as non-Admin')
                    self.run_tests()
                    self.loop.call_later(30, self.quit)


        except KeyboardInterrupt:
            logger.debug('KeyboardInterrupt detected. Calling QUIT')
            self.quit()

    def run_tests(self):
        for i in range(3):
            room = random.choice(example_rooms)
            self.loop.call_soon(self.join_channels, 'test1')
            self.loop.call_later(i + 2, functools.partial(self.send_message, MESSAGE=f'Test {i}', CHANNELS='test1'),
                                 'SENDMSG')
            self.loop.call_later(random.uniform(0, 10), self.create_channel, room)
            self.loop.call_later(random.uniform(0, 10), self.list_channels)
            self.loop.call_soon(functools.partial(self.send_message, MESSAGE=f'Hello, Admin {i}', USERS=['Admin']),
                                'SENDMSG')
        self.loop.call_later(random.uniform(5, 15), self.list_channels, '^M.*$')

        for i in range(3):
            room = random.choice(example_rooms)
            self.loop.call_later(random.uniform(0, 10), self.join_channels, room)

        self.loop.call_later(random.uniform(0, 10), self.join_channels, example_rooms[2:5])

    def process_input(self):
        text = sys.stdin.readline()
        data = text.strip()
        logger.debug(f'Received from stdin: "{data}"')

    def make_message(self, command, kwargs):
        if not kwargs:
            kwargs = None
        return f'{json.dumps({command: kwargs})}\n'.encode()

    def send_message(self, command, **kwargs):
        message = self.make_message(command, kwargs)
        self.loop.call_soon(self.transport.write, message)

    def login(self):
        logger.debug(f'Attempting to login with name {self.name}')
        self.send_message('LOGIN', NICK=self.name)

    def create_channel(self, name):
        logger.debug(f'Attempting to create channel {name}')
        self.send_message('CREATECHAN', NAME=name)

    def list_channels(self, regex_string=None):
        logger.debug(f'Attempting to list channels with regex {regex_string}')
        self.send_message('LIST', FILTER=regex_string)

    def join_channels(self, channels):
        logger.debug(f'Attempting to join channels {channels}')
        if type(channels) == str:
            channels = [channels]
        self.send_message('JOIN', CHANNELS=channels)

    def send_file(self, recv_username):
        self.send_message('SENDFILE', )

    def quit(self):
        logger.debug('Attempting to quit')
        self.send_message('QUIT')

    # async def file_transfer_client(self, host, port, filename):
    #     reader, writer = await asyncio.open_connection(host=host, port=port, loop=self.loop)
    #
    #     logger.debug(f'Handshake. Sending {filename}')
    #     writer.write(filename.encode())
    #     await writer.drain()
    #
    #     logger.debug('Waiting for response OK')
    #     resp = await reader.read(2)
    #     if resp.decode() != 'OK':
    #         logger.debug(f'Error during file transfer handshake. Expected OK. Received {resp}')
    #         return False
    #
    #     with open(filename, 'rb') as f:
    #         logger.debug('Sending the file')
    #         writer.write(f)
    #         await writer.drain()
    #
    # async def file_receive_client(self, host, port):
    #     reader, writer = await asyncio.open_connection(host=host, port=port, loop=self.loop)
    #
    #     logger.debug(f'Handshake. Expecting filename')
    #     filename = await reader.read()
    #
    #     logger.debug(f'Received {filename}. Responding with OK.')
    #     writer.write(b'OK')
    #     await writer.drain()
    #
    #     logger.debug('Awaiting data...')
    #     data = await reader.read()
    #
    #     local_download_dir = f'~/minIRC-Test-Download/{self.name}'
    #
    #     logger.debug(f'Writing data to {local_download_dir}/{filename}')
    #     os.makedirs(local_download_dir, exist_ok=True)
    #     with open(f'{local_download_dir}/{filename}', 'wb') as f:
    #         f.write(data)

    def data_received(self, data):
        messages = data.strip().decode().split('\n')
        for message in messages:
            if message == '{"PING": null}':
                self.transport.write(b'{"PING": "PONG"}\n')
                logger.debug(f'{self.peername}: Received PING, replied with PONG')
            else:
                logger.debug(f'{self.peername}: Message received: {message}')
                # TODO get this working
                # if 'RECVFILE' in message:
                #     # {'RECVFILE': {'HOST': '127.0.0.1', 'PORT': 1234}}
                #     data = json.loads(message)
                #     host = data['RECVFILE']['HOST']
                #     port = data['RECVFILE']['PORT']
                #     self.loop.run_until_complete(self.file_receive_client(host=host, port=port))



    def connection_lost(self, exc):
        logger.debug('The server closed the connection')
        logger.debug('Stop the event loop')
        self.loop.stop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: Client(loop, name='Socrates'), HOST, PORT)

    try:
        loop.run_until_complete(coro)
    except ConnectionRefusedError:
        logger.debug(f'Connection refused. host: {HOST} port: {PORT}')
        loop.close()
        sys.exit(1)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt detected. Stopping client.')
    finally:
        loop.close()
