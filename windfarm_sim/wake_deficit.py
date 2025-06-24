import numpy as np

class Bastankhah():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
    def Beta(self):
        return 0.5*(1+np.sqrt(1-self.ct))/(np.sqrt(1-self.ct))
    def deficit_(self,x,r,h):
        """
         A new analytical model for wind-turbine wakes
            
         Majid Bastankhah, Fernando Porté-Agel*
        """
        r=abs(r)
        e=0.25*np.sqrt(self.Beta())
        a=(self.k*x/self.D+e)**2
        wake=-self.u*(1-np.sqrt(1-self.ct/8/a))*np.exp(-1/2/a*(r*r/self.D/self.D))
        return wake
    def wake_expansion(self,x):
        return self.k*x+0.5*np.sqrt(self.Beta())*self.D

class flex_gauss():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
        self.F=0.8
        self.alpha=1.0
        self.c=0.5
        self.S=1.0
    def Beta(self):
        return 0.5*(1+np.sqrt(1-self.ct))/(np.sqrt(1-self.ct))
    def deficit_(self,x,r,h):
        """
         A new model for wind-turbine wakes from Dr.zhiyuan
        """
        r=abs(r)/self.D
        C=self.c*(1-np.sqrt(1-self.ct))
        umin=self.u*(1-C)
        alpha_flex=self.alpha*(1+self.F)
        Dr=x/self.D
        wake=-(self.u-umin)*np.exp(-r**2/(2*(alpha_flex*(1+2*self.k*Dr)/(self.S/18.34))**2))
        return wake
    def wake_expansion(self,x):
        return self.k*x+self.D

class Gauss():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
    def deficit_(self,x,r,h):

        conts=1.02**2
        beta=0.6
        r=abs(r)
        R=self.D/2
        epart1=np.exp(-beta*x/self.D)
        epart2=-2*conts*r**2/((1+2*self.k*x/self.D)**2*self.D**2)
        f=1-(1-np.sqrt(1-self.ct))*(R/(R+self.k*x))**2
        wake=-0.5*self.u*conts*(1-(1-epart1)*f)*np.exp(epart2)

        return wake
    def wake_expansion(self,x):
        return self.k*x+self.D

class guass_XA():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
    def Beta(self):
        return 0.5*(1+np.sqrt(1-self.ct))/(np.sqrt(1-self.ct))
    def deficit_(self,x,r,h):
        """
         A new analytical model for wind-turbine wakes
            
         Majid Bastankhah, Fernando Porté-Agel*
        """
        r=abs(r)
        e=0.25*np.sqrt(self.Beta())
        Dy=0.025*x+e*self.D
        Dz=0.0175*x+e*self.D
        a=1-np.sqrt(1-self.ct/(8*(Dy*Dz/self.D/self.D)))
        wake=-self.u*a*np.exp(-r*r/2/Dy/Dy)
        return wake
    def wake_expansion(self,x):
        return 0.025*x+0.25*np.sqrt(self.Beta())*self.D+self.D/2

class guass_Ge():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
    def deficit_(self,x,r,h):
        """
            paper: A two-dimensional model based on the expansion of physical wake
            boundary for wind-turbine wakes
        """  
        r=abs(r)
        ro=self.D/2
        a=(self.k*x/ro+1)**2
        b=(1-2*self.ct/a)**0.5
        expin=-2/a*(r/ro)**2
        wake=-self.u*(1-b)*np.exp(expin)
        return wake
    def wake_expansion(self,x):
        return self.k*x+self.D/2+self.D/4

class Jensen():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
    def deficit_(self,x,r,h):
        """
        Park_wake_model;
        """
        r=abs(r)
        R=self.D/2
        a=self.k*x+R
        wake=-self.u*2/3*(R/(R+self.k*x))
        #wake[r>a]=0
        return wake
    def wake_expansion(self,x):
        return self.k*x+self.D/2

class Park():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
    def deficit_(self,x,r,h):
        """
        Park_wake_model;
        """
        r=abs(r)
        R=self.D/2
        a=self.k*x+R
        wake=-self.u*(1-np.sqrt(1-self.ct))*(
            R/(R+self.k*x))**2
        #wake[r>a]=0
        return wake
    def wake_expansion(self,x):
        return self.k*x+self.D/2

class Modified_Park():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
    def deficit_(self,x,r,h):
        """
        Park_wake_model;
        """
        r=abs(r)
        R=self.D/2
        a=self.k*x+R
        wake=-self.u*(1-np.sqrt(1-self.ct))*(self.D/(self.D+2*self.k*x))**2
        #wake[r>a]=0
        return wake
    def wake_expansion(self,x):
        return self.k*x+self.D/2

