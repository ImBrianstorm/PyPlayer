from song_miner import SongMiner
from music_database import MusicDatabase
from threading import Thread

class Controller():
    def __init__(self,view):
        self.view = view
        self.song_model = view.get_song_model()

        self.view.connect('start-querying',self.on_querying)
        self.view.connect('start-mining',self.on_mine_button_pressed)
        

        self.view.show_all()

    def on_querying(self,search_entry,query):
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

    def mine_songs(self):
        self.view.show_spinner(True)
        database = MusicDatabase()
        database.create_database()
        miner = SongMiner(database)
        for song,percentage in miner.send_mp3_files_to_database(miner.get_mp3_founded()):
            self.view.change_subtitle("Mining songs: %" + str(percentage))
            self.view.append_song_to_tree_view(song)
        self.view.change_subtitle("Player built in Python")
        self.view.show_spinner(False)
        database.close()