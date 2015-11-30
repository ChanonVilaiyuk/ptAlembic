from PySide import QtCore
from PySide import QtGui

from shiboken import wrapInstance

class customQWidgetItem(QtGui.QWidget) : 
	def __init__(self, parent = None) : 
		super(customQWidgetItem, self).__init__(parent)
		# set label 
		self.allLayout = QtGui.QHBoxLayout()
		self.gridLayout = QtGui.QGridLayout()

		self.text1Label = QtGui.QLabel()
		self.text2Label = QtGui.QLabel()
		self.text3Label = QtGui.QLabel()

		# set icon
		self.iconQLabel = QtGui.QLabel()

		self.gridLayout.addWidget(self.iconQLabel, 1, 1)
		self.gridLayout.addWidget(self.text1Label, 1, 2)
		self.gridLayout.addWidget(self.text2Label, 2, 2)
		self.gridLayout.addWidget(self.text3Label, 2, 3)
		self.gridLayout.setColumnStretch(2, 2)

		self.allLayout.addLayout(self.gridLayout, 0)
		self.allLayout.setContentsMargins(2, 2, 2, 2)
		self.setLayout(self.allLayout)

		# set font
		font = QtGui.QFont()
		font.setPointSize(9)
		# font.setWeight(70)
		font.setBold(True)
		self.text1Label.setFont(font)


	def setText1(self, text) : 
		self.text1Label.setText(text)


	def setText2(self, text) : 
		self.text2Label.setText(text)


	def setText3(self, text) : 
		self.text3Label.setText(text)


	def setText4(self, text) : 
		self.text4Label.setText(text)


	def setTextColor1(self, color) : 
		self.text1Label.setStyleSheet('color: rgb(%s, %s, %s);' % (color[0], color[1], color[2]))


	def setTextColor2(self, color) : 
		self.text2Label.setStyleSheet('color: rgb(%s, %s, %s);' % (color[0], color[1], color[2]))


	def setTextColor3(self, color) : 
		self.text3Label.setStyleSheet('color: rgb(%s, %s, %s);' % (color[0], color[1], color[2]))


	def setIcon(self, iconPath, size) : 
		self.iconQLabel.setPixmap(QtGui.QPixmap(iconPath).scaled(size, size, QtCore.Qt.KeepAspectRatio))


	def text1(self) : 
		return self.text1Label.text()


	def text2(self) : 
		return self.text2Label.text()


	def text3(self) : 
		return self.text3Label.text()


class customQWidgetItem2(QtGui.QWidget) : 
	def __init__(self, parent = None) : 
		super(customQWidgetItem2, self).__init__(parent)
		# set label 
		self.textQVBoxLayout = QtGui.QVBoxLayout()
		self.text1Label = QtGui.QLabel()
		# self.text2Label = QtGui.QLabel()

		self.textQVBoxLayout.addWidget(self.text1Label)
		# self.textQVBoxLayout.addWidget(self.text2Label)

		# set icon
		self.allLayout = QtGui.QHBoxLayout()
		self.iconQLabel = QtGui.QLabel()
		self.allLayout.addWidget(self.iconQLabel, 0)
		self.allLayout.addLayout(self.textQVBoxLayout, 1)
		self.allLayout.setContentsMargins(2, 2, 2, 2)
		self.setLayout(self.allLayout)

		# set font
		font = QtGui.QFont()
		font.setPointSize(9)
		# font.setWeight(70)
		# font.setBold(True)
		self.text1Label.setFont(font)


	def setText1(self, text) : 
		self.text1Label.setText(text)


	# def setText2(self, text) : 
	# 	self.text2Label.setText(text)


	def setTextColor1(self, color) : 
		self.text1Label.setStyleSheet('color: rgb(%s, %s, %s);' % (color[0], color[1], color[2]))


	# def setTextColor2(self, color) : 
	# 	self.text2Label.setStyleSheet('color: rgb(%s, %s, %s);' % (color[0], color[1], color[2]))


	def setIcon(self, iconPath, size) : 
		self.iconQLabel.setPixmap(QtGui.QPixmap(iconPath).scaled(size, size, QtCore.Qt.KeepAspectRatio))


	def text1(self) : 
		return self.text1Label.text()


	# def text2(self) : 
	# 	return self.text2Label.text()