class Jensen_Gauss():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
        self.Ia=Ia
    def constan_(self,x):
        kn=0.4
        self.Iwake=(kn*self.ct/(x/self.D)**0.5+self.Ia**0.5)**2
        self.a=0.5-0.5*np.sqrt(1-self.ct)  
        if self.Ia<=0:
            self.kwake=self.k
        else:
            self.kwake=self.k*self.Iwake/self.Ia   
        self.R=self.D/2   
    def deficit_(self,x,r,h):
        """
        Park_wake_model;
        """
        self.constan_(x)
        Ustar=self.u*(1-2*self.a/(1+self.kwake*x/self.R)**2)
        rx=self.kwake*x+self.R
        epart=-r**2/(2*(rx/2.58)**2)
        return -(self.u-Ustar)*5.16/np.sqrt(2*np.pi)*np.exp(epart)
    def wake_expansion(self,x):
        self.constan_(x)
        return self.kwake*x+self.D/2

class Park_Gauss():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
        self.Ia=Ia
        self.constan_()
    def constan_(self):
        self.a=0.5-0.5*np.sqrt(1-self.ct)   
        self.R=self.D/2   
    def deficit_(self,x,r,h):
        """
        Park_wake_model;
        """
        rx=self.k*x+self.R
        Ustar=self.u*(1-2*self.a/(1+self.k*x/self.R)**2)

        epart=1-(r/rx)**2
        return (self.u-Ustar)/(1-26*np.exp(1)/35)*(np.exp(epart)-1)
    def wake_expansion(self,x):
        return self.k*x+self.D/2

class Jensen_2D_k():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
        self.Ia=Ia
    def cosd(self,deg):
        return np.cos(deg*np.pi/180)
    def constan_(self,x):
        self.a=0.5-0.5*np.sqrt(1-self.ct)   
        self.R=self.D/2 
        kn=0.4
        self.Iwake=kn*self.ct/(x/self.D)+self.Ia 
        if self.Ia<=0:
            self.kwake=self.k
        else:
            self.kwake=self.k*self.Iwake/self.Ia   
        self.R=self.D/2         
        
    def deficit_(self,x,r,h):
        """
        Park_wake_model;
        """
        self.constan_(x)
        rx=self.kwake*x+self.R
        r1=self.R*np.sqrt((1-self.a)/(1-2*self.a))
        Ustar=self.u*(1-2*self.a/(1+self.kwake*x/self.R)**2)
        #print(Ustar)
        return (self.u-Ustar)*np.cos(np.pi*r/rx+np.pi)+Ustar-self.u
    def wake_expansion(self,x):
        self.constan_(x)
        return self.kwake*x+self.D/2

class Larsen():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
        self.cosntan_()
    def cosntan_(self):
        self.A=np.pi*(self.D/2)**2
        Deff=self.D*np.sqrt((1+np.sqrt(1-self.ct))/(2*np.sqrt(1-self.ct)))
        self.Rnb=1.08*self.D
        R95=0.5*(self.Rnb+self.Rnb)
        self.x0=9.5*self.D/((2*R95/Deff)**3-1)
        self.C1=((Deff/2)**2.5)*((105/2/np.pi)**(-0.5))*((self.ct*self.A*self.x0)**(-5/6))
    def deficit_(self,x,r,h):
        """
        Larsen;
        """
        r=abs(r)
        part1=-self.u/9*(self.ct*self.A*(x+self.x0)**(-2))**(1/3)
        part2=(r**(2/3))*((3*self.C1**2*self.ct*self.A*(x+self.x0))**(-0.5))
        part3=((35/2/np.pi)**(3/10))*((3*self.C1**2)**(-1/5))
        wake=part1*(part2-part3)**2
        #wake[r>a]=0
        return wake
    def wake_expansion(self,x):
        return (105*self.C1**2/2/np.pi)**(1/5)*(self.ct*self.A*(x+self.x0))**(1/3)

class Frandsen():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.Hub=Hub
        self.constan_()
    def constan_(self):
        self.A=np.pi*(self.D/2)**2
        self.beta=(1+np.sqrt(1-self.ct))/(2*np.sqrt(1-self.ct))
    def deficit_(self,x,r,h):
        """
        Frandsen;
        """
        r=abs(r)
        Dw=self.D*(self.beta**(3/2)+0.7*(x/self.D))**(1/3)
        Aw=np.pi*Dw*Dw/4
        wake=-self.u/2*(1-np.sqrt(1-2*self.A/Aw*self.ct))
        return wake
    def wake_expansion(self,x):
        return 0.5*self.D*(self.beta**(3/2)+0.7*(x/self.D))**(1/3)

class Bastankhah_yaw():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.ka=0.38
        self.kb=0.004
        self.dm=1.0
        self.Ia=Ia
        self.yaw=yaw
        self.Hub=Hub
        self.constan_()
        self.deflectionmodel=deflectionmodel(self.u,self.D,self.ct,self.Ia,self.yaw)
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

    def deficit_(self,x,r,h):

