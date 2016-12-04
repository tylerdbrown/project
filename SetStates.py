import numpy as np


#state is defined as a moment in the cycle.  Two properties are required to fix the state
class State(object):
    def __init__(self, M, T=None, P=None, v=None, u=None, h=None, s=None, X=None):
        self.M, self.T, self.P, self.v, self.u, self.h, self.s, self.X = M, T, P, v, u, h, s, X
        
    def __str__(self):
        return ("State of " + self.M + "\nT = " + str(self.T) + "\nP = " + str(self.P) + "\nv = " + str(self.v) + "\nu = " + str(self.u) + "\nh = " + str(self.h) + "\ns = " + str(self.s) + "\nX = " + str(self.X))
        
        
#Bool defines if this state is currentely fixed or not
    def fixed(self):
        c = 0
        if self.T is not None:
            c+=1
        if self.P is not None:
            c+=1
        if self.v is not None:
            c+=1
        if self.u is not None:
            c+=1
        if self.h is not None:
            c+=1
        if self.s is not None:
            c+=1
        if self.X is not None:
            c+=1
        if c >= 2:
            return True
        else:
            return False
            
#void function sets the state, True is a successful operation, False is a failed operation
    def setState(self, tbls=None):
        if self.fixed() == True:
            #Reserve symbol "I" for ideal gas - different function than tabulated properties
            if self.M == 'I':
                self.setStateIGL()
                return True
            else:
                if tbls is not None:
                    self.setStateTab(tbls)
                    return True
        return False
        
    def setStateIGL(self):
        return None

    def setStateTabSolverCom(self, tbls, c3, c4, x):
        if self.T is not None:
            while (tbls.com_T[c3] < self.T):
                c3+=1
            while (tbls.com_T[c4] < self.T):
                c4+=1
            if self.h is None:
                tblvala = (self.T - tbls.com_T[c3-1]) / (tbls.com_T[c3] - tbls.com_T[c3-1]) * (tbls.com_h[c3] - tbls.com_h[c3-1]) + tbls.com_h[c3-1]
                tblvalb = (self.T - tbls.com_T[c4-1]) / (tbls.com_T[c4] - tbls.com_T[c4-1]) * (tbls.com_h[c4] - tbls.com_h[c4-1]) + tbls.com_h[c4-1]
                self.h = x * (tblvala - tblvalb) + (tblvalb)
            if self.s is None:
                tblvala = (self.T - tbls.com_T[c3-1]) / (tbls.com_T[c3] - tbls.com_T[c3-1]) * (tbls.com_s[c3] - tbls.com_s[c3-1]) + tbls.com_s[c3-1]
                tblvalb = (self.T - tbls.com_T[c4-1]) / (tbls.com_T[c4] - tbls.com_T[c4-1]) * (tbls.com_s[c4] - tbls.com_s[c4-1]) + tbls.com_s[c4-1]
                self.s = x * (tblvala - tblvalb) + (tblvalb)
            if self.u is None:
                tblvala = (self.T - tbls.com_T[c3-1]) / (tbls.com_T[c3] - tbls.com_T[c3-1]) * (tbls.com_u[c3] - tbls.com_u[c3-1]) + tbls.com_u[c3-1]
                tblvalb = (self.T - tbls.com_T[c4-1]) / (tbls.com_T[c4] - tbls.com_T[c4-1]) * (tbls.com_u[c4] - tbls.com_u[c4-1]) + tbls.com_u[c4-1]
                self.u = x * (tblvala - tblvalb) + (tblvalb)
            if self.v is None:
                tblvala = (self.T - tbls.com_T[c3-1]) / (tbls.com_T[c3] - tbls.com_T[c3-1]) * (tbls.com_v[c3] - tbls.com_v[c3-1]) + tbls.com_v[c3-1]
                tblvalb = (self.T - tbls.com_T[c4-1]) / (tbls.com_T[c4] - tbls.com_T[c4-1]) * (tbls.com_v[c4] - tbls.com_v[c4-1]) + tbls.com_v[c4-1]
                self.v = x * (tblvala - tblvalb) + (tblvalb)
        if self.v is not None:
            while (tbls.com_v[c3] < self.v):
                c3+=1
            while (tbls.com_v[c4] < self.v):
                c4+=1
            if self.h is None:
                tblvala = (self.v - tbls.com_v[c3-1]) / (tbls.com_v[c3] - tbls.com_v[c3-1]) * (tbls.com_h[c3] - tbls.com_h[c3-1]) + tbls.com_h[c3-1]
                tblvalb = (self.v - tbls.com_v[c4-1]) / (tbls.com_v[c4] - tbls.com_v[c4-1]) * (tbls.com_h[c4] - tbls.com_h[c4-1]) + tbls.com_h[c4-1]
                self.h = x * (tblvala - tblvalb) + (tblvalb)
            if self.s is None:
                tblvala = (self.v - tbls.com_v[c3-1]) / (tbls.com_v[c3] - tbls.com_v[c3-1]) * (tbls.com_s[c3] - tbls.com_s[c3-1]) + tbls.com_s[c3-1]
                tblvalb = (self.v - tbls.com_v[c4-1]) / (tbls.com_v[c4] - tbls.com_v[c4-1]) * (tbls.com_s[c4] - tbls.com_s[c4-1]) + tbls.com_s[c4-1]
                self.s = x * (tblvala - tblvalb) + (tblvalb)
            if self.u is None:
                tblvala = (self.v - tbls.com_v[c3-1]) / (tbls.com_v[c3] - tbls.com_v[c3-1]) * (tbls.com_u[c3] - tbls.com_u[c3-1]) + tbls.com_u[c3-1]
                tblvalb = (self.v - tbls.com_v[c4-1]) / (tbls.com_v[c4] - tbls.com_v[c4-1]) * (tbls.com_u[c4] - tbls.com_u[c4-1]) + tbls.com_u[c4-1]
                self.u = x * (tblvala - tblvalb) + (tblvalb)
            if self.T is None:
                tblvala = (self.v - tbls.com_v[c3-1]) / (tbls.com_v[c3] - tbls.com_v[c3-1]) * (tbls.com_T[c3] - tbls.com_T[c3-1]) + tbls.com_T[c3-1]
                tblvalb = (self.v - tbls.com_v[c4-1]) / (tbls.com_v[c4] - tbls.com_v[c4-1]) * (tbls.com_T[c4] - tbls.com_T[c4-1]) + tbls.com_T[c4-1]
                self.T = x * (tblvala - tblvalb) + (tblvalb)
        if self.u is not None:
            while (tbls.com_u[c3] < self.u):
                c3+=1
            while (tbls.com_u[c4] < self.u):
                c4+=1
            if self.h is None:
                tblvala = (self.u - tbls.com_u[c3-1]) / (tbls.com_u[c3] - tbls.com_u[c3-1]) * (tbls.com_h[c3] - tbls.com_h[c3-1]) + tbls.com_h[c3-1]
                tblvalb = (self.u - tbls.com_u[c4-1]) / (tbls.com_u[c4] - tbls.com_u[c4-1]) * (tbls.com_h[c4] - tbls.com_h[c4-1]) + tbls.com_h[c4-1]
                self.h = x * (tblvala - tblvalb) + (tblvalb)
            if self.s is None:
                tblvala = (self.u - tbls.com_u[c3-1]) / (tbls.com_u[c3] - tbls.com_u[c3-1]) * (tbls.com_s[c3] - tbls.com_s[c3-1]) + tbls.com_s[c3-1]
                tblvalb = (self.u - tbls.com_u[c4-1]) / (tbls.com_u[c4] - tbls.com_u[c4-1]) * (tbls.com_s[c4] - tbls.com_s[c4-1]) + tbls.com_s[c4-1]
                self.s = x * (tblvala - tblvalb) + (tblvalb)
            if self.v is None:
                tblvala = (self.u - tbls.com_u[c3-1]) / (tbls.com_u[c3] - tbls.com_u[c3-1]) * (tbls.com_v[c3] - tbls.com_v[c3-1]) + tbls.com_v[c3-1]
                tblvalb = (self.u - tbls.com_u[c4-1]) / (tbls.com_u[c4] - tbls.com_u[c4-1]) * (tbls.com_v[c4] - tbls.com_v[c4-1]) + tbls.com_v[c4-1]
                self.v = x * (tblvala - tblvalb) + (tblvalb)
            if self.T is None:
                tblvala = (self.u - tbls.com_u[c3-1]) / (tbls.com_u[c3] - tbls.com_u[c3-1]) * (tbls.com_T[c3] - tbls.com_T[c3-1]) + tbls.com_T[c3-1]
                tblvalb = (self.u - tbls.com_u[c4-1]) / (tbls.com_u[c4] - tbls.com_u[c4-1]) * (tbls.com_T[c4] - tbls.com_T[c4-1]) + tbls.com_T[c4-1]
                self.T = x * (tblvala - tblvalb) + (tblvalb)
        if self.h is not None:
            while (tbls.com_h[c3] < self.h):
                c3+=1
            while (tbls.com_h[c4] < self.h):
                c4+=1
            if self.u is None:
                tblvala = (self.h - tbls.com_h[c3-1]) / (tbls.com_h[c3] - tbls.com_h[c3-1]) * (tbls.com_u[c3] - tbls.com_u[c3-1]) + tbls.com_u[c3-1]
                tblvalb = (self.h - tbls.com_h[c4-1]) / (tbls.com_h[c4] - tbls.com_h[c4-1]) * (tbls.com_u[c4] - tbls.com_u[c4-1]) + tbls.com_u[c4-1]
                self.u = x * (tblvala - tblvalb) + (tblvalb)
            if self.s is None:
                tblvala = (self.h - tbls.com_h[c3-1]) / (tbls.com_h[c3] - tbls.com_h[c3-1]) * (tbls.com_s[c3] - tbls.com_s[c3-1]) + tbls.com_s[c3-1]
                tblvalb = (self.h - tbls.com_h[c4-1]) / (tbls.com_h[c4] - tbls.com_h[c4-1]) * (tbls.com_s[c4] - tbls.com_s[c4-1]) + tbls.com_s[c4-1]
                self.s = x * (tblvala - tblvalb) + (tblvalb)
            if self.v is None:
                tblvala = (self.h - tbls.com_h[c3-1]) / (tbls.com_h[c3] - tbls.com_h[c3-1]) * (tbls.com_v[c3] - tbls.com_v[c3-1]) + tbls.com_v[c3-1]
                tblvalb = (self.h - tbls.com_h[c4-1]) / (tbls.com_h[c4] - tbls.com_h[c4-1]) * (tbls.com_v[c4] - tbls.com_v[c4-1]) + tbls.com_v[c4-1]
                self.v = x * (tblvala - tblvalb) + (tblvalb)
            if self.T is None:
                tblvala = (self.h - tbls.com_h[c3-1]) / (tbls.com_h[c3] - tbls.com_h[c3-1]) * (tbls.com_T[c3] - tbls.com_T[c3-1]) + tbls.com_T[c3-1]
                tblvalb = (self.h - tbls.com_h[c4-1]) / (tbls.com_h[c4] - tbls.com_h[c4-1]) * (tbls.com_T[c4] - tbls.com_T[c4-1]) + tbls.com_T[c4-1]
                self.T = x * (tblvala - tblvalb) + (tblvalb)
        if self.s is not None:
            while (tbls.com_s[c3] < self.s):
                c3+=1
            while (tbls.com_s[c4] < self.s):
                c4+=1
            if self.h is None:
                tblvala = (self.s - tbls.com_s[c3-1]) / (tbls.com_s[c3] - tbls.com_s[c3-1]) * (tbls.com_h[c3] - tbls.com_h[c3-1]) + tbls.com_h[c3-1]
                tblvalb = (self.s - tbls.com_s[c4-1]) / (tbls.com_s[c4] - tbls.com_s[c4-1]) * (tbls.com_h[c4] - tbls.com_h[c4-1]) + tbls.com_h[c4-1]
                self.h = x * (tblvala - tblvalb) + (tblvalb)
            if self.u is None:
                tblvala = (self.s - tbls.com_s[c3-1]) / (tbls.com_s[c3] - tbls.com_s[c3-1]) * (tbls.com_u[c3] - tbls.com_u[c3-1]) + tbls.com_u[c3-1]
                tblvalb = (self.s - tbls.com_s[c4-1]) / (tbls.com_s[c4] - tbls.com_s[c4-1]) * (tbls.com_u[c4] - tbls.com_u[c4-1]) + tbls.com_u[c4-1]
                self.u = x * (tblvala - tblvalb) + (tblvalb)
            if self.v is None:
                tblvala = (self.s - tbls.com_s[c3-1]) / (tbls.com_s[c3] - tbls.com_s[c3-1]) * (tbls.com_v[c3] - tbls.com_v[c3-1]) + tbls.com_v[c3-1]
                tblvalb = (self.s - tbls.com_s[c4-1]) / (tbls.com_s[c4] - tbls.com_s[c4-1]) * (tbls.com_v[c4] - tbls.com_v[c4-1]) + tbls.com_v[c4-1]
                self.v = x * (tblvala - tblvalb) + (tblvalb)
            if self.T is None:
                tblvala = (self.s - tbls.com_s[c3-1]) / (tbls.com_s[c3] - tbls.com_s[c3-1]) * (tbls.com_T[c3] - tbls.com_T[c3-1]) + tbls.com_T[c3-1]
                tblvalb = (self.s - tbls.com_s[c4-1]) / (tbls.com_s[c4] - tbls.com_s[c4-1]) * (tbls.com_T[c4] - tbls.com_T[c4-1]) + tbls.com_T[c4-1]
                self.T = x * (tblvala - tblvalb) + (tblvalb)        
        return
                
    def setStateTabSolverSup(self, tbls, c3, c4, x) :
        if self.T is not None:
            while (tbls.sup_T[c3] < self.T):
                c3+=1
            while (tbls.sup_T[c4] < self.T):
                c4+=1
            if self.h is None:
                tblvala = (self.T - tbls.sup_T[c3-1]) / (tbls.sup_T[c3] - tbls.sup_T[c3-1]) * (tbls.sup_h[c3] - tbls.sup_h[c3-1]) + tbls.sup_h[c3-1]
                tblvalb = (self.T - tbls.sup_T[c4-1]) / (tbls.sup_T[c4] - tbls.sup_T[c4-1]) * (tbls.sup_h[c4] - tbls.sup_h[c4-1]) + tbls.sup_h[c4-1]
                self.h = x * (tblvala - tblvalb) + (tblvalb)
            if self.s is None:
                tblvala = (self.T - tbls.sup_T[c3-1]) / (tbls.sup_T[c3] - tbls.sup_T[c3-1]) * (tbls.sup_s[c3] - tbls.sup_s[c3-1]) + tbls.sup_s[c3-1]
                tblvalb = (self.T - tbls.sup_T[c4-1]) / (tbls.sup_T[c4] - tbls.sup_T[c4-1]) * (tbls.sup_s[c4] - tbls.sup_s[c4-1]) + tbls.sup_s[c4-1]
                self.s = x * (tblvala - tblvalb) + (tblvalb)
            if self.u is None:
                tblvala = (self.T - tbls.sup_T[c3-1]) / (tbls.sup_T[c3] - tbls.sup_T[c3-1]) * (tbls.sup_u[c3] - tbls.sup_u[c3-1]) + tbls.sup_u[c3-1]
                tblvalb = (self.T - tbls.sup_T[c4-1]) / (tbls.sup_T[c4] - tbls.sup_T[c4-1]) * (tbls.sup_u[c4] - tbls.sup_u[c4-1]) + tbls.sup_u[c4-1]
                self.u = x * (tblvala - tblvalb) + (tblvalb)
            if self.v is None:
                tblvala = (self.T - tbls.sup_T[c3-1]) / (tbls.sup_T[c3] - tbls.sup_T[c3-1]) * (tbls.sup_v[c3] - tbls.sup_v[c3-1]) + tbls.sup_v[c3-1]
                tblvalb = (self.T - tbls.sup_T[c4-1]) / (tbls.sup_T[c4] - tbls.sup_T[c4-1]) * (tbls.sup_v[c4] - tbls.sup_v[c4-1]) + tbls.sup_v[c4-1]
                self.v = x * (tblvala - tblvalb) + (tblvalb)
        if self.v is not None:
            while (tbls.sup_v[c3] < self.v):
                c3+=1
            while (tbls.sup_v[c4] < self.v):
                c4+=1
            if self.h is None:
                tblvala = (self.v - tbls.sup_v[c3-1]) / (tbls.sup_v[c3] - tbls.sup_v[c3-1]) * (tbls.sup_h[c3] - tbls.sup_h[c3-1]) + tbls.sup_h[c3-1]
                tblvalb = (self.v - tbls.sup_v[c4-1]) / (tbls.sup_v[c4] - tbls.sup_v[c4-1]) * (tbls.sup_h[c4] - tbls.sup_h[c4-1]) + tbls.sup_h[c4-1]
                self.h = x * (tblvala - tblvalb) + (tblvalb)
            if self.s is None:
                tblvala = (self.v - tbls.sup_v[c3-1]) / (tbls.sup_v[c3] - tbls.sup_v[c3-1]) * (tbls.sup_s[c3] - tbls.sup_s[c3-1]) + tbls.sup_s[c3-1]
                tblvalb = (self.v - tbls.sup_v[c4-1]) / (tbls.sup_v[c4] - tbls.sup_v[c4-1]) * (tbls.sup_s[c4] - tbls.sup_s[c4-1]) + tbls.sup_s[c4-1]
                self.s = x * (tblvala - tblvalb) + (tblvalb)
            if self.u is None:
                tblvala = (self.v - tbls.sup_v[c3-1]) / (tbls.sup_v[c3] - tbls.sup_v[c3-1]) * (tbls.sup_u[c3] - tbls.sup_u[c3-1]) + tbls.sup_u[c3-1]
                tblvalb = (self.v - tbls.sup_v[c4-1]) / (tbls.sup_v[c4] - tbls.sup_v[c4-1]) * (tbls.sup_u[c4] - tbls.sup_u[c4-1]) + tbls.sup_u[c4-1]
                self.u = x * (tblvala - tblvalb) + (tblvalb)
            if self.T is None:
                tblvala = (self.v - tbls.sup_v[c3-1]) / (tbls.sup_v[c3] - tbls.sup_v[c3-1]) * (tbls.sup_T[c3] - tbls.sup_T[c3-1]) + tbls.sup_T[c3-1]
                tblvalb = (self.v - tbls.sup_v[c4-1]) / (tbls.sup_v[c4] - tbls.sup_v[c4-1]) * (tbls.sup_T[c4] - tbls.sup_T[c4-1]) + tbls.sup_T[c4-1]
                self.T = x * (tblvala - tblvalb) + (tblvalb)
        if self.u is not None:
            while (tbls.sup_u[c3] < self.u):
                c3+=1
            while (tbls.sup_u[c4] < self.u):
                c4+=1
            if self.h is None:
                tblvala = (self.u - tbls.sup_u[c3-1]) / (tbls.sup_u[c3] - tbls.sup_u[c3-1]) * (tbls.sup_h[c3] - tbls.sup_h[c3-1]) + tbls.sup_h[c3-1]
                tblvalb = (self.u - tbls.sup_u[c4-1]) / (tbls.sup_u[c4] - tbls.sup_u[c4-1]) * (tbls.sup_h[c4] - tbls.sup_h[c4-1]) + tbls.sup_h[c4-1]
                self.h = x * (tblvala - tblvalb) + (tblvalb)
            if self.s is None:
                tblvala = (self.u - tbls.sup_u[c3-1]) / (tbls.sup_u[c3] - tbls.sup_u[c3-1]) * (tbls.sup_s[c3] - tbls.sup_s[c3-1]) + tbls.sup_s[c3-1]
                tblvalb = (self.u - tbls.sup_u[c4-1]) / (tbls.sup_u[c4] - tbls.sup_u[c4-1]) * (tbls.sup_s[c4] - tbls.sup_s[c4-1]) + tbls.sup_s[c4-1]
                self.s = x * (tblvala - tblvalb) + (tblvalb)
            if self.v is None:
                tblvala = (self.u - tbls.sup_u[c3-1]) / (tbls.sup_u[c3] - tbls.sup_u[c3-1]) * (tbls.sup_v[c3] - tbls.sup_v[c3-1]) + tbls.sup_v[c3-1]
                tblvalb = (self.u - tbls.sup_u[c4-1]) / (tbls.sup_u[c4] - tbls.sup_u[c4-1]) * (tbls.sup_v[c4] - tbls.sup_v[c4-1]) + tbls.sup_v[c4-1]
                self.v = x * (tblvala - tblvalb) + (tblvalb)
            if self.T is None:
                tblvala = (self.u - tbls.sup_u[c3-1]) / (tbls.sup_u[c3] - tbls.sup_u[c3-1]) * (tbls.sup_T[c3] - tbls.sup_T[c3-1]) + tbls.sup_T[c3-1]
                tblvalb = (self.u - tbls.sup_u[c4-1]) / (tbls.sup_u[c4] - tbls.sup_u[c4-1]) * (tbls.sup_T[c4] - tbls.sup_T[c4-1]) + tbls.sup_T[c4-1]
                self.T = x * (tblvala - tblvalb) + (tblvalb)
        if self.h is not None:
            while (tbls.sup_h[c3] < self.h):
                c3+=1
            while (tbls.sup_h[c4] < self.h):
                c4+=1
            if self.u is None:
                tblvala = (self.h - tbls.sup_h[c3-1]) / (tbls.sup_h[c3] - tbls.sup_h[c3-1]) * (tbls.sup_u[c3] - tbls.sup_u[c3-1]) + tbls.sup_u[c3-1]
                tblvalb = (self.h - tbls.sup_h[c4-1]) / (tbls.sup_h[c4] - tbls.sup_h[c4-1]) * (tbls.sup_u[c4] - tbls.sup_u[c4-1]) + tbls.sup_u[c4-1]
                self.u = x * (tblvala - tblvalb) + (tblvalb)
            if self.s is None:
                tblvala = (self.h - tbls.sup_h[c3-1]) / (tbls.sup_h[c3] - tbls.sup_h[c3-1]) * (tbls.sup_s[c3] - tbls.sup_s[c3-1]) + tbls.sup_s[c3-1]
                tblvalb = (self.h - tbls.sup_h[c4-1]) / (tbls.sup_h[c4] - tbls.sup_h[c4-1]) * (tbls.sup_s[c4] - tbls.sup_s[c4-1]) + tbls.sup_s[c4-1]
                self.s = x * (tblvala - tblvalb) + (tblvalb)
            if self.v is None:
                tblvala = (self.h - tbls.sup_h[c3-1]) / (tbls.sup_h[c3] - tbls.sup_h[c3-1]) * (tbls.sup_v[c3] - tbls.sup_v[c3-1]) + tbls.sup_v[c3-1]
                tblvalb = (self.h - tbls.sup_h[c4-1]) / (tbls.sup_h[c4] - tbls.sup_h[c4-1]) * (tbls.sup_v[c4] - tbls.sup_v[c4-1]) + tbls.sup_v[c4-1]
                self.v = x * (tblvala - tblvalb) + (tblvalb)
            if self.T is None:
                tblvala = (self.h - tbls.sup_h[c3-1]) / (tbls.sup_h[c3] - tbls.sup_h[c3-1]) * (tbls.sup_T[c3] - tbls.sup_T[c3-1]) + tbls.sup_T[c3-1]
                tblvalb = (self.h - tbls.sup_h[c4-1]) / (tbls.sup_h[c4] - tbls.sup_h[c4-1]) * (tbls.sup_T[c4] - tbls.sup_T[c4-1]) + tbls.sup_T[c4-1]
                self.T = x * (tblvala - tblvalb) + (tblvalb)
        if self.s is not None:
            while (tbls.sup_s[c3] < self.s):
                c3+=1
            while (tbls.sup_s[c4] < self.s):
                c4+=1
            if self.h is None:
                tblvala = (self.s - tbls.sup_s[c3-1]) / (tbls.sup_s[c3] - tbls.sup_s[c3-1]) * (tbls.sup_h[c3] - tbls.sup_h[c3-1]) + tbls.sup_h[c3-1]
                tblvalb = (self.s - tbls.sup_s[c4-1]) / (tbls.sup_s[c4] - tbls.sup_s[c4-1]) * (tbls.sup_h[c4] - tbls.sup_h[c4-1]) + tbls.sup_h[c4-1]
                self.h = x * (tblvala - tblvalb) + (tblvalb)
            if self.u is None:
                tblvala = (self.s - tbls.sup_s[c3-1]) / (tbls.sup_s[c3] - tbls.sup_s[c3-1]) * (tbls.sup_u[c3] - tbls.sup_u[c3-1]) + tbls.sup_u[c3-1]
                tblvalb = (self.s - tbls.sup_s[c4-1]) / (tbls.sup_s[c4] - tbls.sup_s[c4-1]) * (tbls.sup_u[c4] - tbls.sup_u[c4-1]) + tbls.sup_u[c4-1]
                self.u = x * (tblvala - tblvalb) + (tblvalb)
            if self.v is None:
                tblvala = (self.s - tbls.sup_s[c3-1]) / (tbls.sup_s[c3] - tbls.sup_s[c3-1]) * (tbls.sup_v[c3] - tbls.sup_v[c3-1]) + tbls.sup_v[c3-1]
                tblvalb = (self.s - tbls.sup_s[c4-1]) / (tbls.sup_s[c4] - tbls.sup_s[c4-1]) * (tbls.sup_v[c4] - tbls.sup_v[c4-1]) + tbls.sup_v[c4-1]
                self.v = x * (tblvala - tblvalb) + (tblvalb)
            if self.T is None:
                tblvala = (self.s - tbls.sup_s[c3-1]) / (tbls.sup_s[c3] - tbls.sup_s[c3-1]) * (tbls.sup_T[c3] - tbls.sup_T[c3-1]) + tbls.sup_T[c3-1]
                tblvalb = (self.s - tbls.sup_s[c4-1]) / (tbls.sup_s[c4] - tbls.sup_s[c4-1]) * (tbls.sup_T[c4] - tbls.sup_T[c4-1]) + tbls.sup_T[c4-1]
                self.T = x * (tblvala - tblvalb) + (tblvalb)        
                        
    def setStateTab(self, tbls):
