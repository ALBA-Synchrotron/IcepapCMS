
class IcepapMode:
    CONFIG, OPER = "CONFIG", "OPER"

class IcepapAnswers:
    ON, OFF = "ON", "OFF"
    
class IcepapStatus:
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

