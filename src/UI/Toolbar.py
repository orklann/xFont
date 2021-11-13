import gi
import math

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf

import sys
import os
# Make utils available to import from parent directory
sys.path.append(os.path.abspath('..'))
from utils import roundrect

# 31 = 30 + 1 pixels, 1 pixel for bottom border
TOOLBAR_HEIGHT = 31

class Toolbar(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect("draw", self.do_drawing);
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0

    def resize_to_fit_width(self, width):
        self.set_size_request(width, TOOLBAR_HEIGHT)

    def move(self, x, y):
        parent = self.get_parent()
        if parent is None:
            print("Error: parent of button", self, " is None")
            return
        parent.move(self, x, y)
        self.x = x
        self.y = y

    def frame(self):
        rectangle = Gdk.Rectangle()
        rectangle.x = self.x
        rectangle.y = self.y
        rectangle.width = self.width
        rectangle.height = self.height
        return rectangle

    def set_size_request(self, width, height):
        super().set_size_request(width, height)
        self.width = width
        self.height = height

    def do_drawing(self, widget, context):
        context.set_source_rgb(0.16, 0.17, 0.20)
        roundrect(context, 0, 0, self.width, self.height, 0)
        context.fill()
        #context.move_to(30, 20)
        #context.set_source_rgb(0.0, 0.0, 0.0)
        #context.set_font_size(14)
        #context.show_text("Get Glyphs")
        # Scale from 50x50 to 25x25, this works both for regular display
        # and HiDPI display
        #context.scale(0.5, 0.5)
        #Gdk.cairo_set_source_pixbuf(context, self.pixbuf, 0, 0)
        #context.paint()


