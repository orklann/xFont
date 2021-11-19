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
from utils import roundrect, inset_rect, point_in_rect

TABVIEW_HEIGHT = 25

class TabView(Gtk.DrawingArea):
    TabviewHeight = TABVIEW_HEIGHT
    bg_color = (0.87, 0.87, 0.87)

    def __init__(self):
        super().__init__()
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect("button-press-event", self.on_button_press)
        self.connect("button-release-event", self.on_button_release)
        self.connect("draw", self.do_drawing);
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0

    def on_button_press(self, widget, event):
        coord = event.get_coords()
        x = coord[0]
        y = coord[1]
        self.queue_draw()

    def on_button_release(self, widget, event):
        pass

    def resize_to_fit_width(self, width):
        self.set_size_request(width, self.TabviewHeight)

    def move(self, x, y):
        parent = self.get_parent()
        if parent is None:
            print("Error: parent of button", self, " is None")
            return
        parent.move(self, x, y)
        self.x = x
        self.y = y

    def bounds(self):
        rectangle = Gdk.Rectangle()
        rectangle.x = 0
        rectangle.y = 0
        rectangle.width = self.width
        rectangle.height = self.height
        return rectangle

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
        context.set_source_rgb(self.bg_color[0], self.bg_color[1],
                self.bg_color[2])
        roundrect(context, 0, 0, self.width, self.height, 0)
        context.fill()
        self.draw_bottom_line(context)

    def draw_bottom_line(self, context):
        context.move_to(0, self.TabviewHeight)
        context.set_source_rgb(0.6, 0.6, 0.6)
        context.line_to(self.width, self.TabviewHeight)
        context.stroke()


