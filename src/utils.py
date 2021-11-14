import math

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

def inset_rect(rect, x_delta, y_delta):
    rect.x += x_delta
    rect.y += y_delta
    rect.width -= 2 * x_delta
    rect.height -= 2 * y_delta
    return rect
