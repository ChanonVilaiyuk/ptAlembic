import maya.cmds as mc
import maya.mel as mm


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


def getReferencePath(obj) : 
	return mc.referenceQuery(obj, f = True)