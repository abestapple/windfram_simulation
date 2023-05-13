import numpy as np

class guass_Bastankhah_yaw():
    def __init__(self,u,D,ct,Ia,yaw,k=0.075):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.yaw=yaw
        self.ka=0.38
        self.kb=0.004
        self.dm=1.0
        self.Ia=Ia
        self.constan_()
    def cosd(self,deg):
        return np.cos(deg*np.pi/180)
    def constan_(self):
        I=self.Ia
        #self.theta=0.3*self.alpha/self.cosalpha*(1-np.sqrt(1-self.ct*self.cosalpha))
        #self.x0=self.D*self.cosalpha*(1+np.sqrt(1-self.ct))/(np.sqrt(2)*(2.32*I+0.154*(1-np.sqrt(1-self.ct))))
        
        self.uR = (
            self.u
          * self.ct
          * self.cosd(self.yaw)
          / (2.0 * (1 - np.sqrt(1 - (self.ct* self.cosd(self.yaw)))))
        )
        self.u0=self.u * np.sqrt(1 - self.ct)
        self.x0 = (
            self.D
            * (self.cosd(self.yaw) * (1 + np.sqrt(1 - self.ct * self.cosd(self.yaw))))
            / (np.sqrt(2) * (
                4 * 0.58 * I + 2 * 0.077 * (1 - np.sqrt(1 - self.ct))
            )) + 0
        )

        self.ky = self.ka * I + self.kb
        self.kz = self.ka * I + self.kb
        C0 = 1 -self.u0 / self.u
        self.M0 = C0 * (2 - C0)
        self.E0 = C0 ** 2 - 3 * np.exp(1.0 / 12.0) * C0 + 3 * np.exp(1.0 / 3.0)
        self.sigma_z0 = self.D * 0.5 * np.sqrt(self.uR / (self.u + self.u0))
        self.sigma_y0 = self.sigma_z0 * self.cosd(self.yaw)*self.cosd(0)
        self.xR = 0
        self.theta_c0 = self.dm * (0.3 * np.radians(self.yaw) / self.cosd(self.yaw))
        self.theta_c0 *= (1 - np.sqrt(1 - self.ct * self.cosd(self.yaw)))
        self.delta0 = np.tan(self.theta_c0) * (self.x0 - 0)  # initial wake deflection;    
        
    def Deflection(self,x,r):
        """
            Controls-Oriented Model for Secondary Effects of Wake Steering
        """
        delta_near_wake = ((x - self.xR) / (self.x0 - self.xR)) * self.delta0 + (0 + 0 * (x - 0))
        delta_near_wake = delta_near_wake * np.array(x >= self.xR)
        delta_near_wake = delta_near_wake * np.array(x <= self.x0)        
        
        sigma_y = self.ky * (x - self.x0) + self.sigma_y0
        sigma_z = self.kz * (x - self.x0) + self.sigma_z0
        self.sigma_y = sigma_y * np.array(x >= self.x0) + self.sigma_y0 * np.array(x < self.x0)
        self.sigma_z = sigma_z * np.array(x >= self.x0) + self.sigma_z0 * np.array(x < self.x0)  
        
        ln_deltaNum = (1.6 + np.sqrt(self.M0)) * (
            1.6 * np.sqrt(self.sigma_y * self.sigma_z / (self.sigma_y0 * self.sigma_z0)) - np.sqrt(self.M0)
        )
        ln_deltaDen = (1.6 - np.sqrt(self.M0)) * (
            1.6 * np.sqrt(self.sigma_y * self.sigma_z / (self.sigma_y0 * self.sigma_z0)) + np.sqrt(self.M0)
        )
        
        delta_far_wake = (
            self.delta0
          + self.theta_c0 * self.E0 / 5.2
          * np.sqrt(self.sigma_y0 * self.sigma_z0 / (self.ky *self.kz * self.M0))
          * np.log(ln_deltaNum / ln_deltaDen)
          + (0 + 0 * (x - 0))
        )
        delta_far_wake = delta_far_wake * np.array(x > self.x0)
        deflection = delta_near_wake + delta_far_wake
        return deflection

