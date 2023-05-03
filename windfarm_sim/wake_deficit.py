import numpy as np

class guass_Bastankhah():
    def __init__(self,u,D,ct,k=0.07):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
    def Beta(self):
        return 0.5*(1+np.sqrt(1-self.ct))/(np.sqrt(1-self.ct))
    def deficit_(self,x,r):
        """
         A new analytical model for wind-turbine wakes
            
         Majid Bastankhah, Fernando Porté-Agel*
        """
        e=0.25*np.sqrt(self.Beta())
        a=(self.k*x/self.D+e)**2
        wake=-self.u*(1-np.sqrt(1-self.ct/8/a))*np.exp(-1/2/a*(r*r/self.D/self.D))
        return wake
    def wake_expansion(self):
        return self.k,0.2*np.sqrt(self.Beta())*self.D+self.D/2

class guass_Ge():
    def __init__(self,u,D,ct,k=0.075):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
    def deficit_(self,x,r):
        """
            paper: A two-dimensional model based on the expansion of physical wake
            boundary for wind-turbine wakes
        """  
        ro=self.D/2
        a=(self.k*x/ro+1)**2
        b=(1-2*self.ct/a)**0.5
        expin=-2/a*(r/ro)**2
        wake=-self.u*(1-b)*np.exp(expin)
        return wake
    def wake_expansion(self):
        return self.k,self.D/2+self.D/4

class Park():
    def __init__(self,u,D,ct,k=0.075):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
    def deficit_(self,x,r):
        """
        Park_wake_model;
        """
        R=self.D/2
        a=self.k*x+R
        wake=-self.u*(1-np.sqrt(1-self.ct))*(R/(R+self.k*x))**2
        #wake[r>a]=0
        return wake
    def wake_expansion(self):
        return self.k,self.D/2

class Modified_Park():
    def __init__(self,u,D,ct,k=0.075):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
    def deficit_(self,x,r):
        """
        Park_wake_model;
        """
        R=self.D/2
        a=self.k*x+R
        wake=-self.u*(1-np.sqrt(1-self.ct))*(self.D/(self.D+2*self.k*x))**2
        #wake[r>a]=0
        return wake
    def wake_expansion(self):
        return self.k,self.D/2