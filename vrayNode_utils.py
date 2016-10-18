import sys, os 
import maya.cmds as mc 
import maya.mel as mm 
from tool.utils import *
from tool.utils import entityInfo, pipelineTools
reload(entityInfo)
reload(pipelineTools)

def doExportVrayNodes() : 
        title = 'Export Vray Nodes'
        asset = entityInfo.info()

        returnResult = dict()
        exportPath = asset.getPath('refData')
        nodeFile = '%s/%s' % (exportPath, asset.getRefNaming('vrayNode'))
        dataFile = '%s/%s' % (exportPath, asset.getRefNaming('vrayNodeData'))

        startMTime1 = None
        startMTime2 = None
        currentMTime1 = None
        currentMTime2 = None

        if os.path.exists(nodeFile) : 
            startMTime1 = os.path.getmtime(nodeFile)

        if os.path.exists(dataFile) : 
            startMTime2 = os.path.getmtime(dataFile)

        result = pipelineTools.exportVrayNode(dataFile, nodeFile)

        dataFileResult = result[0]
        nodeFileResult = result[1]

        if dataFileResult : 
            currentMTime1 = os.path.getmtime(dataFileResult)

        if nodeFileResult : 
            currentMTime2 = os.path.getmtime(nodeFileResult)

        status = False
        status1 = False 
        status2 = False
        message = ''

        if not currentMTime1 == startMTime1 : 
            status1 = True 
            message += 'Node file export complete - '

        if not currentMTime2 == startMTime2 : 
            status2 = True
            message += 'Node data file export complete'

        if status1 and status2 : 
            status = True

        if status : 

            print('---- Vray Nodes Output ---')
            print(dataFileResult)
            print(nodeFileResult)


def exportVrayNode(dataFile, nodeFile) : 
    asset = entityInfo.info()

    data = dict() 
    vrayDispData = dict()
    vrayPropData = dict()

    vrayDisps = mc.ls(type = 'VRayDisplacement')
    vrayProps = mc.ls(type = 'VRayObjectProperties')

    for each in vrayDisps : 
        vdNode = str(each)
        members = mc.sets(each, q = True)
        members = [str(a) for a in members]

        vrayDispData.update({vdNode: members})

    for each in vrayProps : 
        vpNode = str(each)
        members = mc.sets(each, q = True)
        members = [str(a) for a in members]

        vrayPropData.update({vpNode: members})

    data = {'assetName': asset.name(), 'vrayDisp': vrayDispData, 'vrayProp': vrayPropData, 'nodeFile': str(nodeFile), 'assetPath': str(asset.getPath('ref'))}

    dirDataFile = os.path.dirname(dataFile)

    if not os.path.exists(dirDataFile) : 
        os.makedirs(dirDataFile)

    result1 = fileUtils.ymlDumper(dataFile, data)

    # ============================
    # export nodes 
    exp = 'exp'
    expNodes = vrayDisps + vrayProps
    expList = []
    oriData = dict()
    result2 = None

    for each in expNodes : 
        node = each
        tmpName = '%s_%s' % (node, exp)
        originalNode = mc.rename(node, tmpName)
        exportNode = mc.duplicate(tmpName, n = node)
        
        if exportNode : 
            expList.append(exportNode[0])

        if originalNode : 
            oriData.update({originalNode: node})

    if expList : 
        mc.select(expList, ne = True)
        result2 = mc.file(nodeFile, force = True, options = "v=0;", typ = "mayaAscii", pr = True, es = True)


        # clean lock node
        cleanFile(result2)


    # delete 
    if expList : 
        mc.delete(expList)

    # rename back 
    for each in oriData : 
        mc.rename(each, oriData[each])

    return dataFile, result2


