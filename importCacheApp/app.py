# alembic export app

#Import python modules
import sys, os, re, shutil, yaml
import subprocess
from datetime import datetime
import time

from functools import partial

#Import GUI
from PySide import QtCore
from PySide import QtGui

from shiboken import wrapInstance

from tool.ptAlembic.importCacheApp import importUI as ui
reload(ui)

from tool.ptAlembic import mayaHook as hook
reload(hook)

from tool.ptAlembic import abcExport, setting
reload(abcExport)
reload(setting)

moduleDir = sys.modules[__name__].__file__


from tool.utils import pipelineTools 
reload(pipelineTools)

from tool.utils import fileUtils, entityInfo, projectInfo
reload(fileUtils)
reload(entityInfo)
reload(projectInfo)

# logger 
from tool.utils import customLog
reload(customLog)

scriptName = 'ptAlembicImport'
logger = customLog.customLog()
logger.setLevel(customLog.DEBUG)
logger.setLogName(scriptName)

abcExport.logger.setLevel(customLog.DEBUG)
abcExport.logger.setLogName(scriptName)


# If inside Maya open Maya GUI
def getMayaWindow():
	ptr = mui.MQtUtil.mainWindow()
	return wrapInstance(long(ptr), QtGui.QWidget)
	# return sip.wrapinstance(long(ptr), QObject)

import maya.OpenMayaUI as mui
getMayaWindow()


