import serial
import sys
from threading import Lock

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
    
    def sendCommand(self, addr, command):
        pass
    
    def sendCommand2(self, addr, command):
        pass
    
    def sendData(self, data):
        pass
    
    def disconnect(self):
        pass
        
    def getPosition(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        ans = self.sendCommand(addr, '?P')
        return self.parseResponse(str(addr),"P", ans)
    
    def readPar(self, addr, name):
        if (self.Status == CStatus.Disconnected):
            return -1
        ans = self.sendCommand(addr, '?'+name)
        return self.parseResponse(str(addr),name, ans)
    
    def writePar(self, addr, name, val):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr, name+ " " + val)
    
    def getStatus(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        ans = self.sendCommand(None, '?STAT '+ str(addr))
        return self.parseResponse(None,"STAT", ans)
    
    def isMoving(self, addr):
        ans = self.sendCommand(addr, '?ST')
        return self.parseResponse(str(addr),"ST", ans)
    
    def getSpeed(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        ans = self.sendCommand(addr, '?VSR')
        return self.parseResponse(str(addr),"VSR", ans)
    
    def getBaseRate(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        ans = self.sendCommand(addr, '?V0')
        return self.parseResponse(str(addr),"V0", ans)
    
    def getLimitSwitches(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        ans = self.sendCommand(addr, '?SW')
        ans = self.parseResponse(str(addr),"SW", ans)
        return ans.split()
        
    
    def getAcceleration(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        ans = self.sendCommand(addr, '?A0')
        return self.parseResponse(str(addr),"A0", ans)
    
    def getCurrent(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        ans = self.sendCommand(addr, '?IN')
        return self.parseResponse(str(addr),"IN", ans)
        
    def setSpeed(self, addr, Speed):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr , 'VSR %d' % Speed)
    
    def setBaseRate(self, addr, Speed):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr , 'V0 %d' % Speed)
    
    def setAcceleration(self, addr, Acc):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr , 'A0 %d' % Acc)
    
    def setPosition(self, addr, Pos):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr , 'P %d' % Pos)
    
    def setDirection(self, addr, Dir):
        if (self.Status == CStatus.Disconnected):
            return -1
        
        self.sendCommand2(addr , 'DIR %d' % Dir)

    
    def stopMotor(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr , 'STOP')

    def abortMotor(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr , 'ABORT')
    
    def go(self, addr, steps):
        if (self.Status == CStatus.Disconnected):
            return -1
        #print 'GO '+str(steps)
        #self.preStart(addr)
        self.sendCommand2(addr, 'GO '+str(steps))
    
    def configureInputSignal(self, addr, signal, cfg):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr, 'IN2_C '+str(signal) + ' ' + str(cfg))
    
    def configureOutputSignal(self, addr, signal, source, cfg):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr, 'OUT2_C '+str(signal) + ' ' + str(source) + ' ' + str(cfg))
    
    def setSignalDirection(self, addr, signal, dir):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr, 'SIG_DIR '+str(signal) + ' ' + str(dir)) 
    
    def setCounterSource(self, addr, counter, src):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr, 'SET_SRC '+str(counter) + ' ' + str(src))
    
    def setSilent(self, addr, mode):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr , 'SILENT %d' % mode)
                
    def disable(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr , 'CLR')
        self.sendCommand2(addr , 'DIS')
    
    def enable(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr , 'CLR')
        self.sendCommand2(addr , 'EN')         
        
    
    def preStart(self, addr):
        if (self.Status == CStatus.Disconnected):
            return -1
        ans= self.sendCommand(addr , '?CPLD 0')
        try:
            vans = ans.split()
            #print 'prestart %s' % ans
            if int(vans[2]) & 0x0020:
                self.sendCommand2(addr , 'CLR')
                self.sendCommand2(addr , 'EN')
        except:
            ans = self.IceCheckError(ans)
            iex = IcePAPException(IcePAPException.Error, ans)
            raise iex
    
    def checkDriver(self, addr):
        #print "checking driver"
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(0 , 'CFE')
        
        ans= self.sendCommand(addr , '?ID')
        #print ans
        if self.IceFindError(ans):
            return -1
        self.sendCommand2(addr , 'CLR')
        self.sendCommand2(addr , 'DIS') 
        self.sendCommand2(addr , 'SD 10.0')
	
        #ans= self.sendCommand(0 , '?FERR 1')
        #print 'check %s' % ans
        #if  not ans.startswith(" FERR"):
        #    self.icepapfiforst()
        #    return -1
        ##ans = ans.lstrip(" FERR ")
        #print 'check %s' % ans      
        #print addr + ans  
        #if ans == "OK":
        #    return 0
        #self.icepapfiforst()
        return 0
    
    def icepapfiforst(self):
        print ""
        #self.sendCommand2(0 , 'fiforst')
      
    
    def parseResponse(self, addr, command, ans):
        # parsing for both version of icepap firmware
        expr = command
        
        if addr is None:
            expr = "?"+command
        else:
            expr = addr+":?"+command
            
        if ans.find(expr) != -1:
            ans = ans.lstrip()
            ans = ans.lstrip(expr)
            return  ans
        elif ans.find(command) != -1:
            ans = ans.lstrip()
            ans = ans.lstrip(command)
            return  ans
        else:
            print ans + " " + command        
            error = self.IceCheckError(ans)
            iex = IcePAPException(IcePAPException.Error, error)
            raise iex
            
    def IceFindError(self,ice_answer):
        if (ice_answer.find("ERROR") != -1):
            return True
        else:
            return False
        
    def IceCheckError(self,ice_answer):
        if (ice_answer.find("ERROR") != -1):
            new_ans = self.sendCommand(0, "?ERR 1")
            print new_ans + " in IceCheckError"
            return new_ans
        else:
            return "IcePAPError. Not Identified"
      
    def configureInputSignal(self, addr, signal, cfg):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr, 'IN2_C '+str(signal) + ' ' + str(cfg))
    
    def configureOutputSignal(self, addr, signal, source, cfg):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr, 'OUT2_C '+str(signal) + ' ' + str(source) + ' ' + str(cfg))
    
    def setSignalDirection(self, addr, signal, dir):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr, 'SIG_DIR '+str(signal) + ' ' + str(dir)) 
    
    def setCounterSource(self, addr, counter, src):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr, 'SET_SRC '+str(counter) + ' ' + str(src))
    
    def setSilent(self, addr, mode):
        if (self.Status == CStatus.Disconnected):
            return -1
        self.sendCommand2(addr , 'SILENT %d' % mode)
        
    
    def selectMotor(self, crate, motor):
        self.motoraddr = int((crate * 10) + int(motor))
        #self.preStart()
        #return self.getStatus()
    
    def selectMotorAddr(self, addr):
        self.motoraddr = int(addr)
        return self.getStatus()
        
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
    

    
