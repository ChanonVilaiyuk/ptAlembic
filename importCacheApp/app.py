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

		# instance projectInfo 
		self.projectInfo = projectInfo.info()
		self.shotInfo = entityInfo.info()

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

		self.setProjectComboBox()
		self.setAutoComboBox()


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





	# setting area 
	# =========================================================================================



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