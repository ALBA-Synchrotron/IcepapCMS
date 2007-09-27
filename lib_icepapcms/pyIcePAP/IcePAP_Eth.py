import socket
import struct
from IcePAP import *
import time
from errno import EWOULDBLOCK
import icepapdef

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
        
        try:
            self.IcPaSock.connect((self.IcePAPhost, self.IcePAPport))
        except socket.error, msg:
            
            iex = IcePAPException(IcePAPException.TIMEOUT, "Error connecting to the Icepap")
            raise iex
        self.Status = CStatus.Connected
        #self.IcPaSock.settimeout( 0 )
        #print "connected"
        return 0
    
    def sendWriteReadCommand(self, cmd, size = 8192):
        try:
            cmd = cmd + "\n"
            self.lock.acquire()
            self.IcPaSock.send(cmd)          
            data = self.IcPaSock.recv(size)
            self.lock.release()                      
            return data
        except socket.timeout, msg:
            self.disconnect()   
            self.lock.release()              
            iex = IcePAPException(IcePAPException.TIMEOUT, "Connection Timeout")
            raise iex
        except socket.error, msg:
            self.lock.release()  
            print msg
            print "Unexpected error:", sys.exc_info()            
            iex = IcePAPException(IcePAPException.ERROR, "Error sending command to the Icepap")
            raise iex          
        

    
    def sendWriteCommand(self, cmd):
        try:
            cmd = cmd + "\n"
            self.lock.acquire()
            self.IcPaSock.send(cmd)
            self.lock.release()
        except socket.timeout, msg:
            self.disconnect()      
            self.lock.release()           
            iex = IcePAPException(IcePAPException.TIMEOUT, "Connection Timeout")
            raise iex            
        except socket.error, msg:
            self.lock.release()  
            print "Unexpected error:", sys.exc_info()
            iex = IcePAPException(IcePAPException.ERROR, "Error sending command to the Icepap")
            raise iex   
            
        
    def sendData(self, data):
        try:
            self.lock.acquire()
            self.IcPaSock.send(data)            
            self.lock.release()
        except socket.timeout, msg:  
            self.disconnect()          
            iex = IcePAPException(IcePAPException.TIMEOUT, "Connection Timeout")
            raise iex
        except socket.error, msg:
            print msg
            iex = IcePAPException(IcePAPException.ERROR, "Error sending data to the Icepap")
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
            iex = IcePAPException(IcePAPException.ERROR, "Error disconnecting the Icepap")
            raise iex   
        
  

