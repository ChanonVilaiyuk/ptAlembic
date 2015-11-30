# Alembic utilities
# Author TA
# ta.animator@gmail.com
# modify at your own risk

import maya.cmds as mc
import maya.mel as mm
import sys, os

from tool.utils import customLog 
logger = customLog.customLog()

def exportABC(obj, path) : 
	# if dir not exists, create one
	if not os.path.exists(os.path.dirname(path)) : 
		os.makedirs(os.path.dirname(path))

	start = mc.playbackOptions(q = True, min = True)
	end = mc.playbackOptions(q = True, max = True)
	options = []
	options.append('-frameRange %s %s' % (start, end))
	options.append('-attr project -attr assetID -attr assetType -attr assetSubType -attr assetName -attr assetShader ')
	options.append('-uvWrite')
	options.append('-writeFaceSets')
	options.append('-writeVisibility')
	options.append('-dataFormat ogawa')
	options.append('-root %s' % obj)
	options.append('-file %s' % path)
	optionCmd = (' ').join(options)

	cmd = 'AbcExport -j "%s";' % optionCmd
	result = mm.eval(cmd)

	return result

def importABC(obj, path, mode = 'new') : 
	if mode == 'new' : 
		cmd = 'AbcImport -mode import "%s";' % path

	if mode == 'add' : 
		cmd = 'AbcImport -mode import -connect "%s" -createIfNotFound -removeIfNoUpdate "%s";' % (obj, path)

	mm.eval(cmd)

	return path
