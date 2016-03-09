import sys, os 
import maya.cmds as mc 
import maya.mel as mm
import yaml

def listShader(groupName = None) : 
	seNodes = mc.ls(type = 'shadingEngine')
	shaderInfo = dict()

	for eachNode in seNodes : 
		shaders = mc.listConnections('%s.surfaceShader' % eachNode, s = True)
		shapes = mc.listConnections('%s.dagSetMembers' % eachNode, s = True)

		if shaders and shapes : 
			if groupName : 
				objs = findObjGrp(groupName)

				if objs : 
					shapes = [a for a in shapes if a in objs]

			if shapes : 
				strShapes = [str(a) for a in shapes]
				strShaders = [str(a) for a in shaders]
				# shaderInfo[str(shaders[0])] = {'shapes': strShapes, 'shadingEngine': str(eachNode), 'shaders': strShaders}
				shaderInfo[str(shaders[0])] = {'objs': strShapes, 'shadingEngine': str(eachNode), 'shaders': strShaders}

	return shaderInfo 


def findObjGrp(groupName) : 
	curSel = mc.ls(sl = True)
	mc.select(groupName, hi = True)
	objs = mc.ls(sl = True)

	return objs 



def exportShadeNode(exportPath, groupName = None) : 
	shaderInfo = listShader(groupName)

	if shaderInfo : 
		shadeNodes = [shadeNode for shadeNode in shaderInfo]

		mc.select(shadeNodes)
		result = mc.file(exportPath, force = True, options = 'v=0', typ = 'mayaAscii', pr = True, es = True)

		return result 


def exportData(logPath, groupName = None) : 
	shaderInfo = listShader(groupName)
	fileInfo = open(logPath, 'w')

	result = yaml.dump(shaderInfo, fileInfo, default_flow_style = False)
	fileInfo.close()

	return logPath 


def doExport(exportPath, name, groupName = None) : 
	maFile = '%s/%s.ma' % (exportPath, name)
	dataFile = '%s/%s.yml' % (exportPath, name) 
	fileResult = exportShadeNode(maFile, groupName)
	dataResult = exportData(dataFile, groupName)

	print 'Export complete!'
	print fileResult
	print dataResult


def ptExport() : 
	sceneName = mc.file(q = True, location = True)
	dep = '/shade/'

	if dep in sceneName : 
		exportName = sceneName.split(dep)[0].split('/')[-1]
		exportPath = '%s/ref' % sceneName.split(dep)[0]
		name = '%s_Shade' % exportName
		groupName = 'Geo_Grp'
		maFile = '%s/%s.ma' % (exportPath, name)
		dataFile = '%s/%s.yml' % (exportPath, name)

		if not mc.objExists(groupName) : 
			groupName = 'Rig:Geo_Grp'

		fileResult = exportShadeNode(maFile, groupName)
		dataResult = exportData(dataFile, groupName)

		print '==========================='
		print fileResult
		print dataResult
		print 'Export complete' 


def doShadeExport() : 
	from tool.utils import entityInfo2 as entityInfo
	reload(entityInfo)

	asset = entityInfo.info()
	groupNames = ['Geo_Grp', 'Rig:Geo_Grp']
	name = '%s_Shade' % asset.name()
	exportPath = asset.getPath('ref')

	for groupName in groupNames : 
		if mc.objExists(groupName) : 
			doExport(exportPath, name, groupName = groupName)