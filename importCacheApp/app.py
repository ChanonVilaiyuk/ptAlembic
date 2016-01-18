''' version note 
v001 - start version 

'''
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

from tool.ptAlembic import abcExport, setting, abcImport
reload(abcExport)
reload(setting)
reload(abcImport)

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

abcImport.logger.setLevel(customLog.DEBUG)
abcImport.logger.setLogName(scriptName)


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

		# set version
		self.setWindowTitle('PT Alembic Cache Import v.1.0')

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
		self.publishVersionCol = 4
		self.statusCol = 5
		self.assetPathCol = 6
		self.cacheGrpCol = 7
		self.hierarchyCol = 8

		self.nonCacheListCol = 0
		self.nonCahceInSceneCol = 1


		# instance projectInfo 
		self.projectInfo = projectInfo.info()
		self.shotInfo = entityInfo.info()
		self.setting = None
		self.cacheData = None
		self.defaultAssetLevel = 'Cache'
		self.cacheAssetInfo = dict()

		# shot variable 
		self.project = None 
		self.episode = None
		self.sequence = None 
		self.shot = None 
		self.step = None
		self.dept = 'light'

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
		self.ui.shot_comboBox.currentIndexChanged.connect(self.refreshUI)
		self.ui.assetVersion_comboBox.currentIndexChanged.connect(self.setCacheList)

		# button 
		self.ui.rebuildAsset_pushButton.clicked.connect(self.doRebuildAsset)
		self.ui.importCache_pushButton.clicked.connect(self.doApplyCache)
		self.ui.refresh_pushButton.clicked.connect(self.refreshUI)
		self.ui.importCamera_pushButton.clicked.connect(self.doImportCamera)
		self.ui.importNonCache_pushButton.clicked.connect(self.doImportNonCache)
		self.ui.removeAsset_pushButton.clicked.connect(self.doRemoveCacheAsset)
		self.ui.removeCache_pushButton.clicked.connect(self.doRemoveCacheNode)
		self.ui.removeNonCache_pushButton.clicked.connect(self.doRemoveNonCacheAsset)



	def initData(self) : 
		# set logo UI
		self.setLogo()

		# set button state
		self.setButton()

		# call all data and set UI. All critical functions are here
		self.setDataUI()

		# customized column
		self.showHideColumn()

		# check status 
		self.checkDataStatus()


	def setDataUI(self) : 
		self.setProjectComboBox()
		self.setAutoComboBox()
		self.refreshUI()
		


	def showHideColumn(self) : 
		self.ui.asset_tableWidget.setColumnHidden(self.publishVersionCol, 1)
		self.ui.asset_tableWidget.setColumnHidden(self.assetPathCol, 1)
		self.ui.asset_tableWidget.setColumnHidden(self.cacheGrpCol, 1)
		self.ui.asset_tableWidget.setColumnHidden(self.lodCol, 1)


	def refreshUI(self) : 
		logger.debug('=================')
		logger.debug('Refreshing UI ...')
		self.setSelShotData()
		self.setting = setting.cachePathInfo(True, self.project, self.episode, self.sequence, self.shot, self.dept)
		self.cacheData = self.readingCacheData()
		self.cacheVersions = self.collectCacheVersion()
		self.setCacheList()
		self.setNonCacheList()
		self.setLodComboBox()



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
		if self.shotInfo : 
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


	def setLodComboBox(self) :  
		data = self.cacheData 
		lods = []

		if data : 
			for each in data : 
				assetName = each 
				assetPath = data[each]['assetPath']
				assetDir = os.path.dirname(assetPath)

				files = fileUtils.listFile(assetDir)

				for eachFile in files : 
					lod = eachFile.split('_')[-1]

					if not lod in lods : 
						lods.append(lod)

			self.ui.assetVersion_comboBox.addItems(lods)

			# set default 
			# remove this line, if using data 
			default = 'Cache.mb'
			if default in lods : 
				index = lods.index(default)
				self.ui.assetVersion_comboBox.setCurrentIndex(index)



	def setCacheList(self) : 
		# self.cacheData from def refreshUI
		# clear table 
		widget = 'asset_tableWidget'
		self.clearTable(widget)

		self.statuses = []
		assetMissing = []

		if self.cacheData : 
			
			# fix variable 
			row = 0 
			height = 20
			
			for each in self.cacheData.keys() : 

				# set data 
				assetName = each 
				iconPath = self.xIcon
				inScene = 'No'
				color = [120, 0, 0]
			
				status = 'Not Match'
				statusIcon = self.xIcon
				statusColor = [60, 0, 0]

				# This asset path will return absolute path 
				# ex. P:/Lego_Friends2015/asset/3D/character/main/frd_stephanieSchool/ref/frd_stephanieSchool_Cache.ma
				# this tool will override this path to selected cache version from UI -> Render / Cache
				# to modify --> O:\studioTools\maya\python\tool\ptAlembic\abcExport.py func getShaderPath()

				assetPath = self.cacheData[each]['assetPath']
				lod = str(self.ui.assetVersion_comboBox.currentText())

				# comment this line to use default asset path 
				assetPath = assetPath.replace('Cache.ma', lod)

				# check asset exists 
				if os.path.exists(assetPath) : 
					color = [0, 120, 0]

				else : 
					self.statuses.append(['Missing %s' % assetName, self.xIcon])
					assetMissing.append(assetName)

				# check asset exists in scene 
				cacheGrp = self.cacheData[each]['cacheGrp']
				if hook.objectExists(cacheGrp) : 
					inScene = 'Yes'
					iconPath = self.okIcon

				# raed cache version from yml file
				cachePath = self.cacheData[each]['cachePath']
				publishVersion = os.path.dirname(cachePath).split('/')[-1]

				# check existing cache version 
				cacheLod = '-'
				currentAbcVersion = '-'

				if assetName in self.cacheVersions.keys() : 
					currentAbcVersion = self.findCurrentAbcVersion(assetName)


				# set status
				if not currentAbcVersion : 
					status = 'Cache not apply'
					statusColor = [60, 0, 0]

				if currentAbcVersion == publishVersion : 
					status = 'Good'
					statusIcon = self.okIcon
					statusColor = [0, 0, 0]


				# check asset hierarchy 
				assetDataPath = self.setting['assetDataPath']
				assetDataFile = '%s/%s.yml' % (assetDataPath, assetName)
				result = pipelineTools.checkHierarchyData(cacheGrp, assetDataFile)

				hStatus = 'Good'
				hStatusIcon = self.okIcon 

				if result : 
					hStatus = 'Warning'
					hStatusIcon = self.xIcon



				# cache version by striping end of the asset path (Cache)
				cacheLod = assetPath.split('.')[0].split('_')[-1]

				# set cache list UI
				self.insertRow(row, height, widget)
				self.fillInTable(row, self.cacheListCol, assetName, widget, color)
				self.fillInTableIcon(row, self.inSceneCol, inScene, iconPath, widget, [0, 0, 0])
				self.fillInTable(row, self.lodCol, cacheLod, widget, [0, 0, 0])
				self.fillInTableIcon(row, self.statusCol, status, statusIcon, widget, statusColor)
				# self.fillInTable(row, self.currentVersionCol, currentAbcVersion, widget, [0, 0, 0])
				self.fillInTable(row, self.publishVersionCol, publishVersion, widget, [0, 0, 0])
				self.fillInTable(row, self.assetPathCol, assetPath, widget, [0, 0, 0])
				self.fillInTable(row, self.cacheGrpCol, cacheGrp, widget, [0, 0, 0])
				self.fillInTableIcon(row, self.hierarchyCol, hStatus, hStatusIcon, widget, [0, 0, 0])

				
				# add comboBox to current version
				# get all versions 
				comboBox = QtGui.QComboBox()
				versionItems = self.cacheVersions[assetName]['versions']
				comboBox.addItems(versionItems)

				# set current version 
				if currentAbcVersion in versionItems : 
					index = versionItems.index(currentAbcVersion)
					comboBox.setCurrentIndex(index)



				# set signal 
				comboBox.currentIndexChanged.connect(partial(self.applyCacheVersion, row, comboBox))
				# comboBox.currentIndexChanged.connect(lambdapartial(self.applyCacheVersion, index, row))
				self.ui.asset_tableWidget.setCellWidget(row, self.currentVersionCol, comboBox)

				row += 1

			if not assetMissing : 
				self.statuses.append(['Asset OK', self.okIcon])



	def setNonCacheList(self) : 
		# read data 
		if self.setting : 
			nonCacheDataFile = self.setting['nonCacheDataPath']
			widget = 'nonCache_tableWidget'
			self.clearTable(widget)

			if os.path.exists(nonCacheDataFile) : 
				data = fileUtils.ymlLoader(nonCacheDataFile)

				row = 0
				height = 20
				for each in data : 
					assetName = each 
					exportGrp = data[each]['exportGrp']
					filePath = data[each]['filePath']
					status = 'No'
					statusIcon = self.xIcon

					if hook.objectExists(exportGrp) : 
						status = 'Yes'
						statusIcon = self.okIcon

					self.insertRow(row, height, widget)
					self.fillInTable(row, self.nonCacheListCol, assetName, widget, [0, 0, 0])
					self.fillInTableIcon(row, self.nonCahceInSceneCol, status, statusIcon, widget, [0, 0, 0])

					row += 1 
	

	def collectCacheVersion(self) : 
		versions = []

		if self.setting : 
			cachePath = self.setting['cachePath']
			cacheInfo = dict()

			if os.path.exists(cachePath) : 
				versions = fileUtils.listFolder(cachePath)

				for version in versions : 
					files = fileUtils.listFile(os.path.join(cachePath, version))
					assetNames = [os.path.splitext(a)[0] for a in files]

					i = 0 
					for eachFile in assetNames : 
						assetName = eachFile 

						if not assetName in cacheInfo.keys() : 
							cacheInfo.update({assetName: {'versions': [version], 'versionKey': {version: os.path.join(cachePath, version, files[i])}}})

						else : 
							cacheInfo[assetName]['versions'].append(version)
							cacheInfo[assetName]['versionKey'].update({version: os.path.join(cachePath, version, files[i])})

						i += 1 


			return cacheInfo


	def findCurrentAbcVersion(self, assetName) : 
		# find current version 

		cacheGrp = self.cacheData[assetName]['cacheGrp']
		if hook.objectExists(cacheGrp) : 
			alembicNode = hook.getAlembicNode(cacheGrp)

			if alembicNode : 
				currentAbcFile = hook.getAlembicPath(alembicNode[0])
				currentAbcVersion = os.path.dirname(currentAbcFile).split('/')[-1]

				return currentAbcVersion



	# setting area 
	# =========================================================================================
	def readingCacheData(self) : 
		# read asset list 
		if self.setting : 
			dataPath = self.setting['cacheInfoPath']

			if os.path.exists(dataPath) : 
				data = fileUtils.ymlLoader(dataPath)

				return data

	# check area 
	# =========================================================================================
	def checkDataStatus(self) : 

		if self.setting : 
			# check camera
			cameraPath = self.setting['cameraPath']
			shotCameraName = self.setting['shotCameraName']

			camMessage = ['No Camera File', self.xIcon]
			if os.path.exists(cameraPath) : 
				self.ui.importCamera_pushButton.setEnabled(True)
				camMessage = ['Camera File Exists', self.okIcon]

			sceneCamMessage = ['No Cam', self.xIcon]
			if hook.objectExists(shotCameraName) : 
				self.ui.importCamera_pushButton.setEnabled(False)
				sceneCamMessage = ['Camera OK', self.okIcon]


			# append data 
			self.statuses.append(camMessage)
			self.statuses.append(sceneCamMessage)

			# set status UI
			self.ui.status_listWidget.clear()
			self.addToolStatus(self.statuses)

	def addToolStatus(self, statuses) : 
		listWidget = 'status_listWidget'
		color = [0, 0, 0]

		for each in statuses : 
			text = each[0]
			status = each[1]

			self.addListWidgetItem(listWidget, text, status, color, 1)



	# button command area
	# =========================================================================================
	def doRebuildAsset(self) : 
		# read asset
		listWidget = 'asset_tableWidget'

		assetNames = self.getTableData(listWidget, self.cacheListCol)
		assetPaths = self.getTableData(listWidget, self.assetPathCol)

		i = 0 
		for i in range(len(assetNames)) : 
			assetName = assetNames[i]
			assetPath = assetPaths[i]
			cacheGrp = self.cacheData[assetNames[i]]['cacheGrp']

			if os.path.exists(assetPath) : 
				if not hook.objectExists(cacheGrp) : 
					hook.createReference(assetName, assetPath)

		self.refreshUI()


	def doApplyCache(self) : 
		logger.debug('run apply cache')
		# read asset
		listWidget = 'asset_tableWidget'
		assetNames = self.getTableData(listWidget, self.cacheListCol)
		alwaysRebuild = True


		for assetName in assetNames : 
			abcFile = self.cacheData[assetName]['cachePath']
			cacheGrp = self.cacheData[assetName]['cacheGrp']

			if os.path.exists(abcFile) and hook.objectExists(cacheGrp) : 
				abcImport.applyCache(cacheGrp, abcFile, alwaysRebuild)
				logger.debug('set cache %s -> %s' % (cacheGrp, abcFile))

			else : 
				logger.debug('%s or %s not exists' % (abcFile, cacheGrp))

		self.refreshUI()


	def doImportNonCache(self) : 
		# import Non Cache 
		logger.debug('run apply non cache')


		# read asset
		listWidget = 'nonCache_tableWidget'
		nonCacheDataFile = self.setting['nonCacheDataPath']
		data = dict()

		if os.path.exists(nonCacheDataFile) : 
			data = fileUtils.ymlLoader(nonCacheDataFile)

		assetNames = self.getTableData(listWidget, self.nonCacheListCol)

		for each in assetNames : 
			assetName = each 
			if data : 
				exportGrp = data[assetName]['exportGrp']
				filePath = data[assetName]['filePath']

				if not hook.objectExists(exportGrp) : 
					if os.path.exists(filePath) : 
						hook.importFile(filePath)

					else : 
						logger.debug('Path does not exists %s' % filePath)

				else : 
					logger.debug('%s already in the scene' % exportGrp)

			else : 
				logger.error('Error check %s' % nonCacheDataFile)

		self.refreshUI()



	def applyCacheVersion(self, row, comboBox, arg = None) : 
		listWidget = 'asset_tableWidget'
		version = str(comboBox.currentText())
		assetNames = self.getColumnData(listWidget, self.cacheListCol)
		assetName = assetNames[row]
		cacheGrp = self.cacheData[assetName]['cacheGrp']
		abcFile = self.cacheVersions[assetName]['versionKey'][version]

		if os.path.exists(abcFile) : 
			# abcImport.logger.setLevel(DEBUG)
			abcImport.applyCache(cacheGrp, abcFile)

		else : 
			logger.debug('abcFile not found %s' % abcFile)
		
		self.refreshUI()


	def doImportCamera(self) : 
		cameraPath = self.setting['cameraPath']
		cameraInfoPath = self.setting['cameraInfoPath']
		shotCameraName = self.setting['shotCameraName']
		cameraInfoPath = self.setting['cameraInfoPath']

		if not hook.objectExists(shotCameraName) : 
			if os.path.exists(cameraPath) : 
				hook.importFile(cameraPath)

		if os.path.exists(cameraInfoPath) : 
			range = fileUtils.ymlLoader(cameraInfoPath)

			if range : 
				currentShot = self.shotInfo.getShotName()
				min = range[currentShot]['startFrame']
				max = range[currentShot]['endFrame']
				hook.setShotRange(min, max)

		self.checkDataStatus()



	def doRemoveCacheAsset(self) : 
		# list
		listWidget = 'asset_tableWidget'
		assetNames = self.getTableData(listWidget, self.nonCacheListCol)

		if self.cacheData : 
			for each in assetNames : 
				namespace = each 
				cacheGrp = self.cacheData[each]['cacheGrp']

				if hook.objectExists(cacheGrp) : 
					alembicNode = hook.getAlembicNode(cacheGrp)

					if hook.objectExists(cacheGrp) : 
						hook.removeReference(cacheGrp)
						hook.removeNamespace(namespace)
						hook.delete(alembicNode)

		self.refreshUI()


	def doRemoveCacheNode(self) : 
		# list
		listWidget = 'asset_tableWidget'
		assetNames = self.getTableData(listWidget, self.nonCacheListCol)

		if self.cacheData : 
			for each in assetNames : 
				cacheGrp = self.cacheData[each]['cacheGrp']
				alembicNode = hook.getAlembicNode(cacheGrp)

				hook.delete(alembicNode)
				logger.debug('Remove alembic nodes -> %s' % alembicNode)

		self.refreshUI()


	def doRemoveNonCacheAsset(self) : 
		listWidget = 'nonCache_tableWidget'
		assetNames = self.getTableData(listWidget, self.nonCacheListCol)

		nonCacheDataFile = self.setting['nonCacheDataPath']

		data = fileUtils.ymlLoader(nonCacheDataFile)

		for each in assetNames : 
			exportGrp = data[each]['exportGrp']
			hook.removeReference(exportGrp)


		self.refreshUI()


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

	def getTableData(self, listWidget, col) : 
		items = self.getColumnData(listWidget, col)
		
		if listWidget == 'asset_tableWidget' : 
			if not self.ui.all_checkBox.isChecked() : 
				items = self.getDataFromSelectedRange(listWidget, col)

		if listWidget == 'nonCache_tableWidget' : 
			if not self.ui.all2_checkBox.isChecked() : 
				items = self.getDataFromSelectedRange(listWidget, col)

		return items




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



	def getColumnData(self, widget, column) : 
		counts = eval('self.ui.%s.rowCount()' % widget)
		data = []

		for i in range(counts) : 
			item = eval('self.ui.%s.item(i, column)' % widget)
			if item : 
				data.append(str(item.text()))

		return data 


	def getDataFromSelectedRange(self, widget, columnNumber) : 
		lists = eval('self.ui.%s.selectedRanges()' % widget)

		if lists : 
			topRow = lists[0].topRow()
			bottomRow = lists[0].bottomRow()
			leftColumn = lists[0].leftColumn()
			rightColumn = lists[0].rightColumn()

			items = []

			for i in range(topRow, bottomRow + 1) : 
				item = str(eval('self.ui.%s.item(i, columnNumber).text()' % widget))
				items.append(item)


			return items


	def addListWidgetItem(self, listWidget, text, iconPath, color, addIcon = 1) : 
		if addIcon == 1 : 
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(iconPath),QtGui.QIcon.Normal,QtGui.QIcon.Off)
			cmd = 'QtGui.QListWidgetItem(self.ui.%s)' % listWidget
			item = eval(cmd)
			item.setIcon(icon)
			item.setText(text)
			item.setBackground(QtGui.QColor(color[0], color[1], color[2]))
			size = 16

			cmd2 = 'self.ui.%s.setIconSize(QtCore.QSize(%s, %s))' % (listWidget, size, size)
			eval(cmd2)
			QtGui.QApplication.processEvents()



	def messageBox(self, title, description) : 
		result = QtGui.QMessageBox.question(self,title,description ,QtGui.QMessageBox.Ok)

		return result