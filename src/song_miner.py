"""
song_miner is a module that will search for mp3 files in Music directory
"""

__author__ = "Mauricio Chavéz Olea"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0"
__email__ = "mauriciochavez@ciencias.unam.mx"

from os import walk
from getpass import getuser
from song import Song
from music_database import MusicDatabase

class SongMiner:

	def __init__(self,database=MusicDatabase(), root='/home/' + getuser() + '/Music'):
		self.root = root
		self.songpaths = []
		self.database = database

	def count_mp3_files(self):
		mp3_files_founded = len(self.songpaths)
		for path, _, files in walk(self.root):
			for song in files:
				if song[-4:] == ".mp3":
					songpath = path + "/" + song
					if songpath not in self.songpaths:
						self.songpaths.append(songpath)
						mp3_files_founded += 1
		return mp3_files_founded

	def send_mp3_files_to_database(self):
		if self.database.get_table_created():
			percentage = 0
			part = 100/self.count_mp3_files()
			for songpath in self.songpaths:
				song = Song(songpath)
				self.database.insert_song(song)
				percentage += part
				percentage = round(percentage,2)
				yield song,percentage