#远尾流
        sigma_y2 = self.ky * (x - self.x0) + self.sigma_y0
        sigma_z2 = self.kz * (x - self.x0) + self.sigma_z0
#        sigma_y = sigma_y * np.array(x >= self.x0) + self.sigma_y0 * np.array(x < self.x0)
#        sigma_z = sigma_z * np.array(x >= self.x0) + self.sigma_z0 * np.array(x < self.x0)

        sigma_y2 = sigma_y2 * np.array(x >= self.x0) 
        sigma_z2 = sigma_z2 * np.array(x >= self.x0)
#近
        near_wake_ramp_up = (x - self.xR) / (self.x0 - self.xR)
        near_wake_ramp_down = (self.x0 - x) / (self.x0 - self.xR)
        sigma_y1 = near_wake_ramp_down * 0.501 * self.D * np.sqrt(self.ct / 2.0)
        sigma_y1 += near_wake_ramp_up * self.sigma_y0
        sigma_y1 *= np.array(x >= self.xR)
        sigma_y1 += np.ones_like(sigma_y1) * np.array(x < self.xR) * 0.5 * self.D

        sigma_z1 = near_wake_ramp_down * 0.501 * self.D * np.sqrt(self.ct / 2.0)
        sigma_z1 += near_wake_ramp_up * self.sigma_z0
        sigma_z1 *= np.array(x >= self.xR)
        sigma_z1 += np.ones_like(sigma_z1) * np.array(x < self.xR) * 0.5 * self.D
        
        sigma_y = sigma_y2 * np.array(x >= self.x0) + sigma_y1 * np.array(x < self.x0)
        sigma_z = sigma_z2 * np.array(x >= self.x0) + sigma_z1 * np.array(x < self.x0)

        deflection=self.deflectionmodel.Deflection(x,r)
        deltau=1-np.sqrt(1 - (self.ct * self.cosd(self.yaw) / ( 8.0 * sigma_y * sigma_z / (self.D * self.D) )))
        expart=np.exp(-(r-deflection)**2/2/sigma_y/sigma_y)*np.exp(-(h-self.Hub)**2/2/sigma_z/sigma_z)
        wake=-self.u*deltau*expart
        #C=(
        #1-np.sqrt(
        #    1-self.sigma_y0*self.sigma_z0*
        #    self.M0/(sigma_y*sigma_z)
        #)
        #)
        #wake=self.u*(-C*np.exp(
        #-(r-deflection)**2/2/sigma_y/sigma_y
        #))
        return wake
    def wake_expansion(self,x):
        return 0.025*x+self.D*20

class QianIshihara():
    def __init__(self,u,D,Hub,ct,Ia,yaw,deflectionmodel,k=0.04):
        self.u=u
        self.D=D
        self.ct=np.minimum(0.999, ct)
        self.k=k
        self.yaw=yaw
        self.yaw_rad=self.yaw*np.pi/180
        self.Ia=np.maximum(0.01,Ia)
        self.Hub=Hub
        self.deflectionmodel=deflectionmodel(self.u,self.D,self.ct,self.Ia,self.yaw)
        self.constan_()
    def cosd(self,deg):
        return np.cos(deg*np.pi/180)
    def sind(self,deg):
        return np.sin(deg*np.pi/180)
    def constan_(self):
        I=self.Ia
        self.ct_=self.ct*self.cosd(self.yaw)**3
        self.k_star=0.11*self.ct_**1.07*I**0.2
        self.epsilonstar=0.23*self.ct_**(-0.25)*I**0.17
        #self.theta=0.3*self.alpha/self.cosalpha*(1-np.sqrt(1-self.ct*self.cosalpha))
        #self.x0=self.D*self.cosalpha*(1+np.sqrt(1-self.ct))/(np.sqrt(2)*(2.32*I+0.154*(1-np.sqrt(1-self.ct))))
        self.a=0.93*self.ct_**(-0.75)*I**(0.17)
        self.b=0.42*self.ct_**(0.6)*I**(0.2)
        self.c=0.15*self.ct_**(-0.25)*I**(-0.7)

    def deficit_(self,x,r,h):
        yd=self.deflectionmodel.Deflection(x,r)
        simga=self.k_star*x+self.epsilonstar*self.D
        #print(simga,yd)
        r=np.sqrt((r-yd)**2+(h-self.Hub)**2)
        part1=self.u/(self.a+self.b*x/self.D+self.c*(1+x/self.D)**(-2))**2
        part2=np.exp(-r*r/2/simga/simga)
        #print(part2)
        wake=-part1*part2
        return wake
    def wake_expansion(self,x):
        simga=self.k_star*x+self.epsilonstar*self.D
        return 4*np.sqrt(2*np.log(2))*simga
