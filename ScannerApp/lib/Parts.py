# tkinter GUI library
import tkinter as tk

# date time library used for clock and time durations
from datetime import datetime, timedelta

# Config global variables
from lib import Config

class Parts():
    
    root_frame = None
    parent_frame = None

    def __init__(self, root, master):

        self.root_frame = root
        self.parent_frame = master

    def parts_list(self, frame):
        #
        # Fetches and displays a list of the parts
        #

        self.parent_frame = frame

        # set the scanning mode to default
        Config.scanning_mode = 0


        return

    def process_barcode(self, barcode, frame=None):

        if (frame != None):
            self.parent_frame = frame

        return
