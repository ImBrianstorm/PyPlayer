import sqlite3

class MusicDatabase:
	def __init__(self):
		self.con = sqlite3.connect('music.db')
		self.c = self.con.cursor()
		self.create_database()

	def create_database(self):
		self.con.execute("CREATE TABLE IF NOT EXISTS types(" +
						"id_type INTEGER PRIMARY KEY," +
						"description TEXT)")

		self.con.execute("INSERT INTO types VALUES (0 , 'Person')")
		self.con.execute("INSERT INTO types VALUES (1 , 'Group')")
		self.con.execute("INSERT INTO types VALUES (2 , 'Unknown');")

		self.con.execute("CREATE TABLE IF NOT EXISTS performers (" +
						"id_performer INTEGER PRIMARY KEY," +
						"id_type INTEGER ," +
						"name TEXT ," +
						"FOREIGN KEY (id_type) REFERENCES types (id_type))")

		self.con.execute("CREATE TABLE IF NOT EXISTS persons (" +
						"id_person INTEGER PRIMARY KEY," +
						"stage_name TEXT," +
						"real_name TEXT," +
						"birth_date TEXT," +
						"death_date TEXT)")

		self.con.execute("CREATE TABLE IF NOT EXISTS groups (" +
						"id_group INTEGER PRIMARY KEY," +
						"name TEXT," +
						"start_date TEXT," +
						"end_date TEXT)")

		self.con.execute("CREATE TABLE IF NOT EXISTS albums (" +
						"id_album INTEGER PRIMARY KEY," +
						"path TEXT," +
						"name TEXT," +
						"year INTEGER)")

		self.con.execute("CREATE TABLE IF NOT EXISTS rolas (" +
						"id_rola INTEGER PRIMARY KEY," +
						"id_performer INTEGER," +
						"id_album INTEGER," +
						"path TEXT," +
						"title TEXT," +
						"track INTEGER," +
						"year INTEGER," +
						"genre TEXT," +
						"FOREIGN KEY (id_performer) " +
						"REFERENCES performers (id_performer) ," +
						"FOREIGN KEY (id_album) " +
						"REFERENCES albums (id_album))")

		self.con.execute("CREATE TABLE IF NOT EXISTS in_group (" +
						"id_person INTEGER," +
						"id_group INTEGER," +
						"PRIMARY KEY (id_person , id_group) ," +
						"FOREIGN KEY (id_person) REFERENCES persons (id_person) ," +
						"FOREIGN KEY (id_group) REFERENCES groups (id_group))")

	def insert_into_table(self, table_name,values,columns=""):
		insert_string = "INSERT INTO " + table_name + " "
		if columns == "":
			insert_string += "(" + columns + ") "
		insert_string += "VALUES (" + values + ")"
		try:
			with self.con:
				self.con.execute(insert_string)
		except sqlite3.IntegrityError:
			print("An error while inserting into table has ocurred...")
		self.con.execute(insert_string)

	def print_table(self,table_name):
		self.con.execute("SELECT * FROM " + table_name)
		print(self.con)