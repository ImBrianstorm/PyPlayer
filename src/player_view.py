import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gio

import sys

class PlayerView(Gtk.ApplicationWindow):

    __gsignals__ = {
        'start-querying': (GObject.SIGNAL_RUN_LAST, None, (str,)),
        'start-mining': (GObject.SIGNAL_RUN_LAST, None, ()),
        'clicked-song': (GObject.SIGNAL_RUN_LAST, None, (str,)),
        'paused-song': (GObject.SIGNAL_RUN_LAST, None, ()),
        'stopped-song': (GObject.SIGNAL_RUN_LAST, None, ())
    }

    def __init__(self,app):
        Gtk.ApplicationWindow.__init__(self, title="PyPlayer",application=app)
        self.column_counter = 0
        self.initialize_window()

    def initialize_window(self):
        self.set_border_width(10)
        self.maximize()

        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = "PyPlayer"
        self.header_bar.set_subtitle("Player built in Python")
        self.set_titlebar(self.header_bar)

        self.edit_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="edit-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.edit_button.add(image)
        self.edit_button.set_tooltip_text("Edit a song")
        self.header_bar.pack_start(self.edit_button)
        self.edit_button.connect('clicked',self.edit_button_pressed)

        self.mining_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="system-run-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.mining_button.add(image)
        self.mining_button.set_tooltip_text("Start mining")
        self.header_bar.pack_start(self.mining_button)
        self.mining_button.connect("clicked",self.mining_button_pressed)

        self.spinner = Gtk.Spinner()
        self.header_bar.pack_start(self.spinner)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.connect('search-changed', self.search)
        self.header_bar.pack_end(self.search_entry)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.add(self.grid)

        self.song_model = Gtk.ListStore(str, str, str, str, str, str, str)

        self.treeview = Gtk.TreeView(model=self.song_model)
        self.treeview.connect('row-activated',self.row_activated)
        for column_title in ["Performer", "Title", "Album","Release Year","Genre","Track Number","Path"]:
            cell = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, cell, text=self.column_counter)
            if self.column_counter == 6:
                column.set_visible(False)
            self.treeview.append_column(column)
            self.column_counter += 1

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 1, 2, 1)
        self.scrollable_treelist.add(self.treeview)

        self.action_bar = Gtk.ActionBar()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.box.get_style_context(), "linked")

        self.play_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="media-playback-start-symbolic")
        button_image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.play_button.add(button_image)
        self.play_button.connect('clicked',self.row_activated)
        self.box.add(self.play_button)

        self.pause_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="media-playback-pause-symbolic")
        button_image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.pause_button.add(button_image)
        self.pause_button.connect('clicked',self.pause_button_pressed)
        self.box.add(self.pause_button)

        self.stop_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="media-playback-stop-symbolic")
        button_image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.stop_button.add(button_image)
        self.stop_button.connect('clicked',self.stop_button_pressed)
        self.box.add(self.stop_button)

        self.action_bar.pack_start(self.box)
        self.grid.attach(self.action_bar,0,2,2,1)

    def append_song_to_tree_view(self,song):
        song_list = [song.performer, song.title, song.album, str(song.recording_time), song.genre,
              str(song.track_number), song.songpath]
        self.song_model.append(song_list)

    def delete_all_from_tree_view(self):
        self.song_model.clear()

    def change_subtitle(self,subtitle):
        self.header_bar.set_subtitle(subtitle)

    def search(self,search_entry,*args):
        self.emit('start-querying',self.search_entry.get_text())

    def row_activated(self,search_entry,*args):
        model,iter = self.treeview.get_selection().get_selected()
        if iter is not None:
            path = model[iter][6]
            self.emit('clicked-song',path)

    def mining_button_pressed(self,button,*args):
        self.emit('start-mining')

    def edit_button_pressed(self,button,*args):
        edit_window = Gtk.Window(title="Editing a song...")
        edit_window.set_default_geometry(600,400)
        edit_window.set_position(Gtk.WindowPosition.CENTER)
        edit_window.set_border_width(20)

        edit_grid = Gtk.Grid()

        performer_label = Gtk.Label(label="Performer")
        performer_label.set_visible(True)
        edit_grid.attach(performer_label,0,0,1,1)
        performer_entry = Gtk.Entry()
        performer_entry.set_visible(True)
        edit_grid.attach_next_to(performer_label, performer_entry, Gtk.PositionType.RIGHT, 1,1)
        edit_grid.attach(performer_entry,1,0,2,1)

        title_label = Gtk.Label(label="Title")
        title_label.set_visible(True)
        edit_grid.attach(title_label,0,1,1,1)
        title_entry = Gtk.Entry()
        title_entry.set_visible(True)
        edit_grid.attach_next_to(title_label, title_entry, Gtk.PositionType.RIGHT, 1,1)
        edit_grid.attach(title_entry,1,1,2,1)

        album_label = Gtk.Label(label="Album")
        album_label.set_visible(True)
        edit_grid.attach(album_label,0,2,1,1)
        album_entry = Gtk.Entry()
        album_entry.set_visible(True)
        edit_grid.attach_next_to(album_label, album_entry, Gtk.PositionType.RIGHT, 1,1)
        edit_grid.attach(album_entry,1,2,2,1)

        recording_time_label = Gtk.Label(label="Recording Time")
        recording_time_label.set_visible(True)
        edit_grid.attach(recording_time_label,0,3,1,1)
        recording_time_entry = Gtk.Entry()
        recording_time_entry.set_visible(True)
        edit_grid.attach_next_to(recording_time_label, recording_time_entry, Gtk.PositionType.RIGHT, 1,1)
        edit_grid.attach(recording_time_entry,1,3,2,1)

        track_number_label = Gtk.Label(label="Track Number")
        track_number_label.set_visible(True)
        edit_grid.attach(track_number_label,0,4,1,1)
        track_number_entry = Gtk.Entry()
        track_number_entry.set_visible(True)
        edit_grid.attach_next_to(track_number_label, track_number_entry, Gtk.PositionType.RIGHT, 1,1)
        edit_grid.attach(track_number_entry,1,4,2,1)

        genre_label = Gtk.Label(label="Genre")
        genre_label.set_visible(True)
        edit_grid.attach(genre_label,0,5,1,1)
        genre_entry = Gtk.Entry()
        genre_entry.set_visible(True)
        edit_grid.attach_next_to(genre_label, genre_entry, Gtk.PositionType.RIGHT, 1,1)
        edit_grid.attach(genre_entry,1,5,2,1)

        edit_button_box = Gtk.Box()
        cancel_button = Gtk.Button(label='Cancel')
        cancel_button.set_visible(True)
        accept_button = Gtk.Button(label='Accept')
        accept_button.set_visible(True)
        edit_button_box.pack_start(accept_button,True,True,5)
        edit_button_box.pack_start(cancel_button,True,True,5)
        edit_button_box.set_visible(True)
        edit_grid.attach(edit_button_box,1,6,2,1)

        edit_grid.set_row_spacing(20)
        edit_grid.set_row_homogeneous(True)
        edit_grid.set_column_homogeneous(True)

        edit_grid.set_visible(True)
        edit_window.add(edit_grid)
        edit_window.set_visible(True)

    def pause_button_pressed(self,button,*args):
        self.emit('paused-song')

    def stop_button_pressed(self,button,*args):
        self.emit('stopped-song')

    def show_spinner(self,show):
        if show:
            self.spinner.start()
        else:
            self.spinner.stop()

    def get_song_model(self):
        return self.song_model
