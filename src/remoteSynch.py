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
import tempfile
import os
import getpass
import paramiko
from paramiko import SSHConfig, SSHClient
import constants as cts




class remoteSync(loadConfig):

    def __init__(self):
        loadConfig.__init__(self)

        logFile = tempfile.mkstemp('.log','ssh-')[1]
        paramiko.util.log_to_file(logFile)

        #Load config key-value
        self._cfg = loadConfig.getCfg(self)

        self._sftp_life = False
        self._sftp = False

        if self._cfg['remote']['host']['username'] == None:
            self._transport = paramiko.Transport((os.environ['LOGNAME'], 22))
        else:
            self._transport = paramiko.Transport((self._cfg['remote']['host']['hostName'],int(self._cfg['remote']['host']['port'])))

        self._transport_live = True

        if self._cfg['remote']['host']['pass'] != None:
            self._transport.connect(username=self._cfg['remote']['host']['username'], password= self._cfg['remote']['host']['pass'])
        else:
            #User private key
            if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
                private_key = '~/.ssh/id_rsa'
            elif os.path.exists(os.path.expanduser('~/.ssh/id_dsa')):
                private_key = '~/.ssh/id_dsa'
            else:
                raise TypeError('You have not specified a password or key')
            private_key_file = os.path.expanduser(private_key)
            rsa_key = paramiko.RSAKey.from_private_key_file(private_key_file)
            private_key = None
            self._transport.connect(username= self._cfg['remote']['host']['username'], pkey= rsa_key)

    def _sftpConnect(self):
        if not self._sftp_life:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp_life = True

    def get(self, remotepath, localpath=None):
        pass


    def getRemoteCWD(self):
        self._sftpConnect()
        with closing(self._sftp) as sftp:
            cwd = sftp.getcwd()
        return cwd


    def getRemoteFileList(self, address):
        result = []
        self._sftpConnect()
        remotePath = ''.join([self._cfg['remote']['prefix'], self._cfg['remote']['host']['username'],'/', address])
        with closing(self._sftp) as sftp:
            sftp.chdir(remotePath)
            for filename in sftp.listdir():
                result.append(filename)
        return result