class Jimenez():
    def __init__(self,u,D,ct,Ia,yaw,k=0.075):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.yaw=yaw
        self.kd=Ia*0.4
        if Ia==0:
            self.kd=0.05
    def cosd(self,deg):
        return np.cos(deg*np.pi/180)
    def sind(self,deg):
        return np.sin(deg*np.pi/180)

    def Deflection(self,x,r):
        """
            Controls-Oriented Model for Secondary Effects of Wake Steering
        """
        x_i=0 
        xi_init = self.cosd(self.yaw) * self.sind(self.yaw) * self.ct / 2.0
        delta_x = x - x_i
        A = 15 * (2 * self.kd * delta_x / self.D + 1) ** 4.0 + xi_init ** 2.0
        B = (30 * self.kd / self.D)
        B = B * ( 2 * self.kd * delta_x / self.D + 1 ) ** 5.0
        C = xi_init * self.D * (15 + xi_init ** 2.0)
        D = 30 * self.kd
        yYaw_init = (xi_init * A / B) - (C / D)
        deflection = yYaw_init + 0 + 0 * delta_x
        return -deflection

class Qian_Ishihara():
    def __init__(self,u,D,ct,Ia,yaw,k=0.075):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.yaw=yaw
        self.yaw_rad=self.yaw*np.pi/180
        self.Ia=Ia
        if self.yaw==0:
            pass
        else:
            self.constan_()
    def cosd(self,deg):
        return np.cos(deg*np.pi/180)
    def sind(self,deg):
        return np.sin(deg*np.pi/180)
    def constan_(self):
        I=self.Ia
        if I==0:
            I=0.01
        self.ct_=self.ct*self.cosd(self.yaw)**3
        self.k_star=0.11*self.ct_**1.07*I**0.2
        self.epsilonstar=0.23*self.ct_**(-0.25)*I**0.17
        #self.theta=0.3*self.alpha/self.cosalpha*(1-np.sqrt(1-self.ct*self.cosalpha))
        #self.x0=self.D*self.cosalpha*(1+np.sqrt(1-self.ct))/(np.sqrt(2)*(2.32*I+0.154*(1-np.sqrt(1-self.ct))))
        self.theta0 = 0.3*self.yaw_rad/self.cosd(self.yaw)*(1-np.sqrt(1-self.ct_)) 
        self.a=0.93*self.ct_**(-0.75)*I**(0.17)
        self.b=0.42*self.ct_**(0.6)*I**(0.2)
        self.c=0.15*self.ct_**(-0.25)*I**(-0.7)
        self.d=2.3*self.ct_**(-1.2)
        self.e=1.0*I**(0.1)
        self.f=0.7*self.ct_**(-3.2)*I**(-0.45)
        self.simga0=self.D*np.sqrt(self.ct_*(self.sind(self.yaw)/44.4/self.theta0/self.cosd(self.yaw)+0.042))
        self.x0=(self.simga0-self.epsilonstar*self.D)/self.k_star
        #self.k1= 
    def Deflection(self,x,r):
        """
            Controls-Oriented Model for Secondary Effects of Wake Steering
        """  
        if self.yaw==0:
            return 0
        delta_near_wake=self.theta0*x*np.array(x <= self.x0)
        self.simga=self.k_star*x+self.epsilonstar*self.D
        part1=np.sqrt(self.ct_)*self.sind(self.yaw)/18.24/self.k_star/self.cosd(self.yaw)
        part2=(self.simga0/self.D+0.21*np.sqrt(self.ct_))*(self.simga/self.D-0.21*np.sqrt(self.ct_))
        part3=(self.simga0/self.D-0.21*np.sqrt(self.ct_))*(self.simga/self.D+0.21*np.sqrt(self.ct_))
        part4=self.theta0*self.x0/self.D
        delta_far_wake=(part1*np.log(abs(part2/part3))+part4)*self.D*np.array(x > self.x0)
        return delta_near_wake+delta_far_wake