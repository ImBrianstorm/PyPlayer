import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QTreeView, QVBoxLayout, QWidget

class App(QWidget):

	PERFORMER, TITLE, ALBUM, RECORDING_TIME, GENRE, TRACK_NUMBER = range(6)

	def __init__(self):
		super().__init__()
		self.title = 'PyPlayer'
		self.left = 20
		self.top = 20
		self.width = 700
		self.height = 240
		self.model = None
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.dataGroupBox = QGroupBox("Songs")
		self.dataView = QTreeView()
		self.dataView.setRootIsDecorated(False)
		self.dataView.setAlternatingRowColors(True)

		dataLayout = QHBoxLayout()
		dataLayout.addWidget(self.dataView)
		self.dataGroupBox.setLayout(dataLayout)

		self.model = self.createSongModel(self)
		self.dataView.setModel(self.model)
		self.addSong(self.model, 'Arctic Monkeys', 'Arabella','AM','2013','Rock','4/12')
		self.addSong(self.model, 'Arctic Monkeys', 'Do I Wanna Know?','AM','2013','Rock','1/12')
		self.addSong(self.model, 'Arctic Monkeys', 'R U Mine?','AM','2013','Rock','2/12')
		self.addSong(self.model, 'Arctic Monkeys', 'Knee Socks','AM','2013','Rock','11/12')
		self.addSong(self.model, 'Arctic Monkeys', 'I Wanna Be Yours','AM','2013','Rock','12/12')

		mainLayout = QVBoxLayout()
		mainLayout.addWidget(self.dataGroupBox)
		self.setLayout(mainLayout)

		self.show()
 
	def createSongModel(self,parent):
		model = QStandardItemModel(0, 6, parent)
		model.setHeaderData(self.PERFORMER, Qt.Horizontal, "Performer")
		model.setHeaderData(self.TITLE, Qt.Horizontal, "Title")
		model.setHeaderData(self.ALBUM, Qt.Horizontal, "Album")
		model.setHeaderData(self.RECORDING_TIME, Qt.Horizontal, "Recording Time")
		model.setHeaderData(self.GENRE, Qt.Horizontal, "Genre")
		model.setHeaderData(self.TRACK_NUMBER, Qt.Horizontal, "Track Number")
		return model

	def addSong(self,model, performer, title, album, recording_time, genre, track_number):
		model.insertRow(0)
		model.setData(model.index(0, self.PERFORMER), performer)
		model.setData(model.index(0, self.TITLE), title)
		model.setData(model.index(0, self.ALBUM), album)
		model.setData(model.index(0, self.RECORDING_TIME), recording_time)
		model.setData(model.index(0, self.GENRE), genre)
		model.setData(model.index(0, self.TRACK_NUMBER), track_number)

	def getModel(self):
		return self.model
 
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())