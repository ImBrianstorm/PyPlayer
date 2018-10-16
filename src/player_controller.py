from song_miner import SongMiner
from music_database import MusicDatabase
from threading import Thread
import os

class Controller():
    def __init__(self,view):
        self.view = view
        self.song_model = view.get_song_model()
        self.mp3_founded = 0
        self.already_mined = False

        self.view.connect('start-querying',self.on_querying)
        self.view.connect('start-mining',self.on_mine_button_pressed)
        # self.view.connect('clicked_song',self.play_song)
        self.view.connect('event',self.play_song)

        self.view.show_all()

    def on_querying(self,search_entry,query):
        if self.already_mined:
            database = MusicDatabase()
            if query != "":
                self.view.delete_all_from_tree_view()
                for path in database.search_songs(query):
                    self.view.append_song_to_tree_view(path)
            else:
                for path in database.get_songs_list():
                    self.view.append_song_to_tree_view(path)
            database.close()


    def on_mine_button_pressed(self,button,*args):
        Thread(target=self.mine_songs).start()

    def play_song(self,treeview,path):
        if path.button == 3:
        #     widget.popup(None, None, None, event.button, event.time)
            print("Lo tienes")

    def mine_songs(self):
        database = MusicDatabase()
        database.create_database()
        miner = SongMiner(database)
        if self.mp3_founded != miner.count_mp3_files():
            self.view.show_spinner(True)
            for song,percentage in miner.send_mp3_files_to_database():
                self.view.change_subtitle("Mining songs: %" + str(percentage))
                self.view.append_song_to_tree_view(song)
            self.view.change_subtitle("Player built in Python")
            self.view.show_spinner(False)
            database.close()
            self.mp3_founded = miner.count_mp3_files()
            self.already_mined = True
