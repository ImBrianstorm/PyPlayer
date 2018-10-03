"""Finder
Finder is a module that will search for mp3 files in Music directory, and print
its information"""

__author__ = "Mauricio Chavéz Olea"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0"
__email__ = "mauriciochavez@ciencias.unam.mx"

from os import walk
from getpass import getuser
from mutagen import id3
from song import Song

for path, _, files in walk('/home/' + getuser() + '/Music'):
    for song in files:
        if song[-4:] == ".mp3":
            songpath = path + "/" + song
            song = Song(songpath)
            print(song)
            print("\n")
