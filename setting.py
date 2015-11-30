import sys, os 
import maya.cmds as mc

def getSceneInfo() : 
	currentScene = mc.file(q = True, location = True)
	sceneEles = currentScene.split('/')

	info = dict()

	if len(sceneEles) > 6 : 
		drive = sceneEles[0]
		basename = sceneEles[-1]
		project = sceneEles[1]
		episode = sceneEles[3]
		sequence = sceneEles[4]
		shot = sceneEles[5]
		dept = sceneEles[6]
		projectCode = sceneInfo.getCode('project', project)
		episodeCode = sceneInfo.getCode('episode', episode)

		info = {'drive': drive, 'fileName': basename, 'project': project, 
				'episode': episode, 'sequence': sequence, 'shot': shot, 
				'department': dept, 'projectCode': projectCode, 'episodeCode': episodeCode
				}

		return info


def cachePathInfo(increment = True) : 

	info = getSceneInfo()

	if info : 
		drive = info['drive']
		project = info['project']
		episode = info['episode']
		sequence = info['sequence']
		shot = info['shot']
		dept = info['department']
		basename = info['fileName']
		projectCode = info['projectCode']
		episodeCode = info['episodeCode']
		dataName = '%s_%s_%s_%s_list' % (projectCode, episodeCode, sequence, shot)
		cameraName = '%s' % shot 
		nonCacheFile = '%s_%s_%s_%s_nonCache' % (projectCode, episodeCode, sequence, shot)
		cameraName = '%s_%s_%s_%s_cam' % (projectCode, episodeCode, sequence, shot)

		if abcExport.exportDept == dept : 
			cachePath = '%s/%s/film/%s/%s/%s/%s/cache/alembic' % (drive, project, episode, sequence, shot, dept)
			cacheDir = '%s/%s/film/%s/%s/%s/%s/cache' % (drive, project, episode, sequence, shot, dept)
			dataPath = '%s/%s/film/%s/%s/%s/%s/cache/data/%s.yml' % (drive, project, episode, sequence, shot, dept, dataName)
			nonCacheDataPath = '%s/%s/film/%s/%s/%s/%s/cache/data/%s.yml' % (drive, project, episode, sequence, shot, dept, nonCacheFile)
			nonCachePath = '%s/%s/film/%s/%s/%s/%s/cache/nonCache' % (drive, project, episode, sequence, shot, dept)
			cameraPath = '%s/%s/film/%s/%s/%s/%s/cache/camera/%s.ma' % (drive, project, episode, sequence, shot, dept, cameraName)

			# list version 
			version = abcExport.findVersion(cachePath, increment)
			exportPath = '%s/%s' % (cachePath, version)
			
			return {'cachePath': exportPath, 'dataPath': dataPath, 'nonCachePath': nonCachePath, 'nonCacheDataPath': nonCacheDataPath, 'cacheDir': cacheDir, 'cameraPath': cameraPath}