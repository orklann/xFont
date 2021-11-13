import gi
import math

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf

# 31 = 30 + 1 pixels, 1 pixel for bottom border
TOOLBAR_HEIGHT = 31

# Creating function for make roundrect shape
def roundrect(context, x, y, width, height, radius):
    context.arc(x + radius, y + radius, radius,
                math.pi, 3 * math.pi / 2)
    context.arc(x + width - radius, y + radius, radius,
                3 * math.pi / 2, 0)
    context.arc(x + width - radius, y + height - radius,
                radius, 0, math.pi / 2)
    context.arc(x + radius, y + height - radius, radius,
                math.pi / 2, math.pi)
    context.close_path()


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
        context.set_source_rgb(0.55, 0.95, 0.26)
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


