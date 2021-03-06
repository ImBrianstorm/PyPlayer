from song import Song
import sqlite3

class MusicDatabase:

	def __init__(self):
		self.con = sqlite3.connect("music.db",timeout=10)
		self.table_created = False

	def create_table(self,table_name,*args):
		create_string = "CREATE TABLE IF NOT EXISTS " + table_name + "("
		for field in args[:-1]:
			create_string += field + ", "
		create_string += args[-1] + ")"
		self.con.execute(create_string)
		self.con.commit()
		self.table_created = True

	def insert_into_table(self,table_name,values_tuple,columns="",conditional=""):
		insert_string = "INSERT INTO " + table_name + " "
		if columns != "":
			insert_string += "(" + columns + ") "
		insert_string += "VALUES ("
		for value in values_tuple[:-1]:
			if isinstance(value,str):
				if "'" in value:
					insert_string += '"' + value + '",'
				else:
					insert_string += "'" + value + "',"
			else:
				insert_string += str(value) + ","
		if isinstance(values_tuple[-1],str):
			if "'" in values_tuple[-1]:
				insert_string += '"' + values_tuple[-1] + '")'
			else:
				insert_string += "'" + values_tuple[-1] + "')"
		else:
			insert_string += str(values_tuple[-1]) + ")"
		if conditional != "":
			insert_string += " WHERE " + conditional
		try:
			with self.con:
				self.con.execute(insert_string)
				self.con.commit()
		except sqlite3.IntegrityError:
			pass

	def create_database(self):
		if not self.table_created:
			self.create_table("types","id_type INTEGER PRIMARY KEY","description TEXT")

			self.insert_into_table("types",(0,"Person"))
			self.insert_into_table("types",(1,"Group"))
			self.insert_into_table("types",(2,"Unknown"))

			self.create_table("performers","id_performer INTEGER PRIMARY KEY",
											"id_type INTEGER",
											"name TEXT",
											"FOREIGN KEY (id_type) REFERENCES types (id_type)")

			self.create_table("persons","id_person INTEGER PRIMARY KEY",
										"stage_name TEXT",
										"real_name TEXT",
										"birth_date TEXT",
										"death_date TEXT")

			self.create_table("groups","id_group INTEGER PRIMARY KEY",
										"name TEXT",
										"start_date TEXT",
										"end_date")

			self.create_table("albums","id_album INTEGER PRIMARY KEY",
										"path TEXT",
										"name TEXT",
										"year INTEGER")

			self.create_table("rolas","id_rola INTEGER PRIMARY KEY",
									"id_performer INTEGER",
									"id_album INTEGER",
									"path TEXT",
									"title TEXT",
									"track INTEGER",
									"year INTEGER",
									"genre TEXT",
									"FOREIGN KEY (id_performer) REFERENCES performers (id_performer)",
									"FOREIGN KEY (id_album) REFERENCES albums (id_album)")

			self.create_table("in_group","id_person INTEGER",
										"id_group INTEGER",
										"PRIMARY KEY (id_person,id_group)",
										"FOREIGN KEY (id_person) REFERENCES persons (id_person)",
										"FOREIGN KEY (id_group) REFERENCES groups (id_group)")

			self.table_created = True

	def print_table(self,table_name):
		for row in self.con.execute("SELECT * FROM " + table_name):
			print(row)

	def insert_song(self,song):
		count = 0
		insert_string = "SELECT COUNT(name) FROM performers WHERE name='{}'".format(song.performer)
		for row in self.con.execute(insert_string):
			count = row[0]
		if count == 0:
			self.insert_into_table('performers',(2,song.performer),' id_type,name')

		count = 0
		insert_string = "SELECT COUNT(name) FROM albums WHERE name='{}' AND path='{}'".format(song.album,
																							  song.albumpath)
		for row in self.con.execute(insert_string):
			count = row[0]
		if count == 0:
			self.insert_into_table('albums',(song.albumpath,song.album,song.recording_time),'path,name,year')

		count = 0
		if "'" in song.title or "'" in song.songpath:
			insert_string = 'SELECT COUNT(title) FROM rolas WHERE title="{}" AND path="{}"'.format(song.title,
																								song.songpath)
		else:
			insert_string = "SELECT COUNT(title) FROM rolas WHERE title='{}' AND path='{}'".format(song.title,
																								song.songpath)
		for row in self.con.execute(insert_string):
			count = row[0]

		if count == 0:
			for row in self.con.execute("SELECT id_performer FROM performers WHERE name= ? ",(song.performer,)):
				id_performer = row[0]

			for row in self.con.execute("SELECT id_album FROM albums WHERE name= ? ",(song.album,)):
				id_album = row[0]
			self.insert_into_table('rolas',(id_performer,id_album,song.songpath,song.title,song.track_number,
											song.recording_time,song.genre),'id_performer,id_album,path,' +
											'title,track,year,genre')

	def get_songs_list(self):
		songs = []
		for row in self.con.execute("SELECT path FROM rolas"):
			path = row[0]
			song = Song(path)
			song_data = None
			performer = None
			album = None
			for row in self.con.execute("SELECT id_performer, id_album, title, track, year, genre " +
										"FROM rolas WHERE path = (?)",(path,)):
				song_data = row
			for row in self.con.execute("SELECT name FROM performers WHERE id_performer = (?)",(song_data[0],)):
				performer = row[0]
			for row in self.con.execute("SELECT name FROM albums WHERE id_album = (?)",(song_data[1],)):
				album = row[0]
			song.performer = performer
			song.title = song_data[2]
			song.album = album
			song.recording_time = song_data[4]
			song.genre = song_data[5]
			song.track_number = song_data[3]
			songs.append(song)
		return songs

	def search_songs(self,query):
		songs = []
		paths = []
		performers = {}
		for row in self.con.execute("SELECT path FROM rolas WHERE title LIKE ?",("%" + query + "%",)):
			path = row[0]
			song = Song(path)
			paths.append(path)
			songs.append(song)
		for id in self.con.execute("SELECT id_performer FROM performers WHERE name LIKE ?",("%" + query + "%",)):
			for row in self.con.execute("SELECT path FROM rolas WHERE id_performer = (?)",(id[0],)):
				path = row[0]
				song = Song(path)
				if song.songpath not in paths:
					paths.append(path)
					songs.append(song)
		for id in self.con.execute("SELECT id_album FROM albums WHERE name LIKE ?",("%" + query + "%",)):
			for row in self.con.execute("SELECT path FROM rolas WHERE id_album = (?)",(id[0],)):
				path = row[0]
				song = Song(path)
				if song.songpath not in paths:
					paths.append(path)
					songs.append(song)
		for song in songs:
			if song.performer not in performers:
				performer_songs = []
				performers[song.performer] = performer_songs
			else:
				performers[song.performer].append(song)
		songs = []
		for performer in performers:
			for song in performers[performer]:
				songs.append(song)
		return songs

	def close(self):
		self.con.commit()
		self.con.close()

	def get_table_created(self):
		return self.table_created
