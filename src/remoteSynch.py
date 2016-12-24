'''
    Author zombie(c) 20016
    Python Class, Fall C 2016
'''


from loadCfg import loadConfig
from contextlib import closing
import tempfile
import os
import paramiko
import re
import stat


class remoteSync(loadConfig):

    def __init__(self, cfgpath):
        loadConfig.__init__(self, cfgpath)
        self.__initializeCfg()
        self.__initializeLogFile()
        self.__initializeSftp()
        self.__sftpConnect()

    def __initializeLogFile(self):
        # Log file for debug all paramiko module activities
        logFile = tempfile.mkstemp('.log','ssh-')[1]
        paramiko.util.log_to_file(logFile)


    def __initializeCfg(self):
        #Load config key-value
        self._cfg = loadConfig.getCfg(self)

    def __initializeSftp(self):
        # Initialize the connection to secure file transfer protocol
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


    # Open a paramiko SSHClient Transport Socket
    def ___openSock(self):
        self._sftp = paramiko.SFTPClient.from_transport(self._transport)

    # Open paramiko SSHClient Transport Sock at the first time
    def __sftpConnect(self):
        # Establish sftp connection and set _sftp class variable
        if isinstance(self._sftp,(int)):
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        else:
            if self._sftp.sock._closed:
                self._sftp = paramiko.SFTPClient.from_transport(self._transport)


    # Will get a file: from remote by local request
    def get(self, remotepath, localpath=None):
        pass

    # Return a current directory where SSHClient are
    def getRemoteCWD(self):
        # Get current working directory on remote machine. By default, SFTP do not have a current working directory concep.
        # paramiko module emulate the working directory
        with self._sftp as sftp:
            cwd = sftp.getcwd()
        return cwd


    # Perform a local iteration over a local directory
    def __lcl_PathIterator(self, path, files=True):
        result = []
        if files:
            for filename in os.listdir(path):
                result.append(filename)
        else:
            result = [items[0] for items in os.walk(path)]
        return result

    # Change the current directory by dir in remote machine
    def __rmt_Chdir(self, dir):
        if self.getRemoteCWD() != dir:
            self._sftp.chdir(dir)


    # Emulate a walk on remote machine like os.walk on local
    def __rmt_walk(self, dir, container):
        for filename in self._sftp.listdir(dir):
            container.append(''.join([dir, '/', filename]))


    # Perform a iteration over a remote directory, add to the list all files in each directory
    def __rmt_PathIterator(self, path, files=True):
        result = []
        self.__rmt_Chdir(path)
        # After any operation over sftp, the transport close the socket on the channel
        if files:
            self.___openSock()
            # If directory is not empty
            if len(self._sftp.listdir_attr(path)) > 1:
                for attr in self._sftp.listdir_attr(path):
                    if stat.S_ISDIR(attr.st_mode):
                        self.__rmt_walk(attr.filename, result)
                    else:
                        result.append(''.join([path, '/', attr.filename]))
        else:
            # The last operation close the sock, re-open is required
            self.___openSock()
            with closing(self._sftp) as sftp:
                for attr in self._sftp.listdir_attr(path):
                    if stat.S_ISDIR(attr.st_mode):
                        result.append(attr.filename)
        return result


    # Ask and return True or False if path exist on remote machine
    def __rmt_Is_pathName_valid(self, pathName):
        with self._sftp as sftp:
            try:
                sftp.chdir(pathName)
            except OSError:
                return False
        return True


    # Get all files on address directory
    # Check if address is local or remote
    def getList(self, address, files=True):
        pattern = re.compile('(\w+)@(\w+\D+)(:){1}(\w+\D+\w+)')
        result = []
        if pattern.search(address) != None:
            # Remote address
            if not self.__rmt_Is_pathName_valid(''.join(['/', address.split(':')[1]])):
                path = ''.join([self._cfg['remote']['prefix'], self._cfg['remote']['host']['username'],'/', address.split(':')[1]])
            else:
                path = ''.join(['/', address.split(':')[1]])
            result = self.__rmt_PathIterator(path, files)
        else:
            result = self.__lcl_PathIterator(address, files)

        return result



