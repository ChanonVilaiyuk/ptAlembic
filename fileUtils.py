import os, sys 

def listFile(path,ex=''):
    dirs = []
    try:
        for i in [d for d in os.listdir(path) if os.path.isfile(os.path.join(path, d))]:
            if len(ex):
                if i.split('.')[-1] == ex:
                    dirs.append(i)
            else:
                dirs.append(i)
        return sorted(dirs)
    except:
        return dirs 


def listFolder(path):
    dirs = []
    try:
        for i in [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]:
            dirs.append(i)
        return sorted(dirs)
    except:
        return dirs  