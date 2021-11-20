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
        self.tabs = []
        ft = Tab()
        ft.set_parent(self)
        ft.set_title('A')
        self.tabs.append(ft)
        st = Tab()
        st.set_parent(self)
        st.set_title('B')
        self.tabs.append(st)
        st.active = True
        tt = Tab()
        tt.set_parent(self)
        tt.set_title('C')
        self.tabs.append(tt)

    def on_button_press(self, widget, event):
        coord = event.get_coords()
        x = coord[0]
        y = coord[1]
        for tab in self.tabs:
            if point_in_rect(tab.get_rect(), x, y):
                tab.active_tab()
                break
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
        for tab in self.tabs:
            tab.draw(context)

    def draw_bottom_line(self, context):
        context.move_to(0, self.TabviewHeight - 1)
        context.set_source_rgb(0.6, 0.6, 0.6)
        context.line_to(self.width, self.TabviewHeight - 1)
        context.set_line_width(2.0)
        context.stroke()


class Tab:
    TabbarHeight = TABVIEW_HEIGHT
    TabWidth = 100
    LeftPadding = 10
    RightPadding = 14
    DeltaXForTabs = 2
    DeltaYForTabs = 3
    RADIUS = 4
    FontSize = 11

    def __init__(self):
        self.width = self.TabWidth
        self.active = False
        self.highlight = False
        self.can_closed = True
        self.is_main_tab = False
        self.active_bg_color = (1.0, 1.0, 1.0)
        self.normal_bg_color = (0.71, 0.71, 0.71)

    def set_parent(self, parent):
        self.tabview = parent

    def set_title(self, title):
        self.title = title

    def active_tab(self):
        for tab in self.tabview.tabs:
            tab.active = False
        self.active = True

    def draw(self, context):
        if self.active:
            self.draw_active(context)
        else:
            self.draw_inactive(context)
        self.draw_title(context)

    def draw_title(self, context):
        rect = self.get_rect()
        if self.active:
            pass
        else:
            pass
        # Title text
        # Todo: Implement self.get_short_title() method
        short_title = self.title#self.get_short_title()
        text_extents = context.text_extents(short_title)
        title_rect = inset_rect(rect, 8, 3)
        x = (title_rect.x + title_rect.width / 2) - (text_extents.width / 2)
        y = (title_rect.y + title_rect.height /2) + (text_extents.height / 2)
        context.move_to(x, y)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.set_font_size(self.FontSize)
        context.show_text(short_title)
        context.new_path() # clear path for next tab drawing

    def draw_active(self, context):
        rect = self.get_rect()
        mid_x = rect.x + (rect.width / 2)
        mid_y = rect.y + (rect.height / 2)
        min_x = rect.x
        min_y = rect.y
        max_x = rect.x + rect.width

        # -0.5 to feed graphic stroke API for perfect line width
        # noborder_min_y feed fill API for whole fill
        max_y = rect.y + rect.height
        noborder_min_y = rect.y + 1.5

        # Substract min_x by DeltaXForTabs
        # Restore min_x to original value at the end
        # We do this to min_x, max_x for drawing active tab more
        # closing to normal tabs
        MIN_X = min_x
        min_x = MIN_X - self.DeltaXForTabs

        # Add max_x by DeltaXForTabs
        # Restore max_x to original value at the end
        MAX_X = max_x
        max_x = MAX_X + self.DeltaXForTabs

        # Substract min_y, restore to origin at the end
        MIN_Y = min_y
        min_y = MIN_Y + 1

        # Move minY lower by 1px to fill whole tab
        minY = 0
        radius = self.RADIUS
        #
        # Fill path
        #
        # bottom left arc
        context.arc_negative(min_x, max_y - radius, radius, math.pi / 2, 0)
        # top left arc
        context.arc(min_x + 2 * radius, min_y + radius, radius,
                math.pi, 3 * math.pi / 2)
        # top right arc
        context.arc(max_x - 2 * radius, min_y + radius, radius,
                3 * math.pi / 2, 0)
        # bottom right arc
        context.arc_negative(max_x, max_y - radius, radius,
                math.pi, math.pi / 2)
        context.set_source_rgb(self.active_bg_color[0],
                self.active_bg_color[1],
                self.active_bg_color[2])
        context.fill()
        #
        # Stroke the same path
        #
        # bottom left arc
        context.arc_negative(min_x, max_y - radius, radius, math.pi / 2, 0)
        # top left arc
        context.arc(min_x + 2 * radius, min_y + radius, radius,
                math.pi, 3 * math.pi / 2)
        # top right arc
        context.arc(max_x - 2 * radius, min_y + radius, radius,
                3 * math.pi / 2, 0)
        # bottom right arc
        context.arc_negative(max_x, max_y - radius, radius,
                math.pi, math.pi / 2)
        context.set_source_rgb(0.60, 0.60, 0.60)
        context.set_line_width(2.0)
        context.stroke()

    def draw_inactive(self, context):
        rect = self.get_rect()
        mid_x = rect.x + (rect.width / 2)
        mid_y = rect.y + (rect.height / 2)
        min_x = rect.x
        min_y = rect.y
        max_x = rect.x + rect.width

        # -0.5 to feed graphic stroke API for perfect line width
        # noborderMaxY feed fill API for whole fill
        max_y = rect.y + rect.height
        noborder_min_y = rect.y# + 1.5

        # Substract min_x by DeltaXForTabs
        # Restore min_x to original value at the end
        # We do this to minX, maxX for drawing active tab more
        # closing to normal tabs
        MIN_X = min_x
        min_x = MIN_X - self.DeltaXForTabs

        # Add max_x by DeltaXForTabs
        # Restore max_x to original value at the end
        MAX_X = max_x
        max_x = MAX_X + self.DeltaXForTabs

        # Substract min_y, restore to origin at the end
        MIN_Y = min_y
        min_y = MIN_Y + 1

        # We use CGContextAddArcToPoint(context, x1, y1, x2, y2, radius)
        # to construct rounded corners

        # Make active tab 1px heigher than normal tab
        max_y -= 1

        # Move minY upper by 1 px
        min_y += 1

        # Restore minX, maxX to original value
        min_x = MIN_X
        max_x = MAX_X

        radius = self.RADIUS

        #
        # Fill path
        #

        # top left arc
        context.arc(min_x + radius, min_y + radius, radius,
                math.pi, 3 * math.pi / 2)
        # top right arc
        context.arc(min_x + self.width - radius, min_y + radius, radius,
                3 * math.pi /2, 0)
        #context.arc_negative(max_x + radius, max_y - radius, radius, math.pi, math.pi / 2)
        # line to bottom right
        context.line_to(max_x, max_y)
        # line to bottom left point
        context.line_to(min_x, max_y)
        context.close_path()
        context.set_source_rgb(self.normal_bg_color[0],
                self.normal_bg_color[1],
                self.normal_bg_color[2])
        context.fill()
        #
        # Stroke the same path
        #

        # top left arc
        context.arc(min_x + radius, min_y + radius, radius,
                math.pi, 3 * math.pi / 2)
        # top right arc
        context.arc(min_x + self.width - radius, min_y + radius, radius,
                3 * math.pi /2, 0)
        # line to bottom right
        context.line_to(max_x, max_y)
        # line to bottom left point
        context.line_to(min_x, max_y)
        context.close_path()
        context.set_line_width(2.0)
        context.set_source_rgb(0.60, 0.60, 0.60)
        context.stroke()


    def get_rect(self):
        index = self.tabview.tabs.index(self)
        rect = Gdk.Rectangle()
        prev_tabs_width = 0
        for tab in self.tabview.tabs:
            if tab == self:
                break
            prev_tabs_width += tab.width;
        rect.x = prev_tabs_width + self.LeftPadding
        rect.width = self.width
        rect.height = self.TabbarHeight - self.DeltaYForTabs
        rect.y = self.DeltaYForTabs
        return rect
