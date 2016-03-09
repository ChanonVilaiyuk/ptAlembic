import sys, os 
import maya.cmds as mc
import maya.mel as mm

from tool.utils import fileUtils
from tool.utils import mayaTools
from tool.utils import pipelineTools


def objectExists(obj) : 
	return mc.objExists(obj)


def getSelectedObjs() : 
	return mc.ls(sl = True)


def export(obj, exportFile) : 
	mc.select(obj)
	result = mc.file(exportFile, force = True, options = "v=0;", typ = "mayaAscii", pr = True, es = True)
	return result 


def isolateObj(state) : 
	currentPane = mc.paneLayout('viewPanes', q=True, pane1=True)
	mc.isolateSelect( currentPane, state=state )


def getShotRange() : 
	min = mc.playbackOptions(q = True, min = True)
	max = mc.playbackOptions(q = True, max = True)

	return [min, max]


def setShotRange(min, max) : 
	mc.playbackOptions(min = min)
	mc.playbackOptions(max = max)
	mc.playbackOptions(ast = min)
	mc.playbackOptions(aet = max)


def getReferencePath(obj) : 
	return mc.referenceQuery(obj, f = True)


def exportAnim(namespace, exportFile) : 
	# ctrls
	set1 = mc.ls('%s:*_ctrl' % namespace)
	set2 = mc.ls('%s:*:*_ctrl' % namespace)
	set3 = mc.ls('%s:*:*:*_ctrl' % namespace)
	set4 = mc.ls('%s:*_Ctrl' % namespace)
	set5 = mc.ls('%s:*:*_Ctrl' % namespace)
	set6 = mc.ls('%s:*:*:*_Ctrl' % namespace)

	ctrls = set1+set2+set3+set4+set5+set6

	animFile = '%s/%s.anim' % (exportFile, namespace)

	# manage dirs 
	if not os.path.exists(exportFile) : 
		os.makedirs(exportFile)

	# export command 
	mc.select(ctrls)

	tempFile = '%s/temp.anim' % mc.internalVar(utd = True)
	mm.eval('file -force -options "precision=8;intValue=17;nodeNames=1;verboseUnits=0;whichRange=1;range=1:24;options=keys;hierarchy=none;controlPoints=0;shapes=0;helpPictures=0;useChannelBox=0;copyKeyCmd=-animation objects -option keys -hierarchy none -controlPoints 0 -shape 0 " -typ "animExport" -pr -es "%s";' % tempFile)

	fileUtils.copy(tempFile, animFile)
	os.remove(tempFile)

	# export selection controllers 
	exportFilePath = '%s/%s.txt' % (exportFile, namespace)
	fileUtils.writeFile(exportFilePath, str(ctrls))

	mc.select(cl = True)

	return True 

def createReference(namespace, path) : 
	result = mc.file(path, reference = True, ignoreVersion = True, gl = True, loadReferenceDepth = 'all', namespace = namespace, options = 'v=0')

''' need to change the way to find alembic nodes. This function only works for deform geo only '''
# def getAlembicNode(cacheGrp) : 
# 	meshes = mayaTools.findMeshInGrp(cacheGrp)
# 	alembicNodes = []

# 	if meshes : 

# 		for each in meshes : 
# 			nodes = mc.listConnections('%s.inMesh' % each, s = True, type = 'AlembicNode')

# 			if nodes : 
# 				for node in nodes : 
# 					if not node in alembicNodes : 
# 						alembicNodes.append(node)

# 		return alembicNodes
''' re written get alembicNode functions '''

def getAlembicNode(cacheGrp) : 
	mc.select(cacheGrp, hi = True)
	allObjs = mc.ls(sl = True)
	allAlembicNodes = getAllAlembicNodes()

	alembicNodes = []

	if allObjs : 
		for each in allObjs : 
			if allAlembicNodes : 
				for eachNode in allAlembicNodes : 
					connectObjs = allAlembicNodes[eachNode]

					if each in connectObjs : 
						if not eachNode in alembicNodes : 
							alembicNodes.append(eachNode)

		return alembicNodes


def getAllAlembicNodes() : 
	nodes = mc.ls(type = 'AlembicNode')
	alembicNodes = dict()

	for each in nodes : 
		result = mc.listConnections(each, s = False, d = True, c = True)
		alembicNodes.update({each: result})

	mc.select(cl = True)

	return alembicNodes


def getAlembicPath(node) : 
	return mc.getAttr('%s.abc_File' % node)


def importFile(file) : 
	return mc.file(file,  i = True, type = 'mayaAscii', options = 'v=0', pr = True, loadReferenceDepth = 'all')


def removeReference(obj) : 
	if isReference(obj) : 
		mayaTools.removeReference(obj)

	else : 
		delete(obj)


def removeReferenceByPath(path) : 
	mc.file(path, rr = True)

def removeNamespace(namespace) : 
	mayaTools.removeNamespace(namespace)

def delete(objs) : 
	return mc.delete(objs)


def isReference(obj) : 
	return mc.referenceQuery(obj, isNodeReferenced = True)


def getParent(obj) : 
	parent = mc.listRelatives(obj, p = True)
	return parent

def getAllReference() : 
	return mc.file(q = True, r = True)

def getNamespace(path) : 
	return mc.file(path, q = True, namespace = True)


def deleteUnUsedNodes() : 
	mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')