#first determine quality - assumes you know either pressure or temperature (would be silly to have enthalpy and entropy and internal energy is not used)
        if (self.X is None):
            c=0
            if (self.T is not None) and (self.P is not None):
                while (tbls.sat_T[c] < self.T):
                    c+=1
                tblvalP = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_P[c] - tbls.sat_P[c-1]) + tbls.sat_P[c-1]
                if self.P < tblvalP:
                    self.X = 1
                elif self.P > tblvalP:
                    self.X = 0
                else:
                    self.X = None
                    print "This state is in the rare case and is not actually fixed"
                    return
            else:
                if self.T is not None:
                    while (tbls.sat_T[c] < self.T):
                        c+=1
                    if self.h is not None:
                        tblvalf = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_hf[c] - tbls.sat_hf[c-1]) + tbls.sat_hf[c-1]
                        tblvalg = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_hg[c] - tbls.sat_hg[c-1]) + tbls.sat_hg[c-1]
                        if self.h < tblvalf:
                            self.X = 0
                        elif self.h > tblvalg:
                            self.X = 1
                        else:
                            self.X = (self.h - tblvalf)/(tblvalg - tblvalf)
                    elif self.s is not None:
                        tblvalf = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_sf[c] - tbls.sat_sf[c-1]) + tbls.sat_sf[c-1]
                        tblvalg = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_sg[c] - tbls.sat_sg[c-1]) + tbls.sat_sg[c-1]
                        if self.s < tblvalf:
                            self.X = 0
                        elif self.s > tblvalg:
                            self.X = 1
                        else:
                            self.X = (self.s - tblvalf)/(tblvalg - tblvalf)
                    else:
                        print "ERORR:  Trying to set state of tabulated property without either enthalpy or entropy"
                elif self.P is not None:
                    while (tbls.sat_P[c] > self.P):
                        c+=1
                    if self.h is not None:
                        tblvalf = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_P[c-1]) * (tbls.sat_hf[c] - tbls.sat_hf[c-1]) + tbls.sat_hf[c-1]
                        tblvalg = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_P[c-1]) * (tbls.sat_hg[c] - tbls.sat_hg[c-1]) + tbls.sat_hg[c-1]
                        if self.h < tblvalf:
                            self.X = 0
                        elif self.h > tblvalg:
                            self.X = 1
                        else:
                            self.X = (self.h - tblvalf)/(tblvalg - tblvalf)
                    elif self.s is not None:
                        tblvalf = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_T[c-1]) * (tbls.sat_sf[c] - tbls.sat_sf[c-1]) + tbls.sat_sf[c-1]
                        tblvalg = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_T[c-1]) * (tbls.sat_sg[c] - tbls.sat_sg[c-1]) + tbls.sat_sg[c-1]
                        if self.s < tblvalf:
                            self.X = 0
                        elif self.s > tblvalg:
                            self.X = 1
                        else:
                            self.X = (self.s - tblvalf)/(tblvalg - tblvalf)
                    else:
                        print "ERORR:  Trying to set state of tabulated property without either enthalpy or entropy"
                else:
                    print "ERROR:  Trying to set state of tabulated property without temperature or pressure"
    #Quality Determined!
        if self.X == 1: #Superheated
            #c represents the first value of the first table, c2 represents the first value of the second table
            if self.P is not None:
                c2=0 
                while (tbls.sup_P[c2] < self.P):
                    c2+=1
                c=c2-1
                while (tbls.sup_P[c] == tbls.sup_P[c2-1]):
                    c-=1
                c+=1
                x = (self.P-tbls.sup_P[c])/(tbls.sup_P[c2] - tbls.sup_P[c])
                self.setStateTabSolverSup(tbls, c, c2, x)
            elif self.T is not None:
                if self.s is not None:
                    c=0
                    tblvala = 99999999
                    while tblvala - self.s > 0:
                        while tbls.sup_T[c] < self.T:
                            c+=1
                        tblvala = (self.T - tbls.sup_T[c-1]) / (tbls.sup_T[c] - tbls.sup_T[c-1]) * (tbls.sup_s[c] - tbls.sup_s[c-1]) + tbls.sup_s[c-1]
                        if tblvala - self.s >= 0:
                            c2=c
                            while tbls.sup_P[c] == tbls.sup_P[c2]:
                                c+=1
                    c2=c
                    while (tbls.sup_P[c2] == tbls.sup_P[c]):
                        c2-=1
                    while (tbls.sup_T[c2-1] > self.T):
                        c2-=1
                    #c2 -> c [oops]
                    #c -> c2
                    tblvalb = (self.T - tbls.sup_T[c2-1]) / (tbls.sup_T[c2] - tbls.sup_T[c2-1]) * (tbls.sup_s[c2] - tbls.sup_s[c2-1]) + tbls.sup_s[c2-1]
                    x = (self.s - tblvala)/(tblvalb - tblvala)
                elif self.h is not None:
                    c=0
                    tblvala = 99999999
                    while tblvala - self.h > 0:
                        while tbls.sup_T[c] < self.T:
                            c+=1
                        tblvala = (self.T - tbls.sup_T[c-1]) / (tbls.sup_T[c] - tbls.sup_T[c-1]) * (tbls.sup_h[c] - tbls.sup_h[c-1]) + tbls.sup_h[c-1]
                        if tblvala - self.h >= 0:
                            c2=c
                            while tbls.sup_P[c] == tbls.sup_P[c2]:
                                c+=1
                    c2=c
                    while (tbls.sup_P[c2] == tbls.sup_P[c]):
                        c2-=1
                    while (tbls.sup_T[c2-1] > self.T):
                        c2-=1
                    #c2 -> c [oops]
                    #c -> c2
                    tblvalb = (self.T - tbls.sup_T[c2-1]) / (tbls.sup_T[c2] - tbls.sup_T[c2-1]) * (tbls.sup_h[c2] - tbls.sup_h[c2-1]) + tbls.sup_h[c2-1]
                    x = (self.h - tblvala)/(tblvalb - tblvala)                    
                elif self.v is  not None:
                    c=0
                    tblvala = 99999999
                    while tblvala - self.v > 0:
                        while tbls.sup_T[c] < self.T:
                            c+=1
                        tblvala = (self.T - tbls.sup_T[c-1]) / (tbls.sup_T[c] - tbls.sup_T[c-1]) * (tbls.sup_v[c] - tbls.sup_v[c-1]) + tbls.sup_v[c-1]
                        if tblvala - self.v >= 0:
                            c2=c
                            while tbls.sup_P[c] == tbls.sup_P[c2]:
                                c+=1
                    c2=c
                    while (tbls.sup_P[c2] == tbls.sup_P[c]):
                        c2-=1
                    while (tbls.sup_T[c2-1] > self.T):
                        c2-=1
                    #c2 -> c [oops]
                    #c -> c2
                    tblvalb = (self.T - tbls.sup_T[c2-1]) / (tbls.sup_T[c2] - tbls.sup_T[c2-1]) * (tbls.sup_v[c2] - tbls.sup_v[c2-1]) + tbls.sup_v[c2-1]
                    x = (self.v - tblvala)/(tblvalb - tblvala)
                else:
                    print "ERROR: Tried to fix stating knowing P but not knowing v, s, or h?"
                    return
                self.setStateTabSolverSup(tbls, c2, c, x)
            else:
                print "ERROR: Tried to fix state without knowing T or P"
                return
        elif self.X == 0: #Supercompressed
            #c represents the first value of the first table, c2 represents the first value of the second table
            if self.P is not None:
                c2=0 
                while (tbls.com_P[c2] < self.P):
                    c2+=1
                c=c2-1
                while (tbls.com_P[c] == tbls.com_P[c2-1]):
                    c-=1
                c+=1
                x = (self.P-tbls.com_P[c])/(tbls.com_P[c2] - tbls.com_P[c])
                self.setStateTabSolverCom(tbls, c, c2, x)
            elif self.T is not None:
                if self.s is not None:
                    c=0
                    tblvala = 99999999
                    while tblvala - self.s > 0:
                        while tbls.com_T[c] < self.T:
                            c+=1
                        tblvala = (self.T - tbls.com_T[c-1]) / (tbls.com_T[c] - tbls.com_T[c-1]) * (tbls.com_s[c] - tbls.com_s[c-1]) + tbls.com_s[c-1]
                        if tblvala - self.s >= 0:
                            c2=c
                            while tbls.com_P[c] == tbls.com_P[c2]:
                                c+=1
                    c2=c
                    while (tbls.com_P[c2] == tbls.com_P[c]):
                        c2-=1
                    while (tbls.com_T[c2-1] > self.T):
                        c2-=1
                    #c2 -> c [oops]
                    #c -> c2
                    tblvalb = (self.T - tbls.com_T[c2-1]) / (tbls.com_T[c2] - tbls.com_T[c2-1]) * (tbls.com_s[c2] - tbls.com_s[c2-1]) + tbls.com_s[c2-1]
                    x = (self.s - tblvala)/(tblvalb - tblvala)
                elif self.h is not None:
                    c=0
                    tblvala = 99999999
                    while tblvala - self.h > 0:
                        while tbls.com_T[c] < self.T:
                            c+=1
                        tblvala = (self.T - tbls.com_T[c-1]) / (tbls.com_T[c] - tbls.com_T[c-1]) * (tbls.com_h[c] - tbls.com_h[c-1]) + tbls.com_h[c-1]
                        if tblvala - self.h >= 0:
                            c2=c
                            while tbls.com_P[c] == tbls.com_P[c2]:
                                c+=1
                    c2=c
                    while (tbls.com_P[c2] == tbls.com_P[c]):
                        c2-=1
                    while (tbls.com_T[c2-1] > self.T):
                        c2-=1
                    #c2 -> c [oops]
                    #c -> c2
                    tblvalb = (self.T - tbls.com_T[c2-1]) / (tbls.com_T[c2] - tbls.com_T[c2-1]) * (tbls.com_h[c2] - tbls.com_h[c2-1]) + tbls.com_h[c2-1]
                    x = (self.h - tblvala)/(tblvalb - tblvala)                    
                elif self.v is  not None:
                    c=0
                    tblvala = 99999999
                    while tblvala - self.v > 0:
                        while tbls.com_T[c] < self.T:
                            c+=1
                        tblvala = (self.T - tbls.com_T[c-1]) / (tbls.com_T[c] - tbls.com_T[c-1]) * (tbls.com_v[c] - tbls.com_v[c-1]) + tbls.com_v[c-1]
                        if tblvala - self.v >= 0:
                            c2=c
                            while tbls.com_P[c] == tbls.com_P[c2]:
                                c+=1
                    c2=c
                    while (tbls.com_P[c2] == tbls.com_P[c]):
                        c2-=1
                    while (tbls.com_T[c2-1] > self.T):
                        c2-=1
                    #c2 -> c [oops]
                    #c -> c2
                    tblvalb = (self.T - tbls.com_T[c2-1]) / (tbls.com_T[c2] - tbls.com_T[c2-1]) * (tbls.com_v[c2] - tbls.com_v[c2-1]) + tbls.com_v[c2-1]
                    x = (self.v - tblvala)/(tblvalb - tblvala)
                else:
                    print "ERROR: Tried to fix stating knowing P but not knowing v, s, or h?"
                    return
                self.setStateTabSolverCom(tbls, c2, c, x)
            else:
                print "ERROR: Tried to fix state without knowing T or P"
                return
                
            
        else:   #Saturated
            c=0
            if self.T is not None:
                if c == 0:
                    while (tbls.sat_T[c] < self.T):
                        c+=1
                if self.h is None:
                    tblvalf = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_hf[c] - tbls.sat_hf[c-1]) + tbls.sat_hf[c-1]
                    tblvalg = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_hg[c] - tbls.sat_hg[c-1]) + tbls.sat_hg[c-1]
                    self.h = self.X * (tblvalg - tblvalf) + tblvalf
                if self.s is None:
                    tblvalf = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_sf[c] - tbls.sat_sf[c-1]) + tbls.sat_sf[c-1]
                    tblvalg = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_sg[c] - tbls.sat_sg[c-1]) + tbls.sat_sg[c-1]
                    self.s = self.X * (tblvalg - tblvalf) + tblvalf
                if self.u is None:
                    tblvalf = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_uf[c] - tbls.sat_uf[c-1]) + tbls.sat_uf[c-1]
                    tblvalg = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_ug[c] - tbls.sat_ug[c-1]) + tbls.sat_ug[c-1]     
                    self.u = self.X * (tblvalg - tblvalf) + tblvalf      
                if self.v is None:
                    tblvalf = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_vf[c] - tbls.sat_vf[c-1]) + tbls.sat_vf[c-1]
                    tblvalg = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_vg[c] - tbls.sat_vg[c-1]) + tbls.sat_vg[c-1]     
                    self.v = self.X * (tblvalg - tblvalf) + tblvalf         
                if self.P is None:
                    self.P = (self.T - tbls.sat_T[c-1]) / (tbls.sat_T[c] - tbls.sat_T[c-1]) * (tbls.sat_P[c] - tbls.sat_P[c-1]) + tbls.sat_P[c-1]
            elif self.P is not None:
                if c == 0:
                    while (tbls.sat_P[c] < self.P):
                        c+=1
                if self.h is None:
                    tblvalf = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_P[c-1]) * (tbls.sat_hf[c] - tbls.sat_hf[c-1]) + tbls.sat_hf[c-1]
                    tblvalg = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_P[c-1]) * (tbls.sat_hg[c] - tbls.sat_hg[c-1]) + tbls.sat_hg[c-1]
                    self.h = self.X * (tblvalg - tblvalf) + tblvalf
                if self.s is None:
                    tblvalf = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_P[c-1]) * (tbls.sat_sf[c] - tbls.sat_sf[c-1]) + tbls.sat_sf[c-1]
                    tblvalg = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_P[c-1]) * (tbls.sat_sg[c] - tbls.sat_sg[c-1]) + tbls.sat_sg[c-1]
                    self.s = self.X * (tblvalg - tblvalf) + tblvalf
                if self.u is None:
                    tblvalf = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_P[c-1]) * (tbls.sat_uf[c] - tbls.sat_uf[c-1]) + tbls.sat_uf[c-1]
                    tblvalg = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_P[c-1]) * (tbls.sat_ug[c] - tbls.sat_ug[c-1]) + tbls.sat_ug[c-1]
                    self.u = self.X * (tblvalg - tblvalf) + tblvalf
                if self.T is None:
                    self.T = (self.P - tbls.sat_P[c-1]) / (tbls.sat_P[c] - tbls.sat_P[c-1]) * (tbls.sat_T[c] - tbls.sat_T[c-1]) + tbls.sat_T[c-1]
        return
        

