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


from loadCfg import loadConfig
from contextlib import closing
import sys
import os
import paramiko
from paramiko import SSHConfig, SSHClient
import constants as cts



#Remote connection Sync will be making transfer between two lines
class remoteSync(loadConfig):

    def __init__(self):
        loadConfig.__init__(self)

    def __sshConnection(self):
        result = []
        sshCfg = SSHConfig()
        cfg = loadConfig.getCfg(self)

        #Check if local ssh config exist
        if os.path.isfile('~/.ssh/config'):
            with open(os.path.expanduser('~/.ssh/config')) as cfg_file:
                sshCfg.parse(cfg_file)
                if bool(sshCfg.lookup(cfg['remote']['host']['hostName'])):
                    pass
#Connection between two with policy ,hotkey and system
        if bool(sshCfg.lookup(cfg['remote']['host']['hostName'])):
            with closing(SSHClient()) as ssh:
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                if cfg['remote']['host']['port'] != cts.rtptclport:
                    ssh.connect(cfg['remote']['host']['hostName'], cfg['remote']['host']['port'],username=cfg['remote']['host']['username'])
                else:
                    ssh.connect(cfg['remote']['host']['hostName'], username=cfg['remote']['host']['username'], key_filename=cfg['remote']['host']['sshKeyFile'])

        return ssh


    def getRemoteFileList(self):
        result = []
        connection = self.__sshConnection()
        with closing(connection.open_sftp()) as sftp:
            with loadConfig.getCfg(self) as cfg:
                sftp.chdir(cfg['remote']['libDir'])
                for filename in sftp.listdir():
                    result.append(sftp.get(filename, filename))
        return result



