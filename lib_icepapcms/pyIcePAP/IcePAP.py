#PyIcepap for Icepap version 1.52
import serial
import sys
from threading import Lock
import time

class CStatus:
    Disconnected, Connected, Error = range(3)


class IcePAPStatus:
    @staticmethod
    def isPresent(register):
        val = register >> 0
        val = val & 1
        return val
    @staticmethod
    def isAlive(register):
        val = register >> 1
        val = val & 1
        return val
    @staticmethod
    def getMode(register):
        val = register >> 2
        val = val & 3
        return val
    @staticmethod
    def isDisabled(register):
        val = register >> 4
        val = val & 7
        return val
    @staticmethod
    def isReady(register):
        val = register >> 9
        val = val & 1
        return val
    @staticmethod
    def isMoving(register):
        val = register >> 10
        val = val & 1
        return val
    @staticmethod
    def getLimitPositive(register):
        val = register >> 18
        val = val & 1
        return val
    @staticmethod
    def getLimitNegative(register):
        val = register >> 19
        val = val & 1
        return val
    @staticmethod
    def inHome(register):
        val = register >> 20
        val = val & 1
        return val
            
class IcePAPException:
    Error = range(1)
    def __init__(self, code, name):
        self.code = code
        self.name = name


class IcePAP:
    
    
    def __init__(self, host,port, timeout = 1):
        #print "IcePAP object created"
        self.IcePAPhost = host
        self.IcePAPport = int(port)
        self.Status = CStatus.Disconnected
        self.timeout = timeout
        self.lock = Lock()
           
    def connect(self):
        pass
    
    def sendWriteReadCommand(self, addr, command):
        pass
    
    def sendWriteCommand(self, addr, command):
        pass
    
    def sendData(self, data):
        pass
    
    def disconnect(self):
        pass

    # ------------ Board Configuration and Identifaction Commands ------------------------------
    
    def parseResponse(self, command, ans):
        if ans.find(command) != -1:
            #print ans
            ans = ans.replace(command, "")
            ans = ans.lstrip()
            #print ans
            return  ans
        else:
            print ans + " " + command
            iex = IcePAPException(IcePAPException.Error,ans)
            raise iex
    
    def setCfgParameter(self, addr, parameter, value):
        command = "%d:CFG %s %s" % (addr, parameter, value)
        self.sendWriteCommand(command)
    
    def getCfgParamenter(self, addr, parameter):
        command = "%d:?CFG %s" % (addr, parameter)
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
    
    def startConfig(self, addr):
        command = "%d:CONFIG" % addr
        self.sendWriteCommand(command)
        
    def getConfigSignature(self, addr):
        command = "%d:?CONFIG" % addr
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
    
    def signConfig(self, addr, signature):
        command = "%d:CONFIG %s" % (addr, signature)
        self.sendWriteCommand(command)
   
    def setMode(self, addr, mode):
        command = "%d:NAME %s" % (addr, mode)
        self.sendWriteCommand(command)
    
    def getMode(self, addr):
        command = "%d:?MODE" % addr
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
    
    def getVersionDsp(self, addr):
        return self.getVersion(addr, "DSP")
    
    def getVersion(self, addr, module):
        command = "%d:?VER %s" % (addr, module)
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse("%d:?VER" % addr, ans)    
            
    def getId(self, addr):
        command = "%d:?ID HW" % addr
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse("%d:?ID" % addr, ans)
    
    def getName(self, addr):
        command = "%d:?NAME" % addr
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
    
    def setName(self, addr, name):
        command = "%d:NAME %s" % (addr, name)
        self.sendWriteCommand(command)

    def getCurrent(self, addr):
        return self.getCfgParamenter(addr, "NCURR")
    
    def move_in_config(self, addr, steps):
        command = "%d:CMOVE %d " % (addr, steps)
        self.sendWriteCommand(command)
        
    # ------------ Power and Motion control Commands ------------------------------      
    def readParameter(self, addr, name, args = ""):
        command = "%d:?%s %s" % (addr, name, args)
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse("%d:?%s" % (addr, name) , ans)
        
    def writeParameter(self, addr, name, value):
        command = "%d:%s %s" % (addr, name, value)
        self.sendWriteCommand(command)
        
    def getPower(self, addr):
        command = "%d:?POWER" % addr
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
    
    def setPower(self, addr, value):
        command = "%d:POWER %s" % (addr, value)
        self.sendWriteCommand(command)
    
    def disable(self, addr):
        self.setPower(addr, "OFF")
    
    def enable(self, addr):
        self.setPower(addr, "ON")
    
    def getAuxPS(self, addr):
        command = "%d:?AUXPS" % addr
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
    
    def setAuxPS(self, addr, value):
        command = "%d:AUXPS %s" % (addr, value)
        self.sendWriteCommand(command)
        
    def getPosition(self, addr, pos_sel = "AXIS"):
        command = "%d:?POS %s" % (addr, pos_sel)
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse("%d:?POS" % addr, ans)
    
    def setPosition(self, addr, pos_val, pos_sel = "AXIS"):
        command = "%d:POS %s %d" % (addr, pos_sel, pos_val)
        self.sendWriteCommand(command)
    
    def getEncoder(self, addr, pos_sel = "AXIS"):
        command = "%d:?ENC %s" % (addr, pos_sel)
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse("%d:?ENC" % addr, ans)
    
    def setEncoder(self, addr, pos_val, pos_sel = "AXIS"):
        command = "%d:ENC %s %d" % (addr, pos_sel, pos_val)
        self.sendWriteCommand(command)
    
    def getSpeed(self, addr):
        command = "%d:?VELOCITY" % addr
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
        
    def setSpeed(self, addr, speed):
        command = "%d:VELOCITY %s" % (addr, speed)
        self.sendWriteCommand(command)
    
    def getAcceleration(self, addr):
        command = "%d:?ACCTIME" % addr
        print command
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
        
    def setAcceleration(self, addr, acctime):
        command = "%d:ACCTIME %s" % (addr, acctime)
        self.sendWriteCommand(command)
    
    def getStatus(self, addr):
        command = "%d:?STATUS" % addr
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
    
    def getRackStatus(self, racknr):
        command = "?SYSSTAT %d" % racknr
        ans = self.sendWriteReadCommand(command)
        ans = self.parseResponse("?SYSSTAT", ans)
        return ans.split()
        
    def getSysStatus(self):
        command = "?SYSSTAT"
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
   
    def stopMotor(self, addr):
        command = "%d:STOP" % addr
        self.sendWriteCommand(command)

    def abortMotor(self, addr):
        command = "%d:ABORT" % addr
        self.sendWriteCommand(command)
    
    def rmove(self, addr, steps):
        command = "%d:RMOVE %d " % (addr, steps)
        self.sendWriteCommand(command)
    
    def rmove(self, addr, steps):
        command = "%d:CMOVE %d " % (addr, steps)
        self.sendWriteCommand(command)
    
    def move(self, addr, abs_pos):
        command = "%d:MOVE %d " % (addr, abs_pos)
        self.sendWriteCommand(command)                
       
    
    def jog(self, addr, speed):
        self.sendWriteCommand(addr, 'J '+str(speed))
    
    # ------------- Input/Output commands ------------------------
    def setIndexerSource(self, addr, src):
        command = "%d:ACCTIME %s" % (addr, src)
        self.sendWriteCommand(command)
        
    def getIndexerSource(self, addr):
        command = "%d:?INDEXER" % addr
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
    
    def setInfoSource(self, addr, info, src, polarity="NORMAL"):
        command = "%d:%s %s %s" % (addr, info, src, polarity)
        self.sendWriteCommand(command)
        
    def getInfoSource(self, addr, info):
        command = "%d:?%s" % (addr, info)
        ans = self.sendWriteReadCommand(command)
        return self.parseResponse(command, ans)
    
        
    def setSilent(self, addr, mode):
        self.sendWriteCommand(addr , 'SILENT %d' % mode)
                
     
    def preStart(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        ans= self.sendWriteReadCommand(addr , '?CPLD 0')
        try:
            vans = ans.split()
            #print 'prestart %s' % ans
            if int(vans[2]) & 0x0020:
                self.sendWriteCommand(addr , 'CLR')
                self.sendWriteCommand(addr , 'EN')
        except:
            ans = self.IceCheckError(ans)
            iex = IcePAPException(IcePAPException.Error, ans)
            raise iex
    
    def checkDriver(self, addr):
        #print "checking driver"
        
        ans= self.getId(addr)

        #if self.IceFindError(ans):
        #    return -1

        return 0
    
    def icepapfiforst(self):
        print ""

            
    def IceFindError(self,ice_answer):
        if (ice_answer.find("ERROR") != -1):
            return True
        else:
            return False
        
    def IceCheckError(self,ice_answer):
        if (ice_answer.find("ERROR") != -1):
            new_ans = self.sendWriteReadCommand(0, "?ERR 1")
            print new_ans + " in IceCheckError"
            return new_ans
        else:
            return "IcePAPError. Not Identified"
      
    
    def setSilent(self, addr, mode):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendWriteCommand(addr , 'SILENT %d' % mode)
        
   
        
    def serialScan():
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                #available.append( (i, s.portstr))
                available.append(s.portstr)
                s.close()   #explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        return available
    
    serialScan = staticmethod(serialScan)
    

    
