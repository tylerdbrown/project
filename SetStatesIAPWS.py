import numpy as np
from iapws import IAPWS97 as iapws

#state is defined as a moment in the cycle.  This is necessary rather than just using IAPWS because one of
#the states defined in this class can be undefined.  If that is the case, or setState has not been run, iapws is NoneType
class State(object):
    def __init__(self, T=None, P=None, v=None, u=None, h=None, s=None, X=None):
        self.T, self.P, self.v, self.u, self.h, self.s, self.X = T, P, v, u, h, s, X
        self.iapws=None;
        
    def __str__(self):
        return ("State of: " + "\nT = " + str(self.T) + "\nP = " + str(self.P) + "\nv = " + str(self.v) + "\nu = " + str(self.u) + "\nh = " + str(self.h) + "\ns = " + str(self.s) + "\nX = " + str(self.X))
    
    #Transfers data from self's iapws to its variables.  Should only be run
    #if the state was just set (iapws was just declared)
    def update(self):
        if self.iapws is None:
            print "CODER ERROR: This shouldn't happen..."
        else:
            self.T = self.iapws.T
            self.P = self.iapws.P
            self.u = self.iapws.u
            self.X = self.iapws.x
            self.h = self.iapws.h
            self.s = self.iapws.s
            self.v = pow(self.iapws.rho,-1)
        return
        
    def isFixed(self):
        if self.iapws is not None:
            return True
        else:
            return False

    #This function will set the states if it can.  Then it will call update()
    #To transfer data from self's iapws to its variables
    #If state cannot be fixed, we will return false
    def setState(self):
        if (self.T is not None and self.P is not None):
            self.iapws = iapws(T=self.T,P=self.P)
            self.update()
        elif (self.T is not None and self.v is not None):
            self.iapws = iapws(T=self.T,rho=pow(self.v,-1))
            self.update()
        elif (self.T is not None and self.s is not None):
            self.iapws = iapws(T=self.T, s=self.s)
            self.update()
        elif (self.T is not None and self.u is not None):
            self.iapws = iapws(T=self.T, u=self.u)
            self.update()
        elif (self.P is not None and self.v is not None):
            self.iapws = iapws(P=self.P, rho=pow(self.v,-1))
            self.update()
        elif (self.P is not None and self.h is not None):
            self.iapws = iapws(P=self.P, h=self.h)
            self.update()
        elif (self.P is not None and self.s is not None):
            self.iapws = iapws(P=self.P, s=self.s)
            self.update()
        elif (self.P is not None and self.u is not None):
            self.iapws = iapws(P=self.P, u=self.u)
            self.update()
        elif (self.v is not None and self.h is not None):
            self.iapws = iapws(rho=pow(self.v,-1), h=self.h)
            self.update()
        elif (self.v is not None and self.s is not None):
            self.iapws = iapws(rho=pow(self.v,-1), s=self.s)
            self.update()
        elif (self.v is not None and self.u is not None):
            self.iapws = iapws(rho=pow(self.v,-1), u=self.u)
            self.update()
        elif (self.h is not None and self.s is not None):
            self.iapws = iapws(h=self.h, s=self.s)
            self.update()
        elif (self.h is not None and self.u is not None):
            self.iapws = iapws(h=self.h, u=self.u)
            self.update()
        elif (self.s is not None and self.u is not None):
            self.iapws = iapws(s=self.s, u=self.u)
            self.update()
        elif (self.T is not None and self.X is not None):
            self.iapws = iapws(T=self.T, x=self.X)
            self.update()
        elif (self.P is not None and self.X is not None):
            self.iapws = iapws(P=self.P, x=self.X)
            self.update()
        else:
            return False
        return True
        