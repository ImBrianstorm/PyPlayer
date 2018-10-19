from song_miner import SongMiner
from music_database import MusicDatabase
from threading import Thread
from gi.repository import GLib
import vlc
import os

class Controller():
    def __init__(self,view):
        self.view = view
        self.song_model = view.get_song_model()
        self.mp3_founded = 0
        self.player = None
        self.already_mined = False
        self.paused = True
        self.path = None
        self.player_instance = vlc.Instance()
        self.player = self.player_instance.media_player_new()

        self.view.connect('start-querying',self.on_querying)
        self.view.connect('start-mining',self.on_mine_button_pressed)
        self.view.connect('clicked-song',self.play_song)
        self.view.connect('paused-song',self.pause_song)
        self.view.connect('stopped-song',self.stop_song)

        self.view.show_all()

    def on_querying(self,search_entry,query):
        if self.already_mined:
            database = MusicDatabase()
            if query != "":
                GLib.idle_add(self.view.delete_all_from_tree_view)
                for song in database.search_songs(query):
                    GLib.idle_add(self.view.append_song_to_tree_view,song)
            else:
                GLib.idle_add(self.view.delete_all_from_tree_view)
                for song in database.get_songs_list():
                    GLib.idle_add(self.view.append_song_to_tree_view,song)
            database.close()


    def on_mine_button_pressed(self,button,*args):
        Thread(target=self.mine_songs).start()

    def play_song(self,treeview,path):
        if not self.player.get_media():
            self.open(path)
            self.player.play()
            self.paused = False
        else:
            if self.paused and self.path == path:
                self.player.play()
                self.paused = False
            elif self.path != path:
                    self.player.stop()
                    self.open(path)
                    self.player.play()
                    self.paused = False
        self.path = path


    def stop_song(self,*args):
        self.player.stop()
        self.paused = True

    def pause_song(self,*args):
        if not self.paused:
            self.player.pause()
            self.paused = True

    def open(self,path):
        self.stop_song()
        media = self.player_instance.media_new(path)
        self.player.set_media(media)

    def mine_songs(self):
        database = MusicDatabase()
        database.create_database()
        miner = SongMiner(database)
        if self.mp3_founded != miner.count_mp3_files():
            GLib.idle_add(self.view.show_spinner,True)
            for song,percentage in miner.send_mp3_files_to_database():
                GLib.idle_add(self.view.change_subtitle,"Mining songs: %" + str(percentage))
                GLib.idle_add(self.view.append_song_to_tree_view,song)
            GLib.idle_add(self.view.change_subtitle,"Player built in Python")
            GLib.idle_add(self.view.show_spinner,False)
            database.close()
            self.mp3_founded = miner.count_mp3_files()
            self.already_mined = True
