import unittest
from song import Song

class TestSong(unittest.TestCase):
    
    def setUp(self):
        self.song = Song('./TestResources/Arabella.mp3')

    def tearDown(self):
        self.song.add_tag('performer','Arctic Monkeys')
        self.song.add_tag('title','Arabella')

    def test_str(self):
        self.assertEqual(str(self.song),"Performer: Arctic Monkeys" + 
                                        "\nTitle: Arabella" + 
                                        "\nAlbum: AM" +
                                        "\nRecording time: 2013" +
                                        "\nGenre: Rock" +
                                        "\nTrack number: 4" +
                                        "\nAlbum tracks number: 10"+
                                        "\nSong path: ./TestResources/Arabella.mp3" + 
                                        "\nAlbum path: ./TestResources/")

    def test_get_attr(self):
        self.assertEqual(self.song.performer,'Arctic Monkeys')

    def test_get_attr_error(self):
        with self.assertRaises(AttributeError):
            self.song.does_not_exist

    def test_set_attr(self):
        self.song.title = 'La Bamba'
        self.assertEqual(self.song.title,'La Bamba')

    def test_set_attr_error(self):
        with self.assertRaises(AttributeError):
            self.song.composer = 'Armando Manzanero'

    def test_add_tag(self):
        self.song.add_tag('performer','Manzanero')
        song2 = Song('./TestResources/Arabella.mp3')
        self.assertEqual(song2.performer,'Manzanero')

    def test_add_tag_error(self):
        with self.assertRaises(AttributeError):
            self.song.add_tag('composer','Manzanero')

if __name__ == '__main__':
    unittest.main()