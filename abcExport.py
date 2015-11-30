import os, sys, yaml
import maya.cmds as mc
import maya.mel as mm

from tool.ptAlembic import abcUtils, fileUtils, setting
reload(abcUtils)
reload(fileUtils)
reload(setting)

# logger 
from tool.utils import customLog, sceneInfo
reload(customLog)
reload(sceneInfo)

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
			shadeFile = getShaderPath(assetName)['shadeFile']
			shadeDataFile = getShaderPath(assetName)['dataFile']
			assetPath = getShaderPath(assetName)['assetFile']

			if os.path.exists(cachePath) : 
				config = open(cachePath, 'r')
				configData = yaml.load(config)

			if not os.path.exists(os.path.dirname(cachePath)) : 
				os.makedirs(os.path.dirname(cachePath))

			print os.path.dirname(cachePath)

			fileInfo = open(cachePath, 'w')
				
			configData.update({str(assetName): {'shadeFile': shadeFile, 'shadeDataFile': shadeDataFile, 'cachePath': str(exportPath), 'assetPath': assetPath}})

			result = yaml.dump(configData, fileInfo, default_flow_style = False)


def getShaderPath(assetName) : 
	obj = '%s:%s' % (assetName, exportGrp)

	if mc.objExists(obj) : 
		refPath = mc.referenceQuery(obj, f = True)
		dirname = os.path.dirname(refPath)
		shadeFile = '%s/%s_Shade.ma' % (dirname, assetName)
		dataFile = '%s/%s_Shade.yml' % (dirname, assetName)
		assetFile = '%s/%s_Cache.ma' % (dirname, assetName)

		return {'shadeFile': shadeFile, 'dataFile': dataFile, 'assetFile': assetFile} 