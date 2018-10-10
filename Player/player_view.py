import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gio

import sys

class PlayerView(Gtk.ApplicationWindow):

    __gsignals__ = {
        'start-querying': (GObject.SIGNAL_RUN_LAST, None, (str,)),
        'start-mining': (GObject.SIGNAL_RUN_LAST, None, ())
    }

    def __init__(self,app):
        Gtk.ApplicationWindow.__init__(self, title="PyPlayer",application=app)
        self.column_counter = 0
        self.initialize_window()

    def initialize_window(self):
        self.set_border_width(30)
        self.set_default_size(1500, 1000)

        self.set_position(Gtk.WindowPosition.CENTER)

        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = "PyPlayer"
        self.header_bar.set_subtitle("Player built in Python")
        self.set_titlebar(self.header_bar)

        self.mining_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="system-run-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.mining_button.add(image)
        self.header_bar.pack_start(self.mining_button)
        self.mining_button.connect("clicked",self.mining_button_pressed)

        self.spinner = Gtk.Spinner()
        self.header_bar.pack_start(self.spinner)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.connect('search-changed', self.search)
        self.header_bar.pack_end(self.search_entry)
        
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.song_model = Gtk.ListStore(str, str, str, str, str, str)

        self.treeview = Gtk.TreeView(model=self.song_model)
        for column_title in ["Performer", "Title", "Album","Release Year","Genre","Track Number"]:
            cell = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, cell, text=self.column_counter)
            self.treeview.append_column(column)
            self.column_counter += 1

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)

    def append_song_to_tree_view(self,song):
        song_list = [song.performer, song.title, song.album, str(song.recording_time), song.genre, 
              str(song.track_number) + "/" + str(song.album_tracks_number)]
        self.song_model.append(song_list)

    def delete_all_from_tree_view(self):
        self.song_model.clear()

    def change_subtitle(self,subtitle):
        self.header_bar.set_subtitle(subtitle)

    def search(self,search_entry,*args):
        self.emit('start-querying',self.search_entry.get_text())

    def mining_button_pressed(self,button,*args):
        self.emit('start-mining')

    def show_spinner(self,show):
        if show:
            self.spinner.start()
        else:
            self.spinner.stop()

    def get_song_model(self):
        return self.song_model