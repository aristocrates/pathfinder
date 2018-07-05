"""
Handles scroll to zoom logic
"""

class Zoom:
    """
    Enforces minimum and maximum zoom, and rate of zoom
    """
    def __init__(self, zoom_thresh = 120, zoom_min = -5, zoom_max = 30):
        # the scroll can be no lower than zero
        self.scroll = 0
        self.zoom_thresh = zoom_thresh
        self.zoom_min = zoom_min
        self.zoom_max = zoom_max

        self.prev_scroll = None

    def change_scroll(self, scroll_amount):
        if self.scroll + scroll_amount <= (self.zoom_min * self.zoom_thresh):
            self.scroll = self.zoom_min * self.zoom_thresh
        elif self.scroll + scroll_amount >= (self.zoom_max * self.zoom_thresh):
            self.scroll = self.zoom_max * self.zoom_thresh
        else:
            self.scroll += scroll_amount

    def zoom_delta(self):
        if self.prev_scroll == None:
            # first time
            scroll_delta = self.scroll
        else:
            scroll_delta = self.scroll - self.prev_scroll
        self.prev_scroll = self.scroll
        return scroll_delta / self.zoom_thresh

    def zoom_level(self):
        return self.scroll // self.zoom_thresh
