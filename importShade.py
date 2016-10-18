import sys, os 
import maya.cmds as mc 
import maya.mel as mm
import yaml
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from tool.utils import customLog 

# logger = customLog.customLog()

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
		# for each in shdMissing : 
		# 	logger.info(each)

		logger.info('Total %s shade missing' % len(shdMissing))

	if objMissing : 
		logger.info('---------------------------')
		# for each in objMissing : 
		# 	logger.info(each )

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

def applyRefShade(namespace, maFile, dataFile) : 
	# import without namespace
	# defind namespace for reference shader
	namespaceShd = '%s_shade' % namespace
	logger.debug('start applyRefShade -> args')
	logger.debug('namespace %s' % namespace)
	logger.debug('shadeFile %s' % maFile)
	logger.debug('dataFile %s' % dataFile)
	

	if os.path.exists(maFile) and os.path.exists(dataFile) : 
		# find existing references
		existingRef = mc.file(q = True, r = True)
		logger.debug('existing ref "%s"' % existingRef)

		# create reference if not created yet
		if not maFile in existingRef : 
			mc.file(maFile, r = True, ignoreVersion = True, gl = True, loadReferenceDepth = "all", namespace = namespaceShd, options = "v=0")
			logger.debug('Shade not found, create reference "%s"' % maFile)
			logger.debug('Shade namespace "%s"' % namespaceShd)

		else : 
			logger.debug('Shade exists')
			namespaceShd = mc.file(maFile, q = True, namespace = True)

		# load shade data
		data = loadData(dataFile)
		materialInfo = dict()
		allLostMtrs = []
		allLostObjs = []
		failedOperations = []
		logger.debug('Loaded shade data %s' % data)

		# loop for material 
		for mtr in data : 
			objs = data[mtr]['objs']

			# material with new namespace 
			material = '%s:%s' % (namespaceShd, mtr)

			# replacing namespace for assigned objs
			assignedObj = ['%s:%s' % (namespace, a.split(':')[-1]) for a in objs]
			validObjs = []
			lostObjs = []

			print material
			

			if mc.objExists(material) : 
				logger.debug('%s --- ' % material)

				# check if objs exists 
				for eachObj in assignedObj : 
					if mc.objExists(eachObj) : 
						validObjs.append(eachObj)

					else : 
						lostObjs.append(eachObj)
						allLostObjs.append(eachObj)

				if lostObjs : 
					logger.debug('lost objs : %s' % lostObjs)

				# run assign 
				try : 
					mc.select(validObjs)
					mc.hyperShade(assign = material)
					logger.debug('Successfully assigned %s\n' % material)
					logger.debug('------------------------------')

				except Exception as e : 
					failedOperations.append(str(e))
					logger.debug(e)

			else : 
				allLostMtrs.append(material)

			# collect information 
			materialInfo.update({material: {'status': mc.objExists(material), 'validObjs': validObjs, 'lostObjs': lostObjs}})

		if allLostMtrs : 
			logger.debug('%s Lost material :\n%s' % (len(allLostMtrs), allLostMtrs))

		if allLostObjs : 
			logger.debug('%s Lost objects : \n%s' % (len(allLostObjs), allLostObjs))

		if failedOperations : 
			logger.debug('%s failed to assign : %s' % (len(failedOperations), failedOperations))

		if not allLostMtrs and not allLostObjs and not failedOperations : 
			logger.info('Successfully assigned')


