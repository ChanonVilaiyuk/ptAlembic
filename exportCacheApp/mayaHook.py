import sys, os 
import maya.cmds as mc
import maya.mel as mm

from tool.utils import fileUtils

version = mc.about(v=True)

if version == '2016':
	try:
		mc.loadPlugin("C:/Program Files/Autodesk/Maya2016/bin/plug-ins/AbcBullet.mll")
		mc.loadPlugin("C:/Program Files/Autodesk/Maya2016/bin/plug-ins/AbcExport.mll")
		mc.loadPlugin("C:/Program Files/Autodesk/Maya2016/bin/plug-ins/AbcImport.mll")
		mc.loadPlugin("C:/Program Files/Autodesk/Maya2016/bin/plug-ins/animImportExport.mll")
	except: 
		pass

def objectExists(obj) : 
	if obj : 
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



def refresh(mode) : 
	if mode == False : 
		mc.refresh(suspend = True)

	if mode == True : 
		mc.refresh(suspend = False)
		mc.refresh(f = True)