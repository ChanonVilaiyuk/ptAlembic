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

from tool.ptAlembic.exportCacheApp import exportUI as ui
reload(ui)

from tool.ptAlembic.exportCacheApp import customWidget
reload(customWidget)

from tool.ptAlembic.exportCacheApp import mayaHook as hook
reload(hook)

from tool.ptAlembic import abcExport, setting
reload(abcExport)
reload(setting)

abcExport.exportDept = 'anim'
moduleDir = sys.modules[__name__].__file__


from tool.utils import pipelineTools 
reload(pipelineTools)

from tool.utils import fileUtils
reload(fileUtils)

# logger 
from tool.utils import customLog
reload(customLog)

scriptName = 'ptAlembicExport'
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
		self.ui = ui.Ui_AlembicExportWin()
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

		# start functions 
		self.initSignal()
		self.initData()


	def initSignal(self) : 
		self.ui.increment_checkBox.stateChanged.connect(self.setCachePath)
		self.ui.nonCache_pushButton.clicked.connect(partial(self.assignAssetStatus, 'nonCache'))
		self.ui.cache_pushButton.clicked.connect(partial(self.assignAssetStatus, 'cache'))
		self.ui.add_pushButton.clicked.connect(self.addNonCache)
		self.ui.remove_pushButton.clicked.connect(self.removeNonCache)
		self.ui.refresh_pushButton.clicked.connect(self.refreshUI)
		self.ui.exportCache_pushButton.clicked.connect(self.doExportCache)
		self.ui.exportNonCache_pushButton.clicked.connect(self.doExportNonCache)

		# camera 
		self.ui.exportCam_pushButton.clicked.connect(self.doExportCamera)

		# setting 
		self.ui.viewOutput_pushButton.clicked.connect(partial(self.manageCacheData, 'view'))
		self.ui.clear2_pushButton.clicked.connect(partial(self.manageCacheData, 'clearAll'))

	def initData(self) : 
		# set logo UI
		self.setLogo()

		# set button state
		self.setButton()
		
		# call all data and set UI. All critical functions are here
		self.refreshUI()
		
		# set shot UI
		self.setShotInfo()
		
		# set cache path UI
		self.setCachePath()


	def refreshUI(self) : 
		logger.debug('=================')
		logger.debug('Refreshing UI ...')
		self.setAssetInfo()
		self.setAssetList()
		self.setNoncacheList()
		self.setCameraList()


	def setLogo(self) : 
		self.ui.logo_label.setPixmap(QtGui.QPixmap(self.logo).scaled(200, 60, QtCore.Qt.KeepAspectRatio))
		self.ui.logo2_label.setPixmap(QtGui.QPixmap(self.logo2).scaled(200, 60, QtCore.Qt.KeepAspectRatio))


	def setButton(self) : 
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(self.refreshIcon),QtGui.QIcon.Normal,QtGui.QIcon.Off)
		self.ui.refresh_pushButton.setIcon(icon)


	''' set shot header '''
	def setShotInfo(self) : 
		logger.debug('Setting shot info ...')
		shotInfo = pipelineTools.info()

		if shotInfo : 
			projectName = shotInfo['projectName']
			episodeName = shotInfo['episodeName']
			sequenceName = shotInfo['sequenceName']
			shotName = shotInfo['shotName']
			step = shotInfo['step']

			self.ui.project_label.setText(projectName)
			self.ui.episode_label.setText(episodeName)
			self.ui.sequence_label.setText(sequenceName)
			self.ui.shot_label.setText(shotName)

			logger.debug('Set shot complete')
	

	''' collect all assets in the scene ''' 
	def setAssetInfo(self) : 
		logger.debug('Collecting asset ...')

		# get all reference assets 
		assets = pipelineTools.getAllAssets()

		# get data path 
		increment = self.ui.increment_checkBox.isChecked()

		# increment True = version up, increment Fase = latest version
		cachePathInfo = self.getCachePathInfo(increment)

		if cachePathInfo : 
			# this data store user custom cache and noncache list, then override default list.
			dataPath = cachePathInfo['dataPath']
			data = self.loadData(dataPath)

			if assets : 
				for each in assets : 
					namespace = each.split(':')[0]
					exportGrp = '%s:%s' % (namespace, self.cacheGrp)

					# get asset's attribute
					attrInfo = pipelineTools.getAssetAttr(each)
					status = ''

					logger.debug(each)

					if attrInfo : 
						assetType = attrInfo['assetType']

						if data : 
							if each in data.keys() : 
								status = data[each]['status']

						# if type in type list, put in cahce list 
						if assetType in self.cacheAssetTypeList : 
							if not status : 
								status = 'cache'

						# else, put in nonCache list 
						else : 
							if not status : 
								status = 'nonCache'

					
					# check if asset really exists
					if hook.objectExists(exportGrp) : 
						if not each in self.assetInfo.keys() : 
							self.assetInfo[each] = {'namespace': namespace, 'cacheGrp': exportGrp, 'rigGrp': each, 'attr': attrInfo, 'status': status, 'type': self.normalAsset}

						else : 
							self.assetInfo.update({each: {'namespace': namespace, 'cacheGrp': exportGrp, 'rigGrp': each, 'attr': attrInfo, 'status': status, 'type': self.normalAsset}})

					else : 
						logger.warning('%s not found!!' % exportGrp)



	def setAssetList(self) : 
		logger.debug('Setting asset list ...')
		self.ui.cache_listWidget.clear() 
		self.ui.nonCache_listWidget.clear()

		if self.assetInfo : 
			for each in self.assetInfo : 
				rigGrp = each 
				namespace = self.assetInfo[each]['namespace']
				cacheGrp = self.assetInfo[each]['cacheGrp']
				status = self.assetInfo[each]['status']
				assetType = self.assetInfo[each]['type']

				displayItem = '%s - %s' % (namespace, rigGrp)
				bgColor = [0, 0, 0]

				if status == 'cache' : 
					self.addCacheListWidget(namespace, rigGrp, '', bgColor, self.rdyIcon, self.iconSize)

				elif status == 'nonCache' : 
					self.addNonCacheListWidget(namespace, rigGrp, '', bgColor, self.rdyIcon, self.iconSize)

				else : 
					logger.warning('%s not assigned to either cache or nonCache list' % rigGrp)

			logger.debug('Set asset list complete')



	def setCachePath(self) : 

		increment = self.ui.increment_checkBox.isChecked()
		path = self.getCachePathInfo(increment)

		if path : 
			cachePath = path['cachePath']
			version = cachePath.split('/')[-1]
			self.ui.version_comboBox.clear()
			self.ui.version_comboBox.addItem(version)
			self.ui.cache_lineEdit.setText(cachePath)



	def getCachePathInfo(self, increment = True) : 
		return setting.cachePathInfo(increment)



	# =========================================================================================
	# button command

	def assignAssetStatus(self, mode) : 

		logger.debug('=====================')		
		logger.debug('assignAssetStatus ...')		

		rigGrps = []
		addGrps = []
		notAddGrps = []

		# send to cache 
		if mode == 'cache' : 
			logger.debug('cache mode')
			listWidget = 'nonCache_listWidget'
			items = self.getSelectedItems(listWidget)

			logger.debug(items)

			if items : 
				rigGrps = items[1]

		# send to non cache 
		if mode == 'nonCache' : 
			logger.debug('nonCache mode')
			listWidget = 'cache_listWidget'
			items = self.getSelectedItems(listWidget)

			logger.debug(items)

			if items : 
				rigGrps = items[1]

		if rigGrps : 
			self.writeStatus()
			dataPath = self.getCachePathInfo(True)['dataPath']

			if dataPath : 
				data = fileUtils.ymlLoader(dataPath)

				if data : 
					for each in rigGrps : 
						if each in data.keys() : 
							if not each == self.nonCacheAsset : 
								data[each]['status'] = mode
								addGrps.append(each)

							else : 
								notAddGrps.append(each)


					logger.debug('writing data back')
					fileUtils.ymlDumper(dataPath,data)
					
					# refresh UI
					self.refreshUI()

					if addGrps : 
						display = (', ').join(addGrps)
						logger.info('%s added to %s' % (display, mode))

					if notAddGrps : 
						display = (', ').join(notAddGrps)
						logger.info('%s cannot be added to %s' % (display, mode))


		else : 
			logger.warning('no items selected')

		


	def writeStatus(self) : 
		logger.debug('start record status ...')

		dataPath = self.getCachePathInfo(True)['dataPath']
		statusInfo = dict()

		if not os.path.exists(os.path.dirname(dataPath)) : 
			os.makedirs(os.path.dirname(dataPath))

		if os.path.exists(dataPath) : 
			statusInfo = fileUtils.ymlLoader(dataPath)
		
		cacheListWidget = 'cache_listWidget'
		cacheTexts = self.getAllItems(cacheListWidget)
		cacheText1 = cacheTexts[0]
		cacheText2 = cacheTexts[1]

		if cacheText1 and cacheText2 : 
			for i in range(len(cacheText1)) : 
				namespace = cacheText1[i]
				rigGrp = cacheText2[i]

				statusInfo.update({rigGrp: {'namespace': namespace, 'status': 'cache', 'rigGrp': rigGrp}})


		nonCacheListWidget = 'nonCache_listWidget'
		nonCacheTexts = self.getAllItems(nonCacheListWidget)
		nonCacheText1 = nonCacheTexts[0]
		nonCacheText2 = nonCacheTexts[1]

		if nonCacheText1 and nonCacheText2 : 
			for i in range(len(nonCacheText1)) : 
				namespace = nonCacheText1[i]
				rigGrp = nonCacheText2[i]

				statusInfo.update({rigGrp: {'namespace': namespace, 'status': 'nonCache', 'rigGrp': rigGrp}})

		result = fileUtils.ymlDumper(dataPath, statusInfo)

		logger.debug('write status info %s' % dataPath)


	def loadData(self, dataPath) : 
		data = None 

		if os.path.exists(dataPath) : 
			data = fileUtils.ymlLoader(dataPath)

		return data 



	def setNoncacheList(self) : 
		if self.getCachePathInfo(True) : 
			nonCacheFile = self.getCachePathInfo(True)['nonCacheDataPath']
			bgColor = [0, 20, 60]
			text3 = ''

			if os.path.exists(nonCacheFile) : 
				data = fileUtils.ymlLoader(nonCacheFile)

				if 'nonCache' in data.keys() : 
					for each in data['nonCache'] : 
						if not hook.objectExists(each) : 
							bgColor = [100, 20, 20]
							text3 = 'not exists'

						self.addNonCacheListWidget(each, self.nonCacheAsset, text3, bgColor, self.rdyIcon, self.iconSize)


	def setCameraList(self) : 
		path = self.getCachePathInfo()
		cameraPath = path['cameraPath']




	def addNonCache(self) : 
		# add to file 
		nonCacheFile = self.getCachePathInfo(True)['nonCacheDataPath']
		selItems = hook.getSelectedObjs()

		if selItems : 
			self.writeStatus()
			if os.path.exists(nonCacheFile) : 
				data = fileUtils.ymlLoader(nonCacheFile)
				
				for each in selItems : 
					if 'nonCache' in data.keys() : 
						if not each in data['nonCache'] : 
							data['nonCache'].append(each)

			else : 
				data = {'nonCache': selItems}

			fileUtils.ymlDumper(nonCacheFile, data)

		self.refreshUI()



	def removeNonCache(self) : 
		nonCacheFile = self.getCachePathInfo(True)['nonCacheDataPath']

		listWidget = 'nonCache_listWidget'
		items = self.getSelectedItems(listWidget)

		# remove from file 

		if items : 
			if os.path.exists(nonCacheFile) : 
				data = fileUtils.ymlLoader(nonCacheFile)
				
				for each in items : 
					grp = each[0]

					if 'nonCache' in data.keys() : 
						if grp in data['nonCache'] : 
							data['nonCache'].remove(grp)

			else : 
				data = {'nonCache': selItems}

			fileUtils.ymlDumper(nonCacheFile, data)

		self.refreshUI()


	# cache area ==============================================================================

	def doExportCache(self) : 
		logger.debug('def doExportCache')
		logger.info('--------------------------')
		logger.info('Start exporting ...')
		startTime = datetime.now()

		# get list 
		allStatus = self.ui.exportCacheAll_checkBox.isChecked()

		# cachePath 
		cachePath = str(self.ui.cache_lineEdit.text())
		
		listWidget = 'cache_listWidget'
		assetList = []
		itemWidgets = []

		# optimized viewport 
		hook.isolateObj(True)

		if allStatus : 
			items = self.getAllItems(listWidget)
			assetList = items[1]
			itemWidgets = items[2]

		else : 
			items = self.getSelectedItems(listWidget)
			assetList = items[1]
			itemWidgets = items[2]

		if assetList : 
			i = 0 

			for eachAsset in assetList : 
				if eachAsset in self.assetInfo : 

					# get export group
					cacheGrp = self.assetInfo[eachAsset]['cacheGrp']
					namespace = self.assetInfo[eachAsset]['namespace']

					# set status 
					itemWidgets[i].setIcon(self.ipIcon, self.iconSize)
					QtGui.QApplication.processEvents()

					# do cache 
					result = abcExport.doExportUICall(namespace, cacheGrp, cachePath)

					if result : 
						logger.info('Export %s to %s complete' % (cacheGrp, result))

						# set status 
						itemWidgets[i].setIcon(self.okIcon, self.iconSize)
						QtGui.QApplication.processEvents()

				i += 1 

		hook.isolateObj(False)
		finishTime = datetime.now()
		duration = finishTime - startTime

		logger.info('Finish export')
		logger.info('%s' % duration)


	# export non cache ==========================================================================
	def doExportNonCache(self) : 
		nonCachePath = self.getCachePathInfo(True)['nonCachePath']

		listWidget = 'nonCache_listWidget'
		if self.ui.exportAll_checkBox.isChecked() : 
			items = self.getAllItems(listWidget)

		else : 
			items = self.getSelectedItems(listWidget)

		if not os.path.exists(nonCachePath) : 
			os.makedirs(nonCachePath)


		if items : 
			for i in range(len(items[0])) : 
				text1 = items[0][i]
				text2 = items[1][i]
				itemWidget = items[2][i]

				exportGrp = text2 
				fileName = text1 

				# if text2 is self.nonCacheAsset, use text1 as an exportGrp 
				if text2 == self.nonCacheAsset : 
					exportGrp = text1 
					fileName = text1.replace(':', '')

				exportFile = '%s/%s.ma' % (nonCachePath, fileName)
				result = hook.export(exportGrp, exportFile)
				itemWidget.setIcon(self.okIcon, self.iconSize)

				logger.debug(result)
				QtGui.QApplication.processEvents()


	# export camera 
	def doExportCamera(self) : 
		pass 



	# setting area 
	# =========================================================================================
	def manageCacheData(self, action) : 
		logger.debug('def manageCacheData')
		increment = self.ui.increment_checkBox.isChecked()
		path = self.getCachePathInfo(increment)
		
		if action == 'view' : 
			logger.debug(' - action %s' % action)
			cachePath = path['cacheDir']
			logger.debug(cachePath)

			if os.path.exists(cachePath) : 
				subprocess.Popen(r'explorer /e,"%s"' % cachePath.replace('/', '\\'))

			else : 
				self.messageBox('Path not exists', '%s not exists' % cachePath)


		if action == 'clearAll' : 
			logger.debug(' - action %s'% action)
			cachePath = path['cacheDir']

			if os.path.exists(cachePath) : 
				dirs = fileUtils.listFolder(cachePath)
				logger.debug(' - %s' % dirs)

				if dirs : 
					for eachDir in dirs : 
						removeDir = '%s/%s' % (cachePath, eachDir)
						shutil.rmtree(removeDir)
						logger.info('Remove %s' % removeDir)

					self.messageBox('Success', 'All caches data removed')

				else : 
					self.messageBox('Warning', 'No cache data to remove')


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


	def addCacheListWidget(self, text1, text2, text3, bgColor, iconPath, size) : 
		myCustomWidget = customWidget.customQWidgetItem()
		myCustomWidget.setText1(text1)
		myCustomWidget.setText2(text2)
		myCustomWidget.setText3(text3)

		myCustomWidget.setTextColor1([200, 200, 200])
		myCustomWidget.setTextColor2([120, 120, 120])
		myCustomWidget.setTextColor3([120, 120, 120])

		myCustomWidget.setIcon(iconPath, size)

		item = QtGui.QListWidgetItem(self.ui.cache_listWidget)
		item.setSizeHint(myCustomWidget.sizeHint())
		item.setBackground(QtGui.QColor(bgColor[0], bgColor[1], bgColor[2]))

		self.ui.cache_listWidget.addItem(item)
		self.ui.cache_listWidget.setItemWidget(item, myCustomWidget)

		# item.setBackground(QtGui.QColor(color[0], color[1], color[2]))


	def addNonCacheListWidget(self, text1, text2, text3, bgColor, iconPath, size) : 
		myCustomWidget = customWidget.customQWidgetItem()
		myCustomWidget.setText1(text1)
		myCustomWidget.setText2(text2)
		myCustomWidget.setText3(text3)

		myCustomWidget.setTextColor1([200, 200, 200])
		myCustomWidget.setTextColor2([120, 120, 120])
		myCustomWidget.setTextColor3([120, 120, 120])

		myCustomWidget.setIcon(iconPath, size)

		item = QtGui.QListWidgetItem(self.ui.nonCache_listWidget)
		item.setSizeHint(myCustomWidget.sizeHint())
		item.setBackground(QtGui.QColor(bgColor[0], bgColor[1], bgColor[2]))

		self.ui.nonCache_listWidget.addItem(item)
		self.ui.nonCache_listWidget.setItemWidget(item, myCustomWidget)



	def messageBox(self, title, description) : 
		result = QtGui.QMessageBox.question(self,title,description ,QtGui.QMessageBox.Ok)

		return result