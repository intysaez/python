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
#declaring the variable with in the program
import constants as cts
import ruamel.yaml as yaml

class loadConfig():

    __cfg = object

    def __init__(self):
        self.loadConfig()

    def getCfg(self):
        return self.__cfg
#loading the configuration file deatils as server needed
    def loadConfig(self):
        try:
            self.__cfg = yaml.load(open(cts.configFileName,'r').read(), yaml.RoundTripLoader)
        except yaml.YAMLError as exc:
            print('Error during load yml config file' + exc)
