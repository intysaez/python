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

import constants as cts
import ruamel.yaml as yaml

class loadConfig(object):

    def __init__(self):
        self.loadCfg()

    def loadCfg(self):
        try:
            result = yaml.load(open(cts.configFileName,'r').read(), yaml.RoundTripLoader)
        except yaml.YAMLError as exc:
            print('Error during load yml config file' + exc)
        return result