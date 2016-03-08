import os, sys, yaml
import maya.cmds as mc
import maya.mel as mm

from tool.ptAlembic import abcUtils, fileUtils, setting
reload(abcUtils)
reload(fileUtils)
reload(setting)

# logger 
from tool.utils import customLog, sceneInfo, pipelineTools
reload(customLog)
reload(sceneInfo)
reload(pipelineTools)

logger = customLog.customLog()
exportGrp = 'Geo_Grp'
exportDept = setting.exportDept

def doExport(assetNames, increment = True) : 
	exportPath = getShot(increment)

	for assetName in assetNames : 
		copyAttr(assetName)
		exportFilePath = '%s/%s.abc' % (exportPath, assetName)
		export(assetName, exportFilePath)
		exportData(assetName, exportFilePath)



def doExportUICall(assetName, cacheGrp, exportPath) : 

	logger.debug('Copying attribute ...') 
	copyAttr(assetName)
	logger.debug('Done')

	logger.debug('exporting alembic ...')
	exportFilePath = '%s/%s.abc' % (exportPath, assetName)
	abcUtils.exportABC('%s' % (cacheGrp), exportFilePath)
	logger.debug('export done')

	logger.debug('exporting data ...')
	exportData(assetName, exportFilePath)
	logger.debug('export data done')

	return exportFilePath


def copyAttr(assetName) : 
	srcGrp = '%s:Rig_Grp' % assetName
	dstGrp = '%s:%s' % (assetName, exportGrp)
	attrs = ['project', 'assetShader', 'assetID', 'assetType', 'assetSubType', 'assetName']

	for each in attrs : 
		attr = '%s.%s' % (srcGrp, each)
		value = mc.getAttr(attr)
		setStringAttr(dstGrp, each, value)

	return True 


def setStringAttr(obj, name, value) : 
	if not mc.objExists('%s.%s' % (obj, name)) : 
		mc.addAttr(obj, ln = name, dt = 'string')
		mc.setAttr('%s.%s' % (obj, name), e = True, keyable = True)

	mc.setAttr('%s.%s' % (obj, name), value, type = 'string')


def getShot(increment) : 
	# return cache path 
	# Result: P:/Lego_Friends2015/film/LEGO_FRIENDS_EPTEST/q0010/s0010/anim/scenes/work/frd_eptest_q0010_s0010_anim_v001.ma # 
	info = setting.getSceneInfo()

	if info : 
		cachePath = info['cachePath']
			
		return cachePath 


def export(assetName, exportPath) : 
	# exportPath = 'C:/Users/TA/Documents/maya/projects/default/cache/alembic/frd_andreaSchool_v001.abc'
	abcUtils.exportABC('%s:%s' % (assetName, exportGrp), exportPath)

	return True


def findVersion(cachePath, increment) : 
	return setting.findVersion(cachePath, increment)


def getSceneInfo() : 
	return setting.getSceneInfo()



def exportData(assetName, exportPath) : 
	info = setting.cachePathInfo()
	configData = dict()
	sceneInfo = setting.getSceneInfo()
	dept = sceneInfo['department']

	if info : 
		if exportDept == dept : 
			cachePath = info['cacheInfoPath']
			shadeFile = str(getShaderPath(assetName)['shadeFile'])
			shadeDataFile = str(getShaderPath(assetName)['dataFile'])
			assetPath = str(getShaderPath(assetName)['assetFile'])
			cacheGrp = str('%s:%s' % (assetName, exportGrp))
			assetDataPath = info['assetDataPath']

			if os.path.exists(cachePath) : 
				config = open(cachePath, 'r')
				configData = yaml.load(config)

			if not os.path.exists(os.path.dirname(cachePath)) : 
				os.makedirs(os.path.dirname(cachePath))

			print os.path.dirname(cachePath)

			fileInfo = open(cachePath, 'w')
				
			configData.update({str(assetName): {'shadeFile': shadeFile, 'shadeDataFile': shadeDataFile, 'cachePath': str(exportPath), 'assetPath': assetPath, 'cacheGrp': cacheGrp}})

			result = yaml.dump(configData, fileInfo, default_flow_style = False)

			# export asset hierarchy
			if not os.path.exists(assetDataPath) : 
				os.makedirs(assetDataPath)

			# export asset data
			dataPath = '%s/%s.yml' % (assetDataPath, assetName)
			pipelineTools.exportHierarchyData(cacheGrp, dataPath)
			print dataPath




def getShaderPath(assetName) : 
	obj = '%s:%s' % (assetName, exportGrp)

	if mc.objExists(obj) : 
		refPath = mc.referenceQuery(obj, f = True)
		dirname = os.path.dirname(refPath)
		assetDirName = dirname.split('/')[-2]
		# TA fix asset path 19/02/16
		shadeFile = '%s/%s_Shade.ma' % (dirname, assetDirName)
		dataFile = '%s/%s_Shade.yml' % (dirname, assetDirName)
		assetFile = '%s/%s_Cache.ma' % (dirname, assetDirName)

		return {'shadeFile': shadeFile, 'dataFile': dataFile, 'assetFile': assetFile} 