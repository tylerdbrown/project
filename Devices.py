import SetStatesIAPWS as ss

#A device can be a Nozzle, Turbine, Boiler, etc.  It consists of left and right nodes (n1, n2) of states for the inlet/outlet.  Additionally, there is a mass
#flow rate, m.  Q and W are what we want to know, which depends on the type of device (turbines, for example - assume no heat loss so Q=0 and W is just
#Q - W = m(delta(h)))
class Device(object):
    def __init__(self, n1, n2, m):
        self.n1, self.n2, self.m = n1, n2, m
        self.type = "undefined"
        self.Q = None
        self.W = None
        return
        
    def __str__(self):
        string = "Device " + self.type + "\n with left node = " + str(self.n1.__str__()) + " \nand right node = " + str(self.n2.__str__()) + " \nwith flow of " + str(self.m) + "\n"     
        if (self.Q is not None and self.W is not None):
            string = string + "Heat of : " + str(self.Q) + "\nWork of : " + str(self.W)
        return string
        
    def fixStates(self):
        #Fixes states - unless they are already fixed.  They are known to be fixed if they have an IAPWS attached
        #see SetStatesIAPWS.py's isFixed().  Moreover, if Q and W have already been determined, there is no need
        if self.isFixed() :
            return
        if self.n1.isFixed() is False:
            self.n1.setState()
        if self.n2.isFixed() is False :
            self.n2.setState()
        return
    
    def isFixed(self):
        if self.Q is not None and self.W is not None:
            return True
        return False
        
class WType(Device):
    #Supered with type Turbine or Compressor. The code won't know until 
    #Work is determined...
    def __init__(self, n1, n2, m):
        super(WType, self).__init__(n1, n2, m)
        self.type = "Turbine | Compressor | Pump"
        return
        
    def fixStates(self):
        #Assume isentropic
        super(WType, self).fixStates()
        if self.n1.s is not None and self.n2.s is None:
            self.n2.s = self.n1.s
        elif self.n1.s is None and self.n2.s is not None:
            self.n1.s = self.n2.s
        super(WType, self).fixStates()
        return
    
    #This method will give us Q and W and determine if it is acting as
    #a compressor/pump or turbine
    def getData(self):
        #assume adiabatic
        self.Q = 0
        if self.n1.isFixed() and self.n2.isFixed() :
            self.W = -1 * self.m * (self.n2.h - self.n1.h)
            if self.W > 0:
                self.type = "Turbine"
            elif self.W < 0:
                if self.n1.X == 0:
                    self.type = "Pump"
                else :
                    self.type = "Compressor"
            else:
                self.type = "QType, error?"
        else:
            print "USER ERROR: Cannot find work without fixed states!"
        return
        
class QType(Device):
    #Supered with type Boiler or Condensor.  The code won't know until
    #heat is determined...
    def __init__(self, n1, n2, m):
        super(QType, self).__init__(n1, n2, m)
        self.type = "Boiler | Evaporator | Condenser"
        return
        
    def fixStates(self):
        #Assumes constant pressure
        super(QType, self).fixStates()
        if self.n1.P is not None and self.n2.P is None:
            self.n2.P = self.n1.P
        elif self.n1.P is None and self.n2.P is not None:
            self.n1.P = self.n2.P
        super(QType, self).fixStates()
        return
    
    #This method will give us Q and W and determine if it is acting as 
    #a boiler/evaporator or condensor
    def getData(self):
        #assume no work is being done on/out
        self.W = 0
        if self.n1.isFixed() and self.n2.isFixed() :
            self.Q = -1 * self.m * (self.n2.iapws.h - self.n1.iapws.h)
            if self.Q > 0:
                self.type = "Condenser"
            elif self.Q < 0:
                #still can't tell if its a boiler of evaporator, but Qin 
                #suggests one of these
                self.type = "Boiler | Evaporator"
            else:
                self.type = "WType, error?"
        else:
            print "USER ERROR: Cannot find work without fixed states!"            
        return

class Throttle(Device):
    #Supered with type Boiler or Condensor.  The code won't know until
    #heat is determined...
    def __init__(self, n1, n2, m):
        super(Throttle, self).__init__(n1, n2, m)
        self.type = "Throttle"
        return
    
    def fixStates(self):
        #Assumes constant pressure
        super(Throttle, self).fixStates()
        if self.n1.h is not None and self.n2.h is None:
            self.n2.h = self.n1.h
        elif self.n1.h is None and self.n2.h is not None:
            self.n1.h = self.n2.h
        super(Throttle, self).fixStates()
        return
    
    #Both are 0 for a throttle
    def getData(self):
        #Technically, since we already know Q and W are 0 we could determine them without fixing the two states
        #However, this would cause problems with cycles.py since the device would be fixed but the states wouldn't
        #assume no work being done and adiabatic.  So i've made it a requirement
        if self.n1.isFixed() and self.n2.isFixed() : 
            self.W = 0
            self.Q = 0            
        return
