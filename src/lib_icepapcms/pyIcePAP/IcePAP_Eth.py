import socket
import struct
from IcePAP import *


class EthIcePAP(IcePAP):

    def connect(self):
        #print "connecting"
        if (self.Status == CStatus.Connected):
            return 0
        self.IcPaSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IcPaSock.settimeout( self.timeout )
        NOLINGER = struct.pack('ii', 1, 0)
        self.IcPaSock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, NOLINGER)
        
        try:
            self.IcPaSock.connect((self.IcePAPhost, self.IcePAPport))
        except socket.error, msg:
            print msg
            iex = IcePAPException(IcePAPException.Error, "Error connecting command to the Icepap")
            raise iex
        self.Status = CStatus.Connected
        #print "connected"
        return 0
    
    def sendCommand(self, addr, command):
        try:
            cmd = ''
            if not addr is None:
                cmd = '%d:'% addr
            cmd = cmd + command + "\n"
            #print cmd
            self.lock.acquire()
            self.IcPaSock.send(cmd)
            newdata = self.IcPaSock.recv(2024)
            self.lock.release()
            return newdata
        except socket.error,msg:
            print command 
            print msg
            #self.disconnect()
            iex = IcePAPException(IcePAPException.Error, "Error sending command to the Icepap")
            raise iex
            
        
        
    
    def sendCommand2(self, addr, command):
        try:
            cmd = ''
            if not addr is None:
                cmd = '%d:'% int(addr)
            cmd = cmd + command + "\n"
	    #print cmd
            self.lock.acquire()
            self.IcPaSock.send(cmd)
            self.lock.release()            
        except socket.error, msg:
            print command 
            print msg
            iex = IcePAPException(IcePAPException.Error, "Error sending command to the Icepap")
            raise iex   
            
        
    def sendData(self, data):
        try:
            self.lock.acquire()
            self.IcPaSock.send(data)            
            self.lock.release()
        except socket.error, msg:
            print msg
            iex = IcePAPException(IcePAPException.Error, "Error sending data to the Icepap")
            raise iex   
    
    def disconnect(self):
        #print "Disconnecting ..."
        if (self.Status == CStatus.Disconnected):
            return 0
        try:
            self.IcPaSock.close()
            self.Status = CStatus.Disconnected
            return 0
        except:
            iex = IcePAPException(IcePAPException.Error, "Error disconnecting the Icepap")
            raise iex   
        
  

