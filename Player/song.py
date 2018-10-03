"""
song is a module that contains Song class. Song will get id3 tags from a file
and set is attributes from them. """

__author__ = "Mauricio Chavéz Olea"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0"
__email__ = "mauriciochavez@ciencias.unam.mx"

from mutagen.id3 import ID3

class Song():
    """
    Class that gets id3 tags from a file and assing them to is attributes

    Attributes:
        tags: Dictionary that contains ID3 tags
        performer: Song's performer
        title: Song's title
        album: Song's album
        recording_time: Song's recording time
        track_number: Track number
    """
    def __init__(self,filething):
        """Initialize a Song object
        Arguments:
            filething: string specifing song's path
        """
        self.tags = ID3(filething)
        self.performer = str(self.tags['TPE1']) if 'TPE1' in self.tags else 'Unknown'
        self.title = str(self.tags['TIT2']) if 'TIT2' in self.tags else 'Unknown'
        self.album = str(self.tags['TALB']) if 'TALB' in self.tags else 'Unknown'
        self.recording_time = str(self.tags['TDRC']) if 'TDRC' in self.tags else '2000'
        self.track_number = str(self.tags['TRCK']) if 'TRCK' in self.tags else '1/1'
    
    def __str__(self):
        """Returns a string with the song information"""
        return ("Performer: " + self.performer + 
                "\nTitle: " + self.title + 
                "\nAlbum: " + self.album +
                "\nRecording time: " + self.recording_time +
                "\nTrack number: " + self.track_number)