#Table is actually three different tables - saturated, compressed, and superheated tables.  These tables are used to fix states for
#non-ideal gasses.  Additionally, the tables need to follow an exact format such as included example table for steam
#This format includes the numbers being sorted the way they are
class Table(object):
    def __init__(self, M, sat, sup, com):
        self.M = M
        self.sat_T, self.sat_P, self.sat_vf, self.sat_vg, self.sat_uf, self.sat_ug, self.sat_hf, self.sat_hfg, self.sat_hg, self.sat_sf, self.sat_sfg, self.sat_sg = [], [], [], [], [], [], [], [], [], [], [], []
        self.sup_T, self.sup_P, self.sup_v, self.sup_u, self.sup_h, self.sup_s = [],[],[],[],[],[]
        self.com_T, self.com_P, self.com_v, self.com_u, self.com_h, self.com_s = [],[],[],[],[],[]
        for line in sat:
            self.sat_T.append(float(line.split()[0]))
            self.sat_P.append(float(line.split()[1]))
            self.sat_vf.append(float(line.split()[2]))
            self.sat_vg.append(float(line.split()[3]))
            self.sat_uf.append(float(line.split()[4]))
            self.sat_ug.append(float(line.split()[5]))
            self.sat_hf.append(float(line.split()[6]))
            self.sat_hfg.append(float(line.split()[7]))
            self.sat_hg.append(float(line.split()[8]))
            self.sat_sf.append(float(line.split()[9]))
            self.sat_sfg.append(float(line.split()[10]))
            self.sat_sg.append(float(line.split()[11]))
        for line in sup:
            self.sup_P.append(float(line.split()[0]))
            self.sup_T.append(float(line.split()[1]))
            self.sup_v.append(float(line.split()[2]))
            self.sup_u.append(float(line.split()[3]))   
            self.sup_h.append(float(line.split()[4]))
            self.sup_s.append(float(line.split()[5]))
            
        for line in com:
            self.com_P.append(float(line.split()[0]))
            self.com_T.append(float(line.split()[1]))
            self.com_v.append(float(line.split()[2]))
            self.com_u.append(float(line.split()[3]))
            self.com_h.append(float(line.split()[4]))
            self.com_s.append(float(line.split()[5]))
        
        print "All tables loaded, no errors"
            
FSAT = open("h20sat", 'r')
FSUP = open("h20sup", 'r')
FCOM = open("h20com", 'r')
TABLE = Table('W', FSAT, FSUP, FCOM)
state = State('W', P=1.401, s=7.605)