class MyForm(QtGui.QMainWindow):

	def __init__(self, parent=None):
		self.count = 0
		#Setup Window
		super(MyForm, self).__init__(parent)
		# QtGui.QWidget.__init__(self, parent)
		self.ui = ui.Ui_AlembicImportWin()
		self.ui.setupUi(self)

		# hook.logger.setLogFile(logPath, True)
		# hook.logger.setLevel('INFO')
		# hook.logger.setLogName(scriptName)

		# icons
		self.logo = '%s/%s' % (os.path.dirname(moduleDir), 'icons/logo.png')
		self.logo2 = '%s/%s' % (os.path.dirname(moduleDir), 'icons/alembic_logo.png')
		self.okIcon = '%s/%s' % (os.path.dirname(moduleDir), 'icons/ok_icon.png')
		self.xIcon = '%s/%s' % (os.path.dirname(moduleDir), 'icons/x_icon.png')
		self.rdyIcon = '%s/%s' % (os.path.dirname(moduleDir), 'icons/rdy_icon.png')
		self.ipIcon = '%s/%s' % (os.path.dirname(moduleDir), 'icons/ip_icon.png')
		self.refreshIcon = '%s/%s' % (os.path.dirname(moduleDir), 'icons/refresh_icon.png')
		self.iconSize = 15
		

		# group 
		self.cacheGrp = 'Geo_Grp'
		self.assetInfo = dict()
		self.cacheAssetTypeList = ['character', 'prop', 'animal']
		self.normalAsset = '[asset]'
		self.nonCacheAsset = 'exportGrp'

		# table column
		self.cacheListCol = 0
		self.inSceneCol = 1
		self.lodCol = 2 
		self.currentVersionCol = 3
		self.serverVersionCol = 4
		self.statusCol = 5


		# instance projectInfo 
		self.projectInfo = projectInfo.info()
		self.shotInfo = entityInfo.info()
		self.setting = setting.cachePathInfo()
		self.cacheData = None
		self.defaultAssetLevel = 'Cache'

		# shot variable 
		self.project = None 
		self.episode = None
		self.sequence = None 
		self.shot = None 
		self.step = None

		# path 
		self.animCurvePath = None

		# start functions 
		self.initSignal()
		self.initData()


	def initSignal(self) : 
		# project comboBox
		self.ui.project_comboBox.currentIndexChanged.connect(self.setEpisodeComboBox)
		self.ui.episode_comboBox.currentIndexChanged.connect(self.setSequenceComboBox)
		self.ui.sequence_comboBox.currentIndexChanged.connect(self.setShotComboBox)
		self.ui.shot_comboBox.currentIndexChanged.connect(self.setData)

		self.ui.cache_comboBox.currentIndexChanged.connect(self.setCacheList)



	def initData(self) : 
		# set logo UI
		self.setLogo()

		# set button state
		self.setButton()
		
		# call all data and set UI. All critical functions are here
		self.refreshUI()


	def refreshUI(self) : 
		logger.debug('=================')
		logger.debug('Refreshing UI ...')

		self.cacheData = self.readingCacheData()
		self.setProjectComboBox()
		self.setAutoComboBox()
		self.setCacheVersionComboBox()
		# self.setCacheList()


	def setData(self) : 
		self.setSelShotData()


	def setLogo(self) : 
		self.ui.logo_label.setPixmap(QtGui.QPixmap(self.logo).scaled(200, 60, QtCore.Qt.KeepAspectRatio))
		self.ui.logo2_label.setPixmap(QtGui.QPixmap(self.logo2).scaled(200, 60, QtCore.Qt.KeepAspectRatio))


	def setButton(self) : 
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(self.refreshIcon),QtGui.QIcon.Normal,QtGui.QIcon.Off)
		self.ui.refresh_pushButton.setIcon(icon)
		self.ui.refresh2_pushButton.setIcon(icon)


	''' set shot header '''
	def setShotInfo(self) : 
		logger.debug('Setting shot info ...')



	# set project comboBox
	def setProjectComboBox(self, setItem = '') : 
		projects = self.projectInfo.listProjects()

		self.setProjectInfoComboBox('project_comboBox', projects, setItem)
		

	def setEpisodeComboBox(self, setItem = '') : 
		project = str(self.ui.project_comboBox.currentText())
		episodes = self.projectInfo.listEpisodes(project)

		self.setProjectInfoComboBox('episode_comboBox', episodes, setItem)

	def setSequenceComboBox(self, setItem = '') : 
		project = str(self.ui.project_comboBox.currentText())
		episode = str(self.ui.episode_comboBox.currentText())
		sequences = self.projectInfo.listSequences(project, episode)

		self.setProjectInfoComboBox('sequence_comboBox', sequences, setItem)

	def setShotComboBox(self, setItem = '') : 
		project = str(self.ui.project_comboBox.currentText())
		episode = str(self.ui.episode_comboBox.currentText())
		sequence = str(self.ui.sequence_comboBox.currentText())
		shots = self.projectInfo.listShots(project, episode, sequence)

		self.setProjectInfoComboBox('shot_comboBox', shots, setItem)


	def setProjectInfoComboBox(self, comboBox, items, setItem) : 
		i = 0 
		index = 0

		cmd = 'self.ui.%s.clear()' % comboBox
		eval(cmd)

		for each in items : 
			cmd = 'self.ui.%s.addItem(each)' % comboBox
			eval(cmd)

			if setItem : 
				if setItem == each : 
					index = i 

			i += 1 
		
		cmd = 'self.ui.%s.setCurrentIndex(%s)' % (comboBox, index)
		eval(cmd)


	def setAutoComboBox(self) : 
		# get current shot data 
		currentProject = self.shotInfo.getProject()
		currentEpisode = self.shotInfo.getEpisode()
		currentSequence = self.shotInfo.getSequence()
		currentShot = self.shotInfo.getShotName()

		# set comboBox
		self.setProjectComboBox(currentProject)
		self.setEpisodeComboBox(currentEpisode)
		self.setSequenceComboBox(currentSequence)
		self.setShotComboBox(currentShot)


	def setSelShotData(self) : 
		# set shotData
		self.project = str(self.ui.project_comboBox.currentText())
		self.episode = str(self.ui.episode_comboBox.currentText())
		self.sequence = str(self.ui.sequence_comboBox.currentText())
		self.shot = str(self.ui.shot_comboBox.currentText())

		# logger.debug('Set shot data %s %s %s %s' % (self.project, self.episode, self.sequence, self.shot))


	# set cache list widget 
	def setCacheVersionComboBox(self) : 
		assetVersions = self.findAssetVersions()
		self.ui.cache_comboBox.clear()

		i = 0 
		index = 0
		if assetVersions : 
			for each in assetVersions : 
				self.ui.cache_comboBox.addItem(each)

				if each == self.defaultAssetLevel : 
					index = i 

				i += 1 

		self.ui.cache_comboBox.setCurrentIndex(index)


	def setCacheList(self) : 
		# self.cacheData from def refreshUI
		if self.cacheData : 

			# input from UI
			cacheVersion = str(self.ui.cache_comboBox.currentText())
			
			# fix variable 
			row = 0 
			height = 20
			widget = 'asset_tableWidget'
			color = [120, 0, 0]
			iconPath = self.xIcon
			inScene = 'No'

			# clear table 
			self.clearTable(widget)
			
			for each in self.cacheData.keys() : 

				# set data 
				assetName = each 

				# This asset path will return absolute path 
				# ex. P:/Lego_Friends2015/asset/3D/character/main/frd_stephanieSchool/ref/frd_stephanieSchool_Cache.ma
				# this tool will override this path to selected cache version from UI -> Render / Cache
				# to modify --> O:\studioTools\maya\python\tool\ptAlembic\abcExport.py func getShaderPath()

				assetPath = self.cacheData[each]['assetPath']

				# comment this line to use default asset path 
				assetPath = '%s/%s_%s.mb' % (os.path.dirname(assetPath), assetName, cacheVersion)

				# check asset exists 
				if os.path.exists(assetPath) : 
					color = [0, 120, 0]

				# check asset exists in scene 
				if hook.objectExists('%s:%s' % (assetName, self.cacheGrp)) : 
					inScene = 'Yes'
					iconPath = self.okIcon

				# raed cache version from yml file
				cachePath = self.cacheData[each]['cachePath']
				version = os.path.dirname(cachePath).split('/')[-1]


				# cache version by striping end of the asset path 
				cacheVersion = assetPath.split('.')[0].split('_')[-1]

				# set cache list UI
				self.insertRow(row, height, widget)
				self.fillInTable(row, self.cacheListCol, assetName, widget, color)
				self.fillInTableIcon(row, self.inSceneCol, inScene, iconPath, widget, [0, 0, 0])
				self.fillInTable(row, self.lodCol, cacheVersion, widget, [0, 0, 0])
				self.fillInTable(row, self.serverVersionCol, version, widget, [0, 0, 0])

				row += 1


	def checkServerVersion(self, assetName) : 
		pass
	

	def findAssetVersions(self) : 
		assetVersions = []

		if self.cacheData : 
			for each in self.cacheData.keys() : 
				print self.cacheData[each] 
				assetPath = self.cacheData[each]['assetPath']
				assetPathDir = os.path.dirname(assetPath)
				files = fileUtils.listFile(assetPathDir)

				for eachFile in files : 
					assetVersion = eachFile.split('.')[0].split('_')[-1]

					if not assetVersion in assetVersions : 
						assetVersions.append(assetVersion)

		return assetVersions


	# setting area 
	# =========================================================================================
	def readingCacheData(self) : 
		# read asset list 
		if self.setting : 
			dataPath = self.setting['cacheInfoPath']

			if os.path.exists(dataPath) : 
				data = fileUtils.ymlLoader(dataPath)

				return data


	# =========================================================================================
	# log area 
	def addTimeLog(self, inputType, namespace, duration) : 
		path = setting.cachePathInfo()
		timeLogPath = path['timeLogPath']
		namespace = str(namespace)
		duration = str(duration)

		data = dict()

		if os.path.exists(timeLogPath) : 
			data = fileUtils.ymlLoader(timeLogPath)

		if inputType == 'asset' : 
			if inputType in data.keys() : 
				if namespace in data[inputType].keys() : 
					data[inputType][namespace].append(duration)

				else : 
					data[inputType].update({namespace: [duration]})

			else : 
				data.update({inputType: {namespace: [duration]}})

		if inputType == 'shot' : 
			if inputType in data.keys() : 
				data[inputType].append(duration)

			else : 
				data.update({inputType: [duration]})


		self.writeData(timeLogPath, data)


	def addAssetLog(self, namespace, cacheGrp) : 
		path = setting.cachePathInfo()
		assetLogPath = path['assetLogPath']
		assetPath = str(hook.getReferencePath(cacheGrp))
		timeInfo = hook.getShotRange()
		startFrame = timeInfo[0]
		endFrame = timeInfo[1]
		namespace = str(namespace)

		data = dict()
		assetData = dict() 

		if os.path.exists(assetLogPath) : 
			data = fileUtils.ymlLoader(assetLogPath)

		if 'asset' in data.keys() : 
			if namespace in data['asset'].keys() : 
				data['asset'][namespace] = assetPath

			else : 
				data['asset'].update({namespace: assetPath})

		else : 
			data.update({'asset': {namespace: assetPath}})

		if 'duration' in data.keys() : 
			data['duration'].update({'startFrame': startFrame, 'endFrame': endFrame})

		else : 
			data.update({'duration': {'startFrame': startFrame, 'endFrame': endFrame}})

		self.writeData(assetLogPath, data)

	# =========================================================================================
	# utils 



	# =========================================================================================
	# widget area

	def insertRow(self, row, height, widget) : 
		cmd1 = 'self.ui.%s.insertRow(row)' % widget
		cmd2 = 'self.ui.%s.setRowHeight(row, height)' % widget

		eval(cmd1)
		eval(cmd2)


	def fillInTable(self, row, column, text, widget, color = [1, 1, 1]) : 
		item = QtGui.QTableWidgetItem()
		item.setText(text)
		item.setBackground(QtGui.QColor(color[0], color[1], color[2]))
		cmd = 'self.ui.%s.setItem(row, column, item)' % widget
		eval(cmd)


	def fillInTableIcon(self, row, column, text, iconPath, widget, color = [1, 1, 1]) : 
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		item = QtGui.QTableWidgetItem()
		item.setText(str(text))
		item.setIcon(icon)
		item.setBackground(QtGui.QColor(color[0], color[1], color[2]))
		
		cmd = 'self.ui.%s.setItem(row, column, item)' % widget
		eval(cmd)



	def clearTable(self, widget) : 
		cmd = 'self.ui.%s.rowCount()' % widget
		rows = eval(cmd)
		# self.ui.asset_tableWidget.clear()

		for each in range(rows) : 
			cmd2 = 'self.ui.%s.removeRow(0)' % widget
			eval(cmd2)


	def getAllItems(self, listWidget) : 
		count = eval('self.ui.%s.count()' % listWidget)
		itemWidgets = []
		items1 = []
		items2 = []

		for i in range(count) : 
			item = eval('self.ui.%s.item(i)' % listWidget)

			customWidget = eval('self.ui.%s.itemWidget(item)' % listWidget)
			text1 = customWidget.text1()
			text2 = customWidget.text2()

			items1.append(text1)
			items2.append(text2)
			itemWidgets.append(customWidget)


		return [items1, items2, itemWidgets]


	def getSelectedItems(self, listWidget) : 
		items = eval('self.ui.%s.selectedItems()' % listWidget)
		items1 = []
		items2 = []
		itemWidgets = []

		if items : 
			for eachItem in items : 
				customWidget = eval('self.ui.%s.itemWidget(eachItem)' % listWidget)
				text1 = customWidget.text1()
				text2 = customWidget.text2()

				items1.append(text1)
				items2.append(text2)
				itemWidgets.append(customWidget)

			return [items1, items2, itemWidgets]



	def getColumnData(self, column) : 
		counts = self.ui.asset_tableWidget.rowCount()
		data = []

		for i in range(counts) : 
			item = self.ui.asset_tableWidget.item(i, column)
			if item : 
				data.append(str(item.text()))

		return data 


	def getDataFromSelectedRange(self, columnNumber) : 
		lists = self.ui.asset_tableWidget.selectedRanges()

		if lists : 
			topRow = lists[0].topRow()
			bottomRow = lists[0].bottomRow()
			leftColumn = lists[0].leftColumn()
			rightColumn = lists[0].rightColumn()

			items = []

			for i in range(topRow, bottomRow + 1) : 
				item = str(self.ui.asset_tableWidget.item(i, columnNumber).text())
				items.append(item)


			return items


	def messageBox(self, title, description) : 
		result = QtGui.QMessageBox.question(self,title,description ,QtGui.QMessageBox.Ok)

		return result