from song_miner import SongMiner
from music_database import MusicDatabase
from threading import Thread

class Controller():
    def __init__(self,view):
        self.view = view

        self.view.connect('start-querying',self.on_querying)  
        
        self.song_model = view.get_song_model()

        self.view.show_all()

        Thread(target=self.initialize).start()

    def on_querying(self,search_entry,query):
        pass

    def initialize(self):
        self.database = MusicDatabase()
        miner = SongMiner(self.database)
        for song,percentage in miner.send_mp3_files_to_database(miner.get_mp3_founded()):
            self.view.change_subtitle("Mining songs: %" + str(percentage))
            self.view.append_song_to_tree_view(song)
        self.view.change_subtitle("Player built in Python")