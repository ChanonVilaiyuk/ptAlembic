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
    disConnectedFacialRig()

    if shaderInfo : 
        shadeNodes = [shadeNode for shadeNode in shaderInfo if not mc.referenceQuery(shadeNode, isNodeReferenced = True)]

        mc.select(shadeNodes)
        result = mc.file(exportPath, force = True, options = 'v=0', typ = 'mayaAscii', pr = True, es = True)
        print shadeNodes

        return result 

def exportUvShadeNode(exportPath, groupName = None) : 
    shaderInfo = listShader(groupName)
    facialRenderConnect(connect=False)

    if shaderInfo : 
        shadeNodes = [shadeNode for shadeNode in shaderInfo if not mc.referenceQuery(shadeNode, isNodeReferenced = True)]

        mc.select(shadeNodes)
        result = mc.file(exportPath, force = True, options = 'v=0', typ = 'mayaAscii', pr = True, es = True)
        print shadeNodes
        facialRenderConnect(connect=True)

        return result 

def exportShadeNodeCmd(exportPath, groupName = None) : 
    shaderInfo = listShader(groupName)
    facialRenderConnect(connect=False)

    if shaderInfo : 
        shadeNodes = [shadeNode for shadeNode in shaderInfo if not mc.referenceQuery(shadeNode, isNodeReferenced = True)]

        mc.select(shadeNodes)
        result = mc.file(exportPath, force = True, options = 'v=0', typ = 'mayaAscii', pr = True, es = True)
        print shadeNodes
        facialRenderConnect(connect=True)

        return result 

def disConnectedFacialRig() : 
    loc = 'facialCtrl_loc'

    if mc.objExists(loc) : 
        nodes = mc.listConnections(loc, s = True, d = False, p = True)

        if nodes : 
            for each in nodes : 
                src = each 
                dsts = mc.listConnections(src, s = False, d = True, p = True)
                
                if dsts : 
                    for dst in dsts : 
                        if mc.isConnected(src, dst) : 
                            mc.disconnectAttr(src, dst)

        mc.parent(loc, w = True)

def facialRenderConnect(connect=False): 
    nodeKey = 'facialRender_lt'
    targetAttr = '.color'
    connectKey = 'tmpFacialConnect'

    if not connect: 
        if mc.objExists(nodeKey): 
            srcNode = '%s.outColor' % nodeKey
            dstNodes = mc.listConnections(srcNode, s = False, d = True, p = True)
            
            if dstNodes: 
                dstNodeAttr = dstNodes[0]
                dstNode = dstNodeAttr.split('.')[0]

                mc.disconnectAttr(srcNode, dstNodeAttr)
                mc.rename(dstNode, '%s_%s' % (dstNode, connectKey))

    else: 
        targetShd = mc.ls('*_%s' % connectKey)

        if targetShd and mc.objExists(nodeKey): 
            queryNode = mc.listConnections('%s.color' % targetShd[0], s=True, d=False, p=True)
            
            if not queryNode: 
                mc.connectAttr('%s.outColor' % nodeKey, '%s.color' % targetShd[0], f=True)
                mc.rename(targetShd[0], targetShd[0].replace('_%s' % connectKey, ''))


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
    return fileResult, dataResult


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
    from tool.utils import entityInfo
    reload(entityInfo)

    asset = entityInfo.info()
    groupNames = ['Geo_Grp', 'Rig:Geo_Grp']
    # name = '%s_Shade' % asset.name()
    name = asset.getRefNaming('shade', showExt = False)
    exportPath = asset.getPath('ref')

    for groupName in groupNames : 
        if mc.objExists(groupName) : 
            result = doExport(exportPath, name, groupName = groupName)

            return result