def importVrayNodes(dataFile, fromFile = True) : 
    data = fileUtils.ymlLoader(dataFile)
    nodeFile = data['nodeFile']
    assetPath = data['assetPath']
    assetName = data['assetName']

    vrayDisps = data['vrayDisp']
    vrayProps = data['vrayProp']

    vrayDispNodes = vrayDisps.keys()
    vrayPropNodes = vrayProps.keys()


    # find asset with assetName 
    assetInfo = getAssetInfo(assetName)

    if assetInfo : 
        for asset in assetInfo : 
            namespaces = assetInfo[asset]

            if asset == assetName : 
                if fromFile : 
                    snapNodes = mc.ls(type = ['VRayDisplacement', 'VRayObjectProperties'])

                    if os.path.exists(nodeFile) : 
                        mc.file(nodeFile,  i = True, type = 'mayaAscii', options = 'v=0', pr = True, loadReferenceDepth = 'all')

                    else : 
                        print 'File not exists %s' % nodeFile
                        return 

                    currentNodes = mc.ls(type = ['VRayDisplacement', 'VRayObjectProperties'])
                    newNodes = [a for a in currentNodes if not a in snapNodes]

                for namespace in namespaces : 
                    
                    if mc.namespace(exists = namespace) : 
                        # mc.namespace(set = namespace)

                        
                        # vrayDisp 
                        if vrayDispNodes : 
                            for each in vrayDispNodes : 
                                members = vrayDisps[each]
                                nsNode = each

                                if not fromFile : 
                                    if not mc.objExists(nsNode) : 
                                        print 'Create node %s' % nsNode
                                        nsNode = mc.createNode('VRayDisplacement', n = each)
                                        mm.eval('vray addAttributesFromGroup %s vray_subdivision 1;' % nsNode)

                                nsMembers = ['%s:%s' % (namespace, a.split(':')[-1]) for a in members if mc.objExists('%s:%s' % (namespace, a.split(':')[-1]))]
                                missingMembers = ['%s:%s' % (namespace, a.split(':')[-1]) for a in members if not mc.objExists('%s:%s' % (namespace, a.split(':')[-1]))]

                                if mc.objExists(nsNode) : 
                                    mc.sets(nsMembers, add = nsNode)
                                    print '%s -> %s' % (nsNode, nsMembers)

                                if missingMembers : 
                                    print '%s has missing members %s' % (nsNode, missingMembers)


                        # vrayProp
                        if vrayPropNodes : 
                            for each in vrayPropNodes : 
                                members = vrayProps[each]
                                nsNode = each

                                if not fromFile : 
                                    if not mc.objExists(nsNode) : 
                                        print 'Create node %s' % nsNode
                                        nsNode = mc.createNode('VRayObjectProperties', n = each)
                                        mm.eval('vray addAttributesFromGroup %s vray_subdivision 1;' % nsNode)

                                nsMembers = ['%s:%s' % (namespace, a.split(':')[-1]) for a in members if mc.objExists('%s:%s' % (namespace, a.split(':')[-1]))]
                                missingMembers = ['%s:%s' % (namespace, a.split(':')[-1]) for a in members if not mc.objExists('%s:%s' % (namespace, a.split(':')[-1]))]

                                if mc.objExists(nsNode) : 
                                    mc.sets(nsMembers, add = nsNode)
                                    print '%s -> %s' % (nsNode, nsMembers)

                                if missingMembers : 
                                    print '%s has missing members %s' % (nsNode, missingMembers)

                        # mc.namespace(set = ':')

                validNodes = [a for a in (vrayDispNodes + vrayPropNodes)]

                for eachNode in newNodes : 
                    if not eachNode in validNodes : 
                        mc.delete(eachNode)
                        print 'Remove %s' % eachNode



def doImportVrayNodes2() : 
    # get from geo_grp in the scene 
    grps = mc.ls('*:Geo_Grp')

    dataFiles = []

    for eachAsset in grps : 
        # get path 
        attr = '%s.ref' % eachAsset
        lodAttr = '%s.lod' % eachAsset

        if mc.objExists(attr) and mc.objExists(lodAttr) : 
            ref = mc.getAttr(attr)
            lod = mc.getAttr(lodAttr)

            # instance asset.info
            asset = entityInfo.info('%s/_%s' % (ref, lod))
            dataPath = asset.getPath('refData')
            dataFile = asset.getRefNaming('vrayNodeData')
            dataFilePath = '%s/%s' % (dataPath, dataFile)

            if not dataFilePath in dataFiles : 
                dataFiles.append(dataFilePath)

    if dataFiles : 
        for dataFile in dataFiles : 
            if os.path.exists(dataFile) : 
                importVrayNodes(dataFile)

            else : 
                print 'Path not exists %s' % dataFile


def doImportVrayNodes() :
    # Get from Shade 
    allRefs = mc.file(q = True, r = True)

    refPaths = []

    for ref in allRefs : 
        lod = pipelineTools.getFileTask(os.path.basename(ref))
        refPath = os.path.dirname(ref)

        # instance asset.info
        asset = entityInfo.info('%s/_%s' % (refPath, lod))
        dataPath = asset.getPath('refData')
        dataFile = asset.getRefNaming('vrayNodeData')
        dataFilePath = '%s/%s' % (dataPath, dataFile)

        if os.path.exists(dataFilePath) : 
            importVrayNodes(dataFilePath)
            print 'import vray node %s' % dataFilePath

        else : 
            print 'Skip -> File not found %s' % dataFilePath


def getAssetInfo(targetAssetName = None) : 
    grps = mc.ls('*:Geo_Grp')

    info = dict()

    for each in grps : 
        attr = '%s.assetName' % each 
        if mc.objExists(attr) : 
            assetName = mc.getAttr(attr)
            namespace = each.split(':')[0]
            con = False

            if targetAssetName : 
                if assetName == targetAssetName : 
                    con = True

            else : 
                con = True

            if con : 
                if not assetName in info.keys() : 
                    info.update({assetName: [namespace]})
                    
                else : 
                    info[assetName].append(namespace)

    return info


def cleanFile(inputFile) : 
    tmp = '%s_tmp.tmp' % inputFile.split('.')[0]
    f = open(inputFile, 'r')
    f2 = open(tmp, 'w')

    for each in f : 
        line = each.replace('lockNode -l 1 ;', '')
        f2.write(line)
        
    f.close()
    f2.close()

    os.remove(inputFile)
    os.rename(tmp, inputFile)
