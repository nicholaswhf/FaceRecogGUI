import sys
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QAction,QLabel,QPushButton

class GUi(QMainWindow):
	"""docstring for GUi"""
	def __init__(self):
		super(GUi, self).__init__()
		self.initUI()
	def initUI(self):
		self.resize(600,400)
		self.move(0,300)
		self.setWindowTitle('Entrance Manager')
		self.add_menu_and_statu()
		self.add_position_layout()

		#
	def add_menu_and_statu(self):
		self.statusBar().showMessage('12')
		#
		menu=self.menuBar()
		
		file_menu=menu.addMenu('file')
		edit_menu=menu.addMenu('edit')
		file_menu.addSeparator()

		new_action=QAction('new file',self)
		new_action.setStatusTip('a new file')
		file_menu.addAction(new_action)
		
		exit_action=QAction('exit',self)
		exit_action.setStatusTip('click to exit ')
		exit_action.triggered.connect(self.close)
		exit_action.setShortcut('Ctrl+Q')
		file_menu.addAction(exit_action)
	def add_position_layout(self):
		label=QLabel('label1',self)
		#button_1=QPushButton('button',self)

if __name__ == '__main__':
	app=QApplication(sys.argv)
	gui=GUi()
	gui.show()
	sys.exit(app.exec_())