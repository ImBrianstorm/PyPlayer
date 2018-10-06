from player_gui import App
from PyQt5.QtWidgets import QApplication, QTreeView
import sys

app = QApplication(sys.argv)
ex = App()
model = ex.getModel()
ex.addSong(model, 'Arctic Monkeys', 'Fireside','AM')
sys.exit(app.exec_())