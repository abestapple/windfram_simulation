import numpy as np
class Qian_Ishihara_turbulent_model():
    def __init__(self,u,D,ct,ti,yaw,deflectionmodel,k=0.075):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.yaw=yaw
        self.yaw_rad=self.yaw*np.pi/180
        self.I=np.maximum(0.01,ti)
        self.deflectionmodel=deflectionmodel(self.u,self.D,self.ct,self.I,self.yaw)
        self.constan_()
    def cosd(self,deg):
        return np.cos(deg*np.pi/180)
    def sind(self,deg):
        return np.sin(deg*np.pi/180)
    def constan_(self):
        self.ct_=self.ct*self.cosd(self.yaw)**3
        self.k_star=0.11*self.ct_**1.07*self.I**0.2
        self.epsilonstar=0.23*self.ct_**(-0.25)*self.I**0.17
        #self.theta=0.3*self.alpha/self.cosalpha*(1-np.sqrt(1-self.ct*self.cosalpha))
        #self.x0=self.D*self.cosalpha*(1+np.sqrt(1-self.ct))/(np.sqrt(2)*(2.32*I+0.154*(1-np.sqrt(1-self.ct))))

        self.d=2.3*self.ct_**(-1.2)
        self.e=1.0*self.I**(0.1)
        self.f=0.7*self.ct_**(-3.2)*self.I**(-0.45)

    def ti_deficit_(self,x,r):

        yd=self.deflectionmodel.Deflection(x,r)
        #print(yd)
        simga=self.k_star*x+self.epsilonstar*self.D
        #print(simga,yd)
        r=np.sqrt((r-yd)**2+(100-100)**2)
        part1=1/(self.d+self.e*x/self.D+self.f*(1+x/self.D)**(-2))
        k11=(np.cos(np.pi/2*(r/self.D-0.5)))**2*np.array(r/self.D <= 0.5)
        k12=1*np.array(r/self.D > 0.5)
        k1=k11+k12
        k21=(np.cos(np.pi/2*(r/self.D+0.5)))**2*np.array(r/self.D <= 0.5)
        k22=0*np.array(r/self.D > 0.5)
        k2=k21+k22  
        part2=k1*np.exp(-(r-self.D/2)**2/2/simga/simga)
        part3=k2*np.exp(-(r+self.D/2)**2/2/simga/simga)
        #print(part2)
        wake=part1*(part2+part3)
        return wake
    def wake_expansion(self,x):
        simga=self.k_star*x+self.epsilonstar*self.D
        return 4*np.sqrt(2*np.log(2))*simga