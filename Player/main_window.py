import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import sys

songs_list = [("Arctic Monkeys","Do I Wanna Know?","AM","2013","Rock","1/12"),
              ("Arctic Monkeys","R U Mine?","AM","2013","Rock","2/12"),
              ("Arctic Monkeys","One For The Road","AM","2013","Rock","3/12"),
              ("Arctic Monkeys","Arabella","AM","2013","Rock","4/12"),
              ("Arctic Monkeys","I Want It All","AM","2013","Rock","5/12")]

class PlayerWindow(Gtk.Window):

    def __init__(self,app):
        Gtk.Window.__init__(self, title="PyPlayer",application=app)
        self.set_border_width(20)
        self.set_default_size(1000, 600)
        self.set_position(Gtk.WindowPosition.CENTER)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "PyPlayer"
        hb.set_subtitle("Player built in Python")
        self.set_titlebar(hb)

        search_entry = Gtk.SearchEntry()
        hb.pack_end(search_entry)
        
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.song_liststore = Gtk.ListStore(str, str, str, str, str, str)
        for song in songs_list:
            self.song_liststore.append(list(song))
        self.current_filter_language = None

        #Creating the filter, feeding it with the liststore model
        self.language_filter = self.song_liststore.filter_new()
        #setting the filter function, note that we're not using the
        self.language_filter.set_visible_func(self.language_filter_func)

        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        for i, column_title in enumerate(["Performer", "Title", "Album","Release Year","Genre","Track Number"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)


        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True
        else:
            return model[iter][2] == self.current_filter_language


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = PlayerWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
