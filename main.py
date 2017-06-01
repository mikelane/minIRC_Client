#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Short description

Long description
"""

# Imports
import wx

__author__ = "Michael Lane"
__email__ = "mikelane@gmail.com"
__copyright__ = "Copyright 2017, Michael Lane"
__license__ = "MIT"

class MyApp(wx.App):
    def OnInit(self):
        wx.MessageBox("Hello wxPython", "wxApp")
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()

