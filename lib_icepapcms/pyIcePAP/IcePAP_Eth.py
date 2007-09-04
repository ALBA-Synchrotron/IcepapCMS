import socket
import struct
from IcePAP import *
import time
from errno import EWOULDBLOCK


class EthIcePAP(IcePAP):

    def connect(self):
        #print "connecting"
        if (self.Status == CStatus.Connected):
            return 0
        self.IcPaSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IcPaSock.settimeout( self.timeout )
        #self.IcPaSock.settimeout( 0.001 )
        
        NOLINGER = struct.pack('ii', 1, 0)
        self.IcPaSock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, NOLINGER)
        #self.IcPaSock.setblocking(0)
        try:
            self.IcPaSock.connect((self.IcePAPhost, self.IcePAPport))
        except socket.error, msg:
            print msg
            iex = IcePAPException(IcePAPException.Error, "Error connecting command to the Icepap")
            raise iex
        self.Status = CStatus.Connected
        #self.IcPaSock.settimeout( 0 )
        #print "connected"
        return 0
    
    def sendWriteReadCommand(self, addr, command):
        try:
            cmd = ''
            if not addr is None:
                cmd = '%d:'% addr
            
            cmd = cmd + command + "\n"
            
            
            self.lock.acquire()
            self.IcPaSock.send(cmd)
            #b = time.time()
            #print str(b) + "  " + cmd 
            
            #try:
            data = self.IcPaSock.recv(8192)
           
            c = time.time()
            #print str(c) + "---" + str(c-b)
            #print cmd + answer
            self.lock.release()  
                      
            return data
        except socket.error,msg:
            #print command 
            #print msg
            print "Unexpected error:", sys.exc_info()
            #if se.args[0] == EWOULDBLOCK:
            #    return 
            iex = IcePAPException(IcePAPException.Error, "Error sending command to the Icepap")
            raise iex
            
        

    
    def sendWriteCommand(self, addr, command):
        try:
            cmd = ''
            if not addr is None:
                cmd = '%d:'% int(addr)
            cmd = cmd + command + "\n"
            
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
        
  

