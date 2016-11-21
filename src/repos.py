
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
import hashlib
import ruamel.yaml as yaml
import constants as cts
import pickle

#Let read stuff in 64Kb chunck
BUF_SIZE = 65536


class featuresMgt:
    __featuresList = {}
    __cfg = object

    def __init__(self):
        self.loadCfg()



    def serialize(self, who, where):
        with open(where, 'wb') as handle:
            pickle.dump(who, handle)


    def fileSignature(self, aFile):
        sha1 = hashlib.sha1()
        with open(aFile, 'rb') as el:
            while True:
                data = el.read(BUF_SIZE)
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()

    def loadCfg(self):
        try:
            self.__cfg = yaml.load(open(cts.configFileName,'r').read(), yaml.RoundTripLoader)
        except yaml.YAMLError as exc:
            print('Error during load yml config file' + exc)

        #Read installed features list from file
        files = os.listdir(self.__cfg['lib']['libDir'])
        if os.stat(self.__cfg['features']['file']).st_size != 0:
            with open(self.__cfg['features']['file'],'rb') as handle:
                self.__featuresList = pickle.loads(handle.read())

        else:
            #First time: create the list of features ignoring ignore list
            list = {}
            for file in os.listdir(self.__cfg['lib']['libDir']):
                if os.path.isdir(file) == False and file not in open(cts.featureIgnore,'rb'):
                    list[str(self.fileSignature(file))] = file
            #Serialize list object
            self.serialize(list, self.__cfg['features']['file'])
            self.__featuresList = list

    def getFeatures(self):
        return self.__featuresList

    # Check if exist differences with the original set of features
    def __diff(self):
        diff = {}
        files = os.listdir(self.__cfg['lib']['libDir'])
        for file in files:
            if (os.path.isdir(file) == False) and (file != self.__cfg['features']['file']):
                signature = self.fileSignature(file)
                if signature not in self.__featuresList:
                    diff[str(signature)] = file
        return diff

    def updateList(self):
        return list((value for value in self.__diff().values()))

    def reportDiff(self):
        import difflib as Compare

        upList = self.updateList()
        result = []
        #Compare one by one
        for el in upList:
            if el in self.getFeatures().values():
                compare = self.__cfg['repos']['folder'] + el
                if os.path.isfile(compare):
                    with open(el,'r') as source:
                        with open(compare,'r') as target:

                            for diff in Compare.unified_diff(source.readlines(), target.readlines()):
                                result.append(diff)
                    source.close()
                    target.close()
        return result

import pprint
test = featuresMgt()
print(test.getFeatures())
print('New features coming from: ')
print(test.updateList())
pprint.pprint(test.reportDiff())