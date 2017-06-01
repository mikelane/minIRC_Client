#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Short description

Long description
"""

# Imports
import curses
from minIRC_Client.client import Client
import asyncio

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"


class ChatUI:
    def __init__(self, stdscr, userlist_width=16, host='127.0.0.1', port=10101):
        loop = asyncio.get_event_loop()
        coro = loop.create_connection(lambda: Client(loop, name='Mike'), host, port)

        curses.use_default_colors()
        for i in range(curses.COLORS):
            curses.init_pair(i, i, -1)
        self.stdscr = stdscr
        self.userlist = []
        self.inputbuffer = ''
        self.linebuffer = []
        self.chatbuffer = []

        userlist_hwyx = (curses.LINES - 2, userlist_width - 1, 0, 0)
        chatbuffer_hwyx = (curses.LINES - 2, curses.COLS - userlist_width - 1, 0, userlist_width + 1)
        chatline_yx = (curses.LINES - 1, 0)
        self.win_userlist = stdscr.derwin(*userlist_hwyx)
        self.win_chatline = stdscr.derwin(*chatline_yx)
        self.win_chatbuffer = stdscr.derwin(*chatbuffer_hwyx)

        self.client = Client

        self.redraw_ui()

    def redraw_ui(self):
        h, w = self.stdscr.getmaxyx()
        u_h, u_w = self.win_userlist.getmaxyx()
        self.stdscr.clear()
        self.stdscr.vline(0, u_w + 1, '|', h - 2)

        self.redraw_userlist()
        self.redraw_chatbuffer()
        self.redraw_chatline()

    def redraw_chatline(self):
        """Redraw the user input textbox"""
        h, w = self.win_chatline.getmaxyx()
        self.win_chatline.clear()
        start = len(self.inputbuffer) - w + 1
        if start < 0:
            start = 0
        self.win_chatline.addstr(0, 0, self.inputbuffer[start:])
        self.win_chatline.refresh()

    def redraw_userlist(self):
        """Redraw the userlist"""
        self.win_userlist.clear()
        h, w = self.win_userlist.getmaxyx()
        for i, name in enumerate(self.userlist):
            if i >= h:
                break
            # name = name.ljust(w - 1) + "|"
            self.win_userlist.addstr(i, 0, name[:w - 1])
        self.win_userlist.refresh()

    def redraw_chatbuffer(self):
        """Redraw the chat message buffer"""
        self.win_chatbuffer.clear()
        h, w = self.win_chatbuffer.getmaxyx()
        j = len(self.linebuffer) - h
        if j < 0:
            j = 0
        for i in range(min(h, len(self.linebuffer))):
            self.win_chatbuffer.addstr(i, 0, self.linebuffer[j])
            j += 1
        self.win_chatbuffer.refresh()

    def wait_input(self, prompt=""):
        """
        Wait for the user to input a message and hit enter.
        Returns the message
        """
        self.inputbuffer = prompt
        self.redraw_chatline()
        self.win_chatline.cursyncup()
        last = -1
        while last != ord('\n'):
            last = self.stdscr.getch()
            if last == ord('\n'):
                tmp = self.inputbuffer
                self.inputbuffer = ""
                self.redraw_chatline()
                self.win_chatline.cursyncup()
                return tmp[len(prompt):]
            elif last == curses.KEY_BACKSPACE or last == 127:
                if len(self.inputbuffer) > len(prompt):
                    self.inputbuffer = self.inputbuffer[:-1]
            elif last == curses.KEY_RESIZE:
                self.resize()
            elif 32 <= last <= 126:
                self.inputbuffer += chr(last)
            self.redraw_chatline()
