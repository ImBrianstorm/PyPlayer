"""
song is a module that contains Song class. Song will get id3 tags from a file
and set its attributes from them. """

__author__ = "Mauricio Chavéz Olea"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0"
__email__ = "mauriciochavez@ciencias.unam.mx"

from mutagen.id3 import ID3, TPE1, TIT2, TALB, TDRC, TCON, TRCK

class Song():
    """
    Class that gets id3 tags from a file and assing them to its attributes

    Attributes:
        tags: Dictionary that contains ID3 tags
        performer: Song's performer
        title: Song's title
        album: Song's album
        recording_time: Song's recording time
        genre: Song's genre
        track_number: Track number
    """
    def __init__(self,filething):
        """Initialize a Song object
        Arguments:
            filething: string specifing song's path
        """
        self.__dict__['tags'] = ID3(filething)
        self.__dict__['performer'] = str(self.tags['TPE1']) if 'TPE1' in self.tags else 'Unknown'
        self.__dict__['title'] = str(self.tags['TIT2']) if 'TIT2' in self.tags else 'Unknown'
        self.__dict__['album'] = str(self.tags['TALB']) if 'TALB' in self.tags else 'Unknown'
        self.__dict__['recording_time'] = int(str(self.tags['TDRC'])) if 'TDRC' in self.tags else 2000
        self.__dict__['genre'] = str(self.tags['TCON']) if 'TCON' in self.tags else 'Unknown'
        self.__dict__['track_number'] = self.get_track_number() if 'TRCK' in self.tags else 1
        self.__dict__['album_tracks_number'] = self.get_album_tracks_number()
        self.__dict__['songpath'] = filething
        self.__dict__['albumpath'] = self.get_album_path()
    
    def __str__(self):
        """Returns a string with the song information"""
        return ("Performer: " + self.performer + 
                "\nTitle: " + self.title + 
                "\nAlbum: " + self.album +
                "\nRecording time: " + str(self.recording_time) +
                "\nGenre: " + self.genre +
                "\nTrack number: " + str(self.track_number) +
                "\nAlbum tracks number: " + str(self.album_tracks_number) +
                "\nSong path: " + self.songpath +
                "\nAlbum path: " + self.albumpath)

    def __getattr__(self,attr):
        """Returns argument's attribute, raises an exception if attribute does not exist
           
           Arguments:
                attr: attribute to get
        """
        value = self.__dict__.get(attr)
        if not value:
            raise AttributeError("'Song' object has no attribute '%s'" % attr)
        else:
            return value

    def __setattr__(self,attr,value):
        """Sets argument's attribute, replacing it by argument's value, and then
           adds its respective ID3 tag to mp3 file. Raises an exception if attribute does not exist 
           
           Arguments:
                attr: attribute to set
                value: new value for attribute
           """
        if attr not in self.__dict__:
            raise AttributeError("'Song' object has no attribute '%s'" % attr)
        else:
            self.__dict__[attr] = value
            if attr != 'tags' and attr != 'songpath' and attr != 'albumpath':
                self.add_tag(attr,value)

    def add_tag(self,attr,value):
        """Replace specified ID3 tag on mp3 file
           Arguments:
                attr: attribute to set on file
                value: new value for ID3 Tag
        """
        if attr in self.__dict__:
            if attr == 'performer':
                self.tags.add(TPE1(encoding=3, text=value))
            elif attr == 'title':
                self.tags.add(TIT2(encoding=3, text=value))
            elif attr == 'album':
                self.tags.add(TALB(encoding=3, text=value))
            elif attr == 'recording_time':
                self.tags.add(TDRC(encoding=3, text=value))
            elif attr == 'genre':
                self.tags.add(TCON(encoding=3, text=value))
            elif attr == 'track_number':
                track = str(value) + "/" + str(self.album_tracks_number)
                self.tags.add(TRCK(encoding=3, text=track))
            elif attr == 'album_tracks_number':
                track = str(self.track_number) + "/" + str(value)
                self.tags.add(TRCK(encoding=3, text=track))    

            self.tags.save()
        else:
            raise AttributeError("'Song' object has no attribute '%s'" % attr)

    def get_album_path(self):
        albumpath = self.songpath[::-1]
        for index,char in enumerate(albumpath):
            if char == '/':
                albumpath = albumpath[index:]
                break
        return albumpath[::-1]

    def get_track_number(self):
        track = str(self.tags['TRCK'])
        for index,char in enumerate(track):
            if char == '/':
                track = track[:index]
                break
        return int(track)

    def get_album_tracks_number(self):
        track = str(self.tags['TRCK'])
        for index,char in enumerate(track):
            if char == '/':
                track = track[index+1:]
                break
        return int(track)
