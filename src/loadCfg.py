'''
    Author zombie(c) 20016
    Python Class, Fall C 2016

    '''

import constants as cts
import ruamel.yaml as yaml
import ruamel.yaml.comments as ymlClass

class loadConfig():

    __cfg = object

    def __init__(self):
        self.loadConfig()

    def getCfg(self):
        return self.__cfg

    def loadConfig(self):
        try:
            self.__cfg = yaml.load(open(cts.configFileName,'r').read(), yaml.RoundTripLoader)
        except yaml.YAMLError as exc:
            print('Error during load yml config file' + exc)


    def get(self, key, inside = None):
        if isinstance(key, ymlClass.CommentedMap):
            if inside != None:
                if len(inside.split('->')) > 1:
                    return self.get(key[inside.split('->')[0]], inside[inside.find(inside.split('->')[1]):len(inside)])
                else:
                    return key[inside]
        else:
            if len(key.split('->')) > 1:
                return self.get(self.__cfg[key.split('->')[0]], key[key.find(key.split('->')[1]):len(key)])
            else:
                if isinstance(self.__cfg[key], ymlClass.CommentedMap):
                    return iter(self.__cfg[key])
                else:
                    return self.__cfg[key]



test = loadConfig()
# print(test.get('remote->host->sshKeyFile'))
print(test.get('repos->folder'))