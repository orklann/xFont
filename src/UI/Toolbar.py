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

# 31 = 30 + 1 pixels, 1 pixel for bottom border
TOOLBAR_HEIGHT = 31

class Toolbar(Gtk.DrawingArea):
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
        self.tools = []
        # select tool
        select_tool = Tool()
        select_tool.set_parent(self)
        select_tool.set_image("cursor-default.png")
        select_tool.set_hl_image("cursor-default-white.png")
        self.tools.append(select_tool)
        # curve tool
        curve_tool = Tool()
        curve_tool.set_parent(self)
        curve_tool.set_image("vector-curve.png")
        curve_tool.set_hl_image("vector-curve-white.png")
        self.tools.append(curve_tool)
        # knife tool
        knife_tool = Tool()
        knife_tool.set_parent(self)
        knife_tool.set_image("knife.png")
        knife_tool.set_hl_image("knife-white.png")
        self.tools.append(knife_tool)
        # rectangle tool
        rectangle_tool = Tool()
        rectangle_tool.set_parent(self)
        rectangle_tool.set_image("rectangle.png")
        rectangle_tool.set_hl_image("rectangle-white.png")
        self.tools.append(rectangle_tool)
        # circle tool
        circle_tool = Tool()
        circle_tool.set_parent(self)
        circle_tool.set_image("circle.png")
        circle_tool.set_hl_image("circle-white.png")
        self.tools.append(circle_tool)
        # eraser tool
        eraser_tool = Tool()
        eraser_tool.set_parent(self)
        eraser_tool.set_image("eraser.png")
        eraser_tool.set_hl_image("eraser-white.png")
        self.tools.append(eraser_tool)
        # fill tool
        fill_tool = Tool()
        fill_tool.set_parent(self)
        fill_tool.set_image("alpha-a.png")
        fill_tool.set_hl_image("alpha-a-white.png")
        self.tools.append(fill_tool)
        # flip tool
        flip_tool = Tool()
        flip_tool.set_parent(self)
        flip_tool.set_image("flip.png")
        flip_tool.set_hl_image("flip-white.png")
        self.tools.append(flip_tool)
        # rotate tool
        rotate_tool = Tool()
        rotate_tool.set_parent(self)
        rotate_tool.set_image("rotate.png")
        rotate_tool.set_hl_image("rotate-white.png")
        self.tools.append(rotate_tool)
        # measure tool
        measure_tool = Tool()
        measure_tool.set_parent(self)
        measure_tool.set_image("numeric.png")
        measure_tool.set_hl_image("numeric-white.png")
        self.tools.append(measure_tool)

    def on_button_press(self, widget, event):
        coord = event.get_coords()
        x = coord[0]
        y = coord[1]
        for tool in self.tools:
            if point_in_rect(tool.get_rect(), x, y):
                tool.active_tool()
                break
        self.queue_draw()

    def on_button_release(self, widget, event):
        pass

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
        context.set_source_rgb(0.16, 0.17, 0.20)
        roundrect(context, 0, 0, self.width, self.height, 0)
        context.fill()
        context.move_to(0, TOOLBAR_HEIGHT)
        context.set_source_rgb(0.7, 0.7, 0.7)
        context.line_to(self.width, TOOLBAR_HEIGHT)
        context.stroke()
        for tool in self.tools:
            tool.draw(context)
        #context.set_font_size(14)
        #context.show_text("Get Glyphs")
        # Scale from 50x50 to 25x25, this works both for regular display
        # and HiDPI display
        #context.scale(0.5, 0.5)
        #Gdk.cairo_set_source_pixbuf(context, self.pixbuf, 0, 0)
        #context.paint()

class Tool:
    ToolWidth = 24
    ToolHeight = 24
    margin = 6
    RADIUS = 3

    def __init__(self):
        self.active = False

    def active_tool(self):
        for tool in self.toolbar.tools:
            tool.active = False
        self.active = True

    def set_parent(self, toolbar):
        self.toolbar = toolbar

    def set_image(self, image):
        path = os.path.join(os.path.abspath('src/icons'), image)
        self.image = GdkPixbuf.Pixbuf.new_from_file_at_size(path, self.ToolWidth * 2, self.ToolHeight * 2)

    def set_hl_image(self, hl_image):
        """Set highlight image, it's in white color"""
        path = os.path.join(os.path.abspath('src/icons'), hl_image)
        self.hl_image = GdkPixbuf.Pixbuf.new_from_file_at_size(path, self.ToolWidth * 2, self.ToolHeight * 2)

    def get_rect(self):
        bounds = self.toolbar.bounds()
        bounds = inset_rect(bounds, 3, 3)
        tools_count = len(self.toolbar.tools)
        tools_width = tools_count * self.ToolWidth + ((tools_count - 1) * self.margin)
        tools_rect_x = bounds.width / 2 - (tools_width / 2)
        index = self.toolbar.tools.index(self)
        x_delta = index * (self.ToolWidth + self.margin)
        x = tools_rect_x + x_delta
        y = bounds.y
        rectangle = Gdk.Rectangle()
        rectangle.x = x
        rectangle.y = y
        rectangle.width = self.ToolWidth
        rectangle.height = self.ToolHeight
        return rectangle

    def draw(self, context):
        rect = self.get_rect()
        if self.active:
            context.set_source_rgb(0.78, 0.54, 0.25)
            roundrect(context, rect.x, rect.y, rect.width, rect.height, self.RADIUS)
            context.fill()
        # Scale from 50x50 to 25x25, this works both for regular display
        # and HiDPI display
        context.scale(0.5, 0.5)
        # Muliple rect.x, rect.y by 2 because context.scale(0.5, 0.5)
        if self.active:
            Gdk.cairo_set_source_pixbuf(context, self.hl_image, rect.x * 2, rect.y * 2)
        else:
            Gdk.cairo_set_source_pixbuf(context, self.image, rect.x * 2, rect.y * 2)
        context.paint()
        context.scale(2.0, 2.0)

        #context.set_source_rgb(1.0, 1.0, 1.0)
        #roundrect(context, rect.x, rect.y, rect.width, rect.height, 0)
        #context.fill()
