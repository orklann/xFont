import gi
import math

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf

from UI.toolbar import Toolbar, TOOLBAR_HEIGHT
from UI.tabview import TabView

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="xFont")
        self.resize(1024, 650)
        self.set_resizable(True)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.connect("configure-event", self.resized)
        window_size = self.get_size()
        mid_x = window_size[0] / 2.0;
        mid_y = window_size[1]/ 2.0;
        self.layout = Gtk.Layout()
        self.add(self.layout)
        self.toolbar = Toolbar()
        self.toolbar.resize_to_fit_width(window_size[0])
        self.layout.add(self.toolbar)
        self.toolbar.move(0, 0)

        self.tabview = TabView()
        self.tabview.resize_to_fit_width(window_size[0])
        self.layout.add(self.tabview)
        self.tabview.move(0, TOOLBAR_HEIGHT)
        #self.button1 = MyButton()
        #self.button1.set_size_request(130, 29)
        #self.button1.connect("motion-notify-event", self.on_button1_move)
        #self.button1.connect("button-press-event", self.on_button1_press)
        #self.button1.connect("button-release-event", self.on_button1_release)

        ##self.fixed.add(self.button1)

        ### Move button1
        #w = self.button1.width;
        #h = self.button1.height;
        #self.button1.move(mid_x - (w / 2.0), mid_y - (h / 2.0))
        #rect = self.button1.frame()
        #print(rect.x, rect.y, rect.width, rect.height)

    def layout_views(self):
        window_size = self.get_size()
        self.toolbar.resize_to_fit_width(window_size[0])
        self.tabview.resize_to_fit_width(window_size[0])

    def resized(self, widget, event):
        self.layout_views()
        return False

    def on_button1_press(self, widget, event):
        #print("Hello, with event: ", dir(event))
        print("event type: ", event.type)

    def on_button1_move(self, widget, event):
        #print("Hello, with event: ", dir(event))
        print("event type: ", event.type)


    def on_button1_release(self, widget, event):
        print("event type: ", event.type)


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

class MyButton(Gtk.DrawingArea):
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

        #1
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("/Users/rkt/projects/xFont/src/logo.png", 50, 50)
        # For super class is Gtk.Button, we need to use below code to
        # make a fix size button, for Gtk.DrawingArea, we don't need
        # this
        #self.hbox = Gtk.HBox()
        #sself.vbox = Gtk.VBox()
        #self.box = self.vbox
        #self.hbox.pack_start(self, False, False, 0)

        # Finally add hbox into vbox
        # To add this button to other layouts, we have two options:
        # 1. Add self.vbox or self.box to them
        # 2. Call self.add_to() method
        #self.vbox.pack_start(self.hbox, False, False, 0)

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
        roundrect(context, 0, 0, self.width, self.height, 5)
        context.fill()
        context.move_to(30, 20)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.set_font_size(14)
        context.show_text("Get Glyphs")
        # Scale from 50x50 to 25x25, this works both for regular display
        # and HiDPI display
        context.scale(0.5, 0.5)
        Gdk.cairo_set_source_pixbuf(context, self.pixbuf, 0, 0)
        context.paint()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
