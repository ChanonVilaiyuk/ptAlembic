# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'O:\studioTools\maya\python\tool\ptAlembic\importCacheApp\importUI.ui'
#
# Created: Fri Jan 08 20:41:28 2016
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from qtshim import QtCore, QtGui
from qtshim import Signal
from qtshim import wrapinstance


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AlembicImportWin(object):
    def setupUi(self, AlembicImportWin):
        AlembicImportWin.setObjectName(_fromUtf8("AlembicImportWin"))
        AlembicImportWin.resize(503, 815)
        self.centralwidget = QtGui.QWidget(AlembicImportWin)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_5 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.project_comboBox = QtGui.QComboBox(self.frame)
        self.project_comboBox.setObjectName(_fromUtf8("project_comboBox"))
        self.gridLayout.addWidget(self.project_comboBox, 0, 1, 1, 1)
        self.sequence_comboBox = QtGui.QComboBox(self.frame)
        self.sequence_comboBox.setObjectName(_fromUtf8("sequence_comboBox"))
        self.gridLayout.addWidget(self.sequence_comboBox, 2, 1, 1, 1)
        self.label = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)
        self.shot_comboBox = QtGui.QComboBox(self.frame)
        self.shot_comboBox.setObjectName(_fromUtf8("shot_comboBox"))
        self.gridLayout.addWidget(self.shot_comboBox, 4, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.episode_comboBox = QtGui.QComboBox(self.frame)
        self.episode_comboBox.setObjectName(_fromUtf8("episode_comboBox"))
        self.gridLayout.addWidget(self.episode_comboBox, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.logo2_label = QtGui.QLabel(self.frame)
        self.logo2_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.logo2_label.setObjectName(_fromUtf8("logo2_label"))
        self.horizontalLayout_2.addWidget(self.logo2_label)
        self.logo_label = QtGui.QLabel(self.frame)
        self.logo_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.logo_label.setObjectName(_fromUtf8("logo_label"))
        self.horizontalLayout_2.addWidget(self.logo_label)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_6.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtGui.QFrame.Box)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setContentsMargins(9, 2, 9, 2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_10 = QtGui.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_3.addWidget(self.label_10)
        self.asset_tableWidget = QtGui.QTableWidget(self.frame_2)
        self.asset_tableWidget.setMinimumSize(QtCore.QSize(0, 200))
        self.asset_tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.asset_tableWidget.setObjectName(_fromUtf8("asset_tableWidget"))
        self.asset_tableWidget.setColumnCount(8)
        self.asset_tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.asset_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.asset_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.asset_tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.asset_tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.asset_tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.asset_tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.asset_tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.asset_tableWidget.setHorizontalHeaderItem(7, item)
        self.asset_tableWidget.horizontalHeader().setVisible(True)
        self.asset_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.asset_tableWidget.horizontalHeader().setDefaultSectionSize(106)
        self.asset_tableWidget.horizontalHeader().setHighlightSections(True)
        self.asset_tableWidget.verticalHeader().setVisible(True)
        self.verticalLayout_3.addWidget(self.asset_tableWidget)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.all_checkBox = QtGui.QCheckBox(self.frame_2)
        self.all_checkBox.setChecked(True)
        self.all_checkBox.setObjectName(_fromUtf8("all_checkBox"))
        self.horizontalLayout_5.addWidget(self.all_checkBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.label_3 = QtGui.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.cache_comboBox = QtGui.QComboBox(self.frame_2)
        self.cache_comboBox.setObjectName(_fromUtf8("cache_comboBox"))
        self.horizontalLayout_5.addWidget(self.cache_comboBox)
        self.refresh_pushButton = QtGui.QPushButton(self.frame_2)
        self.refresh_pushButton.setObjectName(_fromUtf8("refresh_pushButton"))
        self.horizontalLayout_5.addWidget(self.refresh_pushButton)
        self.horizontalLayout_5.setStretch(2, 1)
        self.horizontalLayout_5.setStretch(3, 2)
        self.horizontalLayout_5.setStretch(4, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 6)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_6.addWidget(self.frame_2)
        self.frame_3 = QtGui.QFrame(self.centralwidget)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 140))
        self.frame_3.setFrameShape(QtGui.QFrame.Box)
        self.frame_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.rebuildAsset_pushButton = QtGui.QPushButton(self.frame_3)
        self.rebuildAsset_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.rebuildAsset_pushButton.setPalette(palette)
        self.rebuildAsset_pushButton.setObjectName(_fromUtf8("rebuildAsset_pushButton"))
        self.gridLayout_2.addWidget(self.rebuildAsset_pushButton, 1, 0, 1, 1)
        self.removeAsset_pushButton = QtGui.QPushButton(self.frame_3)
        self.removeAsset_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(156, 70, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(156, 70, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(156, 70, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.removeAsset_pushButton.setPalette(palette)
        self.removeAsset_pushButton.setObjectName(_fromUtf8("removeAsset_pushButton"))
        self.gridLayout_2.addWidget(self.removeAsset_pushButton, 3, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_12 = QtGui.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_7.addWidget(self.label_12)
        self.assetVersion_comboBox = QtGui.QComboBox(self.frame_3)
        self.assetVersion_comboBox.setObjectName(_fromUtf8("assetVersion_comboBox"))
        self.horizontalLayout_7.addWidget(self.assetVersion_comboBox)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 2)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 4, 0, 1, 1)
        self.horizontalLayout_6.addLayout(self.gridLayout_2)
        self.line_3 = QtGui.QFrame(self.frame_3)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.horizontalLayout_6.addWidget(self.line_3)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.importCache_pushButton = QtGui.QPushButton(self.frame_3)
        self.importCache_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.importCache_pushButton.setPalette(palette)
        self.importCache_pushButton.setObjectName(_fromUtf8("importCache_pushButton"))
        self.gridLayout_6.addWidget(self.importCache_pushButton, 1, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_6.addWidget(self.label_13, 0, 0, 1, 1)
        self.removeCache_pushButton = QtGui.QPushButton(self.frame_3)
        self.removeCache_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(156, 70, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(156, 70, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(156, 70, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.removeCache_pushButton.setPalette(palette)
        self.removeCache_pushButton.setObjectName(_fromUtf8("removeCache_pushButton"))
        self.gridLayout_6.addWidget(self.removeCache_pushButton, 2, 0, 1, 1)
        self.label_14 = QtGui.QLabel(self.frame_3)
        self.label_14.setText(_fromUtf8(""))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_6.addWidget(self.label_14, 3, 0, 1, 1)
        self.gridLayout_6.setRowStretch(0, 1)
        self.gridLayout_6.setRowStretch(1, 1)
        self.gridLayout_6.setRowStretch(2, 1)
        self.gridLayout_6.setRowStretch(3, 2)
        self.horizontalLayout_6.addLayout(self.gridLayout_6)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.horizontalLayout_6.setStretch(2, 1)
        self.verticalLayout_6.addWidget(self.frame_3)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.frame_4 = QtGui.QFrame(self.centralwidget)
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 240))
        self.frame_4.setFrameShape(QtGui.QFrame.Box)
        self.frame_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_9 = QtGui.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout.addWidget(self.label_9)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.nonCache_tableWidget = QtGui.QTableWidget(self.frame_4)
        self.nonCache_tableWidget.setMinimumSize(QtCore.QSize(0, 100))
        self.nonCache_tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.nonCache_tableWidget.setObjectName(_fromUtf8("nonCache_tableWidget"))
        self.nonCache_tableWidget.setColumnCount(2)
        self.nonCache_tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.nonCache_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.nonCache_tableWidget.setHorizontalHeaderItem(1, item)
        self.nonCache_tableWidget.horizontalHeader().setVisible(True)
        self.nonCache_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.nonCache_tableWidget.horizontalHeader().setDefaultSectionSize(106)
        self.nonCache_tableWidget.horizontalHeader().setHighlightSections(True)
        self.nonCache_tableWidget.verticalHeader().setVisible(True)
        self.verticalLayout_2.addWidget(self.nonCache_tableWidget)
        self.refresh2_pushButton = QtGui.QPushButton(self.frame_4)
        self.refresh2_pushButton.setObjectName(_fromUtf8("refresh2_pushButton"))
        self.verticalLayout_2.addWidget(self.refresh2_pushButton)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.all2_checkBox = QtGui.QCheckBox(self.frame_4)
        self.all2_checkBox.setChecked(True)
        self.all2_checkBox.setObjectName(_fromUtf8("all2_checkBox"))
        self.gridLayout_3.addWidget(self.all2_checkBox, 0, 0, 1, 1)
        self.importNonCache_pushButton = QtGui.QPushButton(self.frame_4)
        self.importNonCache_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.importNonCache_pushButton.setPalette(palette)
        self.importNonCache_pushButton.setObjectName(_fromUtf8("importNonCache_pushButton"))
        self.gridLayout_3.addWidget(self.importNonCache_pushButton, 1, 0, 1, 1)
        self.removeNonCache_pushButton = QtGui.QPushButton(self.frame_4)
        self.removeNonCache_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(156, 70, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(156, 70, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(156, 70, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.removeNonCache_pushButton.setPalette(palette)
        self.removeNonCache_pushButton.setObjectName(_fromUtf8("removeNonCache_pushButton"))
        self.gridLayout_3.addWidget(self.removeNonCache_pushButton, 1, 1, 1, 1)
        self.importCamera_pushButton = QtGui.QPushButton(self.frame_4)
        self.importCamera_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 60, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.importCamera_pushButton.setPalette(palette)
        self.importCamera_pushButton.setObjectName(_fromUtf8("importCamera_pushButton"))
        self.gridLayout_3.addWidget(self.importCamera_pushButton, 1, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_8.addWidget(self.frame_4)
        self.frame_5 = QtGui.QFrame(self.centralwidget)
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 240))
        self.frame_5.setFrameShape(QtGui.QFrame.Box)
        self.frame_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.frame_5)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_11 = QtGui.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.verticalLayout_5.addWidget(self.label_11)
        self.status_listWidget = QtGui.QListWidget(self.frame_5)
        self.status_listWidget.setObjectName(_fromUtf8("status_listWidget"))
        self.verticalLayout_5.addWidget(self.status_listWidget)
        self.horizontalLayout_8.addWidget(self.frame_5)
        self.horizontalLayout_8.setStretch(1, 1)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        AlembicImportWin.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AlembicImportWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 503, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        AlembicImportWin.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(AlembicImportWin)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        AlembicImportWin.setStatusBar(self.statusbar)

        self.retranslateUi(AlembicImportWin)
        QtCore.QMetaObject.connectSlotsByName(AlembicImportWin)

    def retranslateUi(self, AlembicImportWin):
        AlembicImportWin.setWindowTitle(QtGui.QApplication.translate("AlembicImportWin", "PT Alembic Cache Import v.1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("AlembicImportWin", "Sequence : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AlembicImportWin", "Project : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("AlembicImportWin", "Shot : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("AlembicImportWin", "Episode : ", None, QtGui.QApplication.UnicodeUTF8))
        self.logo2_label.setText(QtGui.QApplication.translate("AlembicImportWin", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.logo_label.setText(QtGui.QApplication.translate("AlembicImportWin", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("AlembicImportWin", "Cache Assets", None, QtGui.QApplication.UnicodeUTF8))
        item = self.asset_tableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("AlembicImportWin", "Cache List", None, QtGui.QApplication.UnicodeUTF8))
        item = self.asset_tableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("AlembicImportWin", "In Scene", None, QtGui.QApplication.UnicodeUTF8))
        item = self.asset_tableWidget.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("AlembicImportWin", "LOD", None, QtGui.QApplication.UnicodeUTF8))
        item = self.asset_tableWidget.horizontalHeaderItem(3)
        item.setText(QtGui.QApplication.translate("AlembicImportWin", "Current Version", None, QtGui.QApplication.UnicodeUTF8))
        item = self.asset_tableWidget.horizontalHeaderItem(4)
        item.setText(QtGui.QApplication.translate("AlembicImportWin", "Publish Version", None, QtGui.QApplication.UnicodeUTF8))
        item = self.asset_tableWidget.horizontalHeaderItem(5)
        item.setText(QtGui.QApplication.translate("AlembicImportWin", "Status", None, QtGui.QApplication.UnicodeUTF8))
        item = self.asset_tableWidget.horizontalHeaderItem(6)
        item.setText(QtGui.QApplication.translate("AlembicImportWin", "Asset Path", None, QtGui.QApplication.UnicodeUTF8))
        item = self.asset_tableWidget.horizontalHeaderItem(7)
        item.setText(QtGui.QApplication.translate("AlembicImportWin", "Geo_Grp", None, QtGui.QApplication.UnicodeUTF8))
        self.all_checkBox.setText(QtGui.QApplication.translate("AlembicImportWin", "Apply to All in List", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AlembicImportWin", "Cache Version", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh_pushButton.setText(QtGui.QApplication.translate("AlembicImportWin", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.rebuildAsset_pushButton.setText(QtGui.QApplication.translate("AlembicImportWin", "1. Rebuild Asset", None, QtGui.QApplication.UnicodeUTF8))
        self.removeAsset_pushButton.setText(QtGui.QApplication.translate("AlembicImportWin", "Remove Asset", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("AlembicImportWin", "Asset", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("AlembicImportWin", "Rebuild Version", None, QtGui.QApplication.UnicodeUTF8))
        self.importCache_pushButton.setText(QtGui.QApplication.translate("AlembicImportWin", "2. Import / Update Cache", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("AlembicImportWin", "Import Cache", None, QtGui.QApplication.UnicodeUTF8))
        self.removeCache_pushButton.setText(QtGui.QApplication.translate("AlembicImportWin", "Remove Cache", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("AlembicImportWin", "Non Cache Assets", None, QtGui.QApplication.UnicodeUTF8))
        item = self.nonCache_tableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("AlembicImportWin", "Non Cache List", None, QtGui.QApplication.UnicodeUTF8))
        item = self.nonCache_tableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("AlembicImportWin", "In Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh2_pushButton.setText(QtGui.QApplication.translate("AlembicImportWin", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.all2_checkBox.setText(QtGui.QApplication.translate("AlembicImportWin", "Apply to All in List", None, QtGui.QApplication.UnicodeUTF8))
        self.importNonCache_pushButton.setText(QtGui.QApplication.translate("AlembicImportWin", "Import Non Cache", None, QtGui.QApplication.UnicodeUTF8))
        self.removeNonCache_pushButton.setText(QtGui.QApplication.translate("AlembicImportWin", "Remove Non Cache", None, QtGui.QApplication.UnicodeUTF8))
        self.importCamera_pushButton.setText(QtGui.QApplication.translate("AlembicImportWin", "Import Camera", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("AlembicImportWin", "Status", None, QtGui.QApplication.UnicodeUTF8))

