'''
    Author zombie(c) 20016
    Python Class, Fall C 2016

    A repository file manager
    Repo manage files from project
    Main features:
        persist features list
        keep features list tracked
        compute differences between files
        compare old/new features
        generate update list
'''

import os
import sys
import fileSystemUtils as fs
import remoteSynch as rsyn

class reposManager():

    def __init__(self):
        pass

    def isLocal(self, address):
        if sys.platform != 'win32':
            return bool(str(address[0]).startswith('/'))
        else:
            return bool(str(address[0]).isalpha())

    def cleanPath(self,path):
        return bytes(path, "utf-8").decode("unicode_escape")

    def getListOfFile(self, address):
        if self.isLocal(address):
            if fs.is_path_exists_or_creatable(address):
                return os.listdir(address)
            else:
                return ['Not current working directory']
        else:
            #Under Unix system, UNC use the following format for network file address
            if len(fs.sshRemote(address)) != 0:
                #Read a remote address and get back the files list
                remote = rsyn.remoteSync()
                return remote.getFileList(address)


