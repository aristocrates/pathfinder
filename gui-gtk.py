#!/usr/bin/python
'''
'''
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gio, GdkPixbuf, Rsvg

class MainWindow(Gtk.Window):

    def __init__(self, width=665, height=500):
        Gtk.Window.__init__(self, title="Hello World")

        self.vbox = Gtk.VBox()
        self.add(self.vbox)

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(width, height)
        self.drawing_area.connect("draw", self.on_draw)
        self.vbox.pack_start(self.drawing_area, expand=False, fill=False,
                             padding=5)
        
        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.vbox.pack_start(self.button, expand=False, fill=False,
                             padding=5)

        self.img = None

    def on_button_clicked(self, widget):
        print("Hello World")

    def load_map(self, filename):
        self.svg = Rsvg.Handle.new_from_file(filename)
        self.buf = self.svg.get_pixbuf()
        self.img = Gtk.Image.new_from_pixbuf(self.buf)
        self.draw_img()

    def draw_img(self):
        if self.img is not None:
            help(self.drawing_area)
            self.drawing_area.draw_image(self.img, 0, 0, 0, 0, -1, -1)

if __name__ == "__main__":
    win = MainWindow()
    win.load_map("Caltech_Map.svg")
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
