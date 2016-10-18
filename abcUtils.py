# Alembic utilities
# Author TA
# ta.animator@gmail.com
# modify at your own risk

import maya.cmds as mc
import maya.mel as mm
import sys, os

from tool.utils import customLog 
logger = customLog.customLog()

mayaVersion = mc.about(version=True)

if '2015' in mayaVersion : 
    load = mc.pluginInfo('AbcExport', query=True, loaded=True, n=True)
    if not load : 
        mc.loadPlugin('C:\\Program Files\\Autodesk\\Maya2015\\bin\\plug-ins\\AbcExport.mll', qt = True)
        print 'loadPlugin \"AbcExport.mll\"'

    load = mc.pluginInfo('AbcImport', query=True, loaded=True, n=True)
    if not load : 
        mc.loadPlugin("C:\\Program Files\\Autodesk\\Maya2015\\bin\\plug-ins\\AbcImport.mll", qt = True)
        print 'LoadPlugin : \"AbcImport.mll\"'

if '2016' in mayaVersion : 
    load = mc.pluginInfo('AbcExport', query=True, loaded=True, n=True)
    if not load : 
        mc.loadPlugin('C:\\Program Files\\Autodesk\\Maya2016\\bin\\plug-ins\\AbcExport.mll', qt = True)
        print 'loadPlugin \"AbcExport.mll\"'

    load = mc.pluginInfo('AbcImport', query=True, loaded=True, n=True)
    if not load : 
        mc.loadPlugin("C:\\Program Files\\Autodesk\\Maya2016\\bin\\plug-ins\\AbcImport.mll", qt = True)
        print 'LoadPlugin : \"AbcImport.mll\"'

# mc.loadPlugin("C:/Program Files/Autodesk/Maya2015/bin/plug-ins/AbcExport.mll", qt = True)
# mc.loadPlugin("C:/Program Files/Autodesk/Maya2015/bin/plug-ins/AbcImport.mll", qt = True)

def exportABC(obj, path) : 
	# if dir not exists, create one
	if not os.path.exists(os.path.dirname(path)) : 
		os.makedirs(os.path.dirname(path))

	start = mc.playbackOptions(q = True, min = True)
	end = mc.playbackOptions(q = True, max = True)
	options = []
	options.append('-frameRange %s %s' % (start, end))
	options.append('-attr project -attr assetID -attr assetType -attr assetSubType -attr assetName -attr assetShader ')
	options.append('-attr id -attr model -attr uv -attr rig -attr surface -attr data -attr ref -attr lod ')
	# this will send bad uv to look dev. do not enable this.
	options.append('-uvWrite')
	options.append('-writeFaceSets')
	options.append('-writeVisibility')
	options.append('-worldSpace')
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
		# cmd = 'AbcImport -mode import -connect "%s" -createIfNotFound -removeIfNoUpdate "%s";' % (obj, path)
		# not work in some cases, so use below
		cmd = 'AbcImport -mode import -connect "%s" "%s";' % (obj, path)

	if mode == 'add_remove' : 
		cmd = 'AbcImport -mode import -connect "%s" -createIfNotFound -removeIfNoUpdate "%s";' % (obj, path)

	mm.eval(cmd)

	return path
