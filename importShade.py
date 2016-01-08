import sys, os 
import maya.cmds as mc 
import maya.mel as mm
import yaml

from tool.utils import customLog 

logger = customLog.customLog()

def loadData(dataFile) : 
	fileInfo = open(dataFile, 'r')
	shadeInfo = yaml.load(fileInfo)
	fileInfo.close()

	return shadeInfo

def readData(dataFile, namespace) : 
	shadeInfo = loadData(dataFile)
	assignData = dict()

	for each in shadeInfo : 
		shd = each 
		objs = shadeInfo[each]['shapes']
		targetShd = '%s:%s' % (namespace, shd)

		for eachObj in objs : 
			targetObj = str()

			# if namespace 
			if ':' in eachObj : 
				rmNamespace = eachObj.split(':')[0]
				targetObj = eachObj.replace('%s:' % rmNamespace, '%s:' % namespace)

			# if not namespace 
			else : 
				if '|' in eachObj : 
					replaceStr = '|%s:' % namespace
					targetObj = eachObj.replace('|', replaceStr)

				else : 
					targetObj = '%s:%s' % (namespace, eachObj)

			if not targetShd in assignData : 
				assignData[targetShd] = [targetObj]

			else : 
				assignData[targetShd].append(targetObj)

	return assignData


def applyShade(namespace, maFile, dataFile) : 
	# import without namespace
	result = mc.file(maFile, i = True, type = 'mayaAscii', loadReferenceDepth = 'all')
	shdInfo = readData(dataFile, namespace)
	shdCount = 0
	shdMissing = 0
	objCount = 0 
	objMissing = 0

	for each in shdInfo : 
		shd = each
		targetObjs = shdInfo[each]

		if mc.objExists(shd) : 
			shdCount += 1

		else : 
			shdMissing += 1 

		for obj in targetObjs : 
			if mc.objExists(obj) : 
				objCount += 1

			else : 
				objMissing += 1 

	# summary 
	if shdMissing : 
		logger.info('---------------------------')
		for each in shdMissing : 
			logger.info(each )

		logger.info('Total %s shade missing' % len(shdMissing))

	if objMissing : 
		logger.info('---------------------------')
		for each in objMissing : 
			logger.info(each )

		logger.info('Total %s objs missing' % len(objMissing))

	# 

	if shdMissing == 0 and objMissing == 0 : 
		logger.info('Start applying shade ...')
		for each in shdInfo : 
			targetObjs = shdInfo[each]
			mc.select(targetObjs)
			mc.hyperShade(assign = each)

			logger.info('assigned %s -> %s' % (each, (',').join(targetObjs)))

		mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
		
		return True

	else : 
		return False