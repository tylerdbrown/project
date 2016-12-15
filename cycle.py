import Devices as dev
import SetStatesIAPWS as ss

class Cycle(object) :
    def __init__(self, nodes):
        self.nodes = nodes
        self.Qnet = None
        self.Wnet = None
        self.eff = None
        return
        
    def __str__(self):
        c=0
        string = "Cycle with nodoes:\n"
        while (c < len(self.nodes)):
            string = string + "\n" + self.nodes[c].__str__() + "\n"
            c+=1
        return string
    def isFixed(self):
        c=0
        while (c < len(self.nodes)):
            if (self.nodes[c].isFixed() is False):
                return False
            c+=1
        return True
            

    #Solves all the devices in the arrays of nodes.
    #goes through the loop twice because that is the maximum number of times
    #it would need to go through the loop to fully solve            
    def solve(self):
        c=0
        while (c < len(self.nodes)):
            self.nodes[c].fixStates()
            self.nodes[c].getData()
            c+=1
        c=0
        while (c < len(self.nodes)):
            self.nodes[c].fixStates()
            self.nodes[c].getData()
            c+=1
        #If this cycle is fixed, we can solve for Qnet, Wnet, and eff
        if (self.isFixed() is True):
            self.Qnet, self.Wnet = 0, 0
            c=0
            while (c < len(self.nodes)):
                self.Qnet = self.Qnet + self.nodes[c].Q
                self.Wnet = self.Wnet + self.nodes[c].W
                c+=1
            self.eff = -1 * self.Wnet / self.Qnet
            print "\nSuccessfully solved.\n" + "Qnet = " + str(self.Qnet) + "\nWnet = " + str(self.Wnet) + "\nEfficiency = " + str(self.eff) + "\n"
            return True
        return False

s1 = ss.State(P=6, T=(500+273))
s2 = ss.State(P=0.01)
s3 = ss.State(X=0.001)
s4 = ss.State(P=7.5)
s5 = ss.State(P=7, T=(40+273))
s6 = ss.State(P=6, T=(550+273))

boiler = dev.QType(s5, s6, 12)
condenser = dev.QType(s2, s3, 12)
turbine = dev.WType(s1, s2, 12)
pump = dev.WType(s3, s4, 12)

cycle = Cycle([turbine, condenser, pump, boiler]) 

cycle.solve()

 