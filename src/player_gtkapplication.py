import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from player_view import PlayerView 
from player_controller import Controller

class PlayerGtkApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)
        self.win = None

    def do_activate(self):
        Controller(PlayerView(app=self))

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def on_quit(self, action, param):
        self.quit()