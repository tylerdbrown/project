import SetStates as SS

FSAT = open("h20sat", 'r')
FSUP = open("h20sup", 'r')
FCOM = open("h20com", 'r')
TABLE = SS.Table('W', FSAT, FSUP, FCOM)
state = SS.State('W', P=8, h=1316.6)
state2 = SS.State('W', P=.008)

#A device can be a Nozzle, Turbine, Boiler, etc.  It consists of left and right nodes (n1, n2) of states for the inlet/outlet.  Additionally, there is a mass
#flow rate, m.  Q and W are what we want to know, which depends on the type of device (turbines, for example - assume no heat loss so Q=0 and W is just
#Q - W = m(del(h)))
class Device(object):
    def __init__(self, n1, n2, m):
        self.n1, self.n2, self.m = n1, n2, m
        self.type = "undefined"
        self.Q = None
        self.W = None
    
    def __str__(self):
        return "Device " + self.type + " with left node = " + str(self.n1.__str__()) + " \nand right node = " + str(self.n2.__str__()) + " \nwith flow of " + str(self.m)     
        
    def fixStates(self, tbls):
        self.n1.setState(tbls)
        self.n2.setState(tbls)
        
class Turbine(Device):
    #Just to set the type to turbine for the purpose of the print statements
    def __init__(self, n1, n2, m):
        super(Turbine, self).__init__(n1, n2, m)
        self.type = "Turbine"
    def fixStates(self, tbls):
        #Assume isentropic 'perfect' turbine so we can say s is constant from inlet to outlet
        
        #This block first checks if either state is fixed, and fixes if it isn't.  Then it will set s2 = s1 or s1 = s2 if not defined
        #This assumes the user hasn't entered two s's for both nodes that don't make sense.  Then it will attempt to fix the states once again
        super(Turbine, self).fixStates(tbls) 
        if self.n2.s is not None and self.n1.s is None:
            self.n1.s = self.n2.s
        elif self.n1.s is not None and self.n2.s is None:
            self.n2.s = self.n1.s
        super(Turbine, self).fixStates(tbls)
        
    #What we're mostinterested in - this method will give is Q and W 
    def getData(self):
        #assume adiabatic
        self.Q = 0
        if self.n2.h is not None and self.n1.h is not None:
            self.W = -1 * self.m * (self.n2.h - self.n1.h)
        else:
            print "Cannot find work without fixed states!"
            return
            
class Compressor(Device):
    #Just to set the type to compressor for the purpose of the print statements
    def __init__(self, n1, n2, m):
        super(Compressor, self).__init__(n1, n2, m)
        self.type = "Compressor"
    def fixStates(self, tbls):
        #Assume isentropic 'perfect' compressor so we can say s is constant from inlet to outlet
        
        #This block first checks if either state is fixed, and fixes if it isn't.  Then it will set s2 = s1 or s1 = s2 if not defined
        #This assumes the user hasn't entered two s's for both nodes that don't make sense.  Then it will attempt to fix the states once again
        super(Compressor, self).fixStates(tbls) 
        if self.n2.s is not None and self.n1.s is None:
            self.n1.s = self.n2.s
        elif self.n1.s is not None and self.n2.s is None:
            self.n2.s = self.n1.s
        super(Compressor, self).fixStates(tbls)
        
    #What we're mostinterested in - this method will give is Q and W 
    def getData(self):
        #assume adiabatic
        self.Q = 0
        if self.n2.h is not None and self.n1.h is not None:
            self.W = -1 * self.m * (self.n2.h - self.n1.h)
        else:
            print "Cannot find work without fixed states!"
            return
            
#Boilers and condensors not implemented yet.  Currently fixing states doesn't fix pressure - need to fix
            
FSAT = open("h20sat", 'r')
FSUP = open("h20sup", 'r')
FCOM = open("h20com", 'r')
table = SS.Table('W', FSAT, FSUP, FCOM)
state = SS.State('W', T = 345)
state2 = SS.State('W', P=3.45, T = 295)
t = Turbine(state, state2, 5.4)