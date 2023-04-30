import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math
import json
import xmltodict

class Mesh():
    def __init__(self,nx,ny,dx,dy):
        self.x=np.arange(0,nx*dx,dx)
        self.y=np.arange(0,ny*dy,dy)
        self.x,self.y=np.meshgrid(self.x,self.y)
    def find_y(self,arr,a):
        pos=[]
        for i in a:
            pos.append(np.where(abs(arr-i)==abs(arr-i).min())[0][0])
        return pos

class Flowfield():
    def __init__(self,uinit,nx,ny,dx,dy):
        self.nx=nx
        self.ny=ny
        self.dx=dx
        self.dy=dy
        self.flow=np.ones([ny,nx])
        self.flow[:,:]=uinit
        self.defit_field=np.zeros([ny,nx])
    def change_flow(self,x,y,var):
        self.flow[x,y]=var
    def plot_field(self,w,h):
        plt.figure(figsize=(w, h))
        mesh=Mesh(self.nx,self.ny,self.dx,self.dy)
        cb=plt.contourf(mesh.x,mesh.y,self.flow,levels=20)
        plt.xlim([mesh.x.min(),mesh.x.max()])
        plt.ylim([mesh.y.min(),mesh.y.max()])
class Wake_defict():
    def __init__(self):
        pass
    def gauss_ge(self,x,r,u=10,D=100,ct=0.5,k=0.075):
        """
            paper: A two-dimensional model based on the expansion of physical wake
            boundary for wind-turbine wakes
        """
        ro=D/2
        a=(k*x/ro+1)**2
        b=(1-2*ct/a)**0.5
        expin=-2/a*(r/ro)**2
        wake=-u*(1-b)*np.exp(expin)
        #print(a,b,expin)
        return wake
    def guass_Bastankhah(self,x,r,u,D,ct,k=0.07):
        """
         A new analytical model for wind-turbine wakes
            
         Majid Bastankhah, Fernando Porté-Agel*
        """
        beta=0.5*(1+np.sqrt(1-ct))/(np.sqrt(1-ct))
        e=0.25*np.sqrt(beta)
        a=(k*x/D+e)**2
        wake=-u*(1-np.sqrt(1-ct/8/a))*np.exp(-1/2/a*(r*r/D/D))
        return wake
    def Park(self,x,r,u,D,ct,k=0.07):
        """
        Park_wake_model;
        """
        R=D/2
        a=k*x+R
        wake=-u*(1-np.sqrt(1-ct))*(R/(R+k*x))**2
        wake[r>a]=0
        return wake
    def Modified_Park(self,x,r,u,D,ct,k=0.07):
        """
        Park_wake_model;
        """
        R=D/2
        a=k*x+R
        wake=-u*(1-np.sqrt(1-ct))*(D/(D+2*k*x))**2
        wake[r>a]=0
        return wake
    def wake_edge(self,x):
        return self.k*x+self.d0/2

def Center(tx,ty,direction):
    if direction==0:
        direction=360
    direction = math.radians(direction)
    k= math.cos(direction)/math.sin(direction)
    b=ty-k*tx
    return k,b

def Wake_area(tx,ty,direction):
    if direction==0:
        direction=360
    direction = math.radians(direction)
    k= -1/(math.cos(direction)/math.sin(direction))
    b=ty-k*tx
    return k,b
def distance_line(k,b,x1,y1):
    return (k*x1-y1+b)/np.sqrt(k**2+1)

def turbine_wake(flowfield,mesh,tx,ty,direction,D,ct,wake_model):
    ix=mesh.find_y(mesh.x[0,:],[tx])[0]
    iy=mesh.find_y(mesh.y[:,0],[ty])[0]
    u=flowfield.flow[iy,ix]
    kc,bc=Center(tx,ty,direction)
    kw,bw=Wake_area(tx,ty,direction)
    xx=mesh.x[0,:]
    yyc=kc*xx+bc
    yyw=kw*xx+bw
    distance_2_line=distance_line(kw,bw,mesh.x,mesh.y)
    if (direction>=0 and direction<=90) or (direction>270 and direction<=360):
        down_index=np.where(distance_2_line>0)
    else: 
        down_index=np.where(distance_2_line<0)
    r=abs(distance_line(kc,bc,mesh.x[down_index],mesh.y[down_index]))
    xc=abs(distance_line(kw,bw,mesh.x[down_index],mesh.y[down_index]))
    #flowfield.flow[down_index]=flowfield.flow[down_index]+wake.gauss_ge(xc,r,u,D,ct)
    flowfield.flow[down_index]=flowfield.flow[down_index]+wake_model(xc,r,u,D,ct)
    flowfield.flow[down_index]=flowfield.flow[down_index]

def turbine_wake_param(param):

    staus=param["staus"]
    pool_sema=param["pool_sema"]
	
    if staus:
        pool_sema.acquire()
    flowfield=param["flowfield"]
    mesh=param["mesh"]
    tx=param["tx"]
    ty=param["ty"]
    direction=param["direction"]
    D=param["D"]
    ct=param["ct"]
    wake_model=param["wake_model"]
    ix=mesh.find_y(mesh.x[0,:],[tx])[0]
    iy=mesh.find_y(mesh.y[:,0],[ty])[0]
    u=flowfield.flow[iy,ix]
    kc,bc=Center(tx,ty,direction)
    kw,bw=Wake_area(tx,ty,direction)
    xx=mesh.x[0,:]
    yyc=kc*xx+bc
    yyw=kw*xx+bw
    distance_2_line=distance_line(kw,bw,mesh.x,mesh.y)
    if (direction>=0 and direction<=90) or (direction>270 and direction<=360):
        down_index=np.where(distance_2_line>0)
    else: 
        down_index=np.where(distance_2_line<0)
    r=abs(distance_line(kc,bc,mesh.x[down_index],mesh.y[down_index]))
    xc=abs(distance_line(kw,bw,mesh.x[down_index],mesh.y[down_index]))
    #flowfield.flow[down_index]=flowfield.flow[down_index]+wake.gauss_ge(xc,r,u,D,ct)
    flowfield.flow[down_index]=flowfield.flow[down_index]+wake_model(xc,r,u,D,ct)
    flowfield.flow[down_index]=flowfield.flow[down_index]
    #flowfield.defit_field[:,:]=0
    #flowfield.defit_field[down_index]=wake_model(xc,r,u,D,ct)
    if staus:
        pool_sema.release()	
    return flowfield.flow,u

def wind_farm(flowfield,mesh,turbine_sites,direction,D,ct,wake_model):

    for i in range(len(turbine_sites)):
        tx=float(turbine_sites[i][0])
        ty=float(turbine_sites[i][1])
        d=float(D[i])
        ix=mesh.find_y(mesh.x[0,:],[tx])[0]
        iy=mesh.find_y(mesh.y[:,0],[ty])[0]
        u=flowfield.flow[iy,ix]
        kc,bc=Center(tx,ty,direction)
        kw,bw=Wake_area(tx,ty,direction)
        xx=mesh.x[0,:]
        yyc=kc*xx+bc
        yyw=kw*xx+bw
        distance_2_line=distance_line(kw,bw,mesh.x,mesh.y)
        if (direction>=0 and direction<=90) or (direction>270 and direction<=360):
            down_index=np.where(distance_2_line>0)
        else: 
            down_index=np.where(distance_2_line<0)
        r=abs(distance_line(kc,bc,mesh.x[down_index],mesh.y[down_index]))
        xc=abs(distance_line(kw,bw,mesh.x[down_index],mesh.y[down_index]))
        #flowfield.flow[down_index]=flowfield.flow[down_index]+wake.gauss_ge(xc,r,u,D,ct)
        flowfield.flow[down_index]=flowfield.flow[down_index]+wake_model(xc,r,u,d,ct)
        flowfield.flow[down_index]=flowfield.flow[down_index]

def power_curver(file):
    xml_file = open(file, 'r')
    xml_str = xml_file.read()
    json = xmltodict.parse(xml_str)
    dic=dict(json).get("WindTurbineGenerator")["PerformanceTable"]["DataTable"]["DataPoint"]
    ws=[]
    p=[]
    ct=[]
    for i in dic:
        ws.append(float(i.get("@WindSpeed")))
        p.append(float(i.get("@PowerOutput"))/1000)
        ct.append(float(i.get("@ThrustCoEfficient")))
    return ws,p,ct
def Get_pct(ws,p,ct,vs):
    f1 = interp1d(ws,p,kind='linear')
    f2 = interp1d(ws,ct,kind='linear')
    vl=np.array(ws)
    pl=np.array(p)
    ctl=np.array(ct)
    if vs<vl.min() or vs>vl.max():
        power=0
        Ct=0
    elif vs==vl.min():
        power=pl[0]
        Ct=ctl[0]
    elif vs==vl.max():
        power=pl[-1]
        Ct=ctl[-1]
    else:
        power=f1(vs)*1
        Ct=f2(vs)*1
    return power,Ct

def Layout_by_direction(turbine_sites, direction):
    direction = math.radians(270-direction)
    new_xy=[]
    for x,y in turbine_sites:
        new_x = round(float(x) * math.cos(direction) + float(y) * math.sin(direction),3)
        new_y = round(-float(x) * math.sin(direction) + float(y)* math.cos(direction),3)
        new_xy.append((new_x,new_y))
    nindex=np.argsort(np.array(new_xy)[:,0])
    new_xy=[]
    for i in nindex:
        new_xy.append(turbine_sites[i])
    return new_xy

def wind_farm_powercurver(flowfield,mesh,turbine_sites,direction,D,wtg_file,wake_model):
    ws,ps,cts=power_curver(wtg_file)
    u_storge=[]
    p_storge=[]
    ct_storge=[]
    turbine_sites=Layout_by_direction(turbine_sites, direction)
    for i in range(len(turbine_sites)):
        tx=float(turbine_sites[i][0])
        ty=float(turbine_sites[i][1])
        d=float(D[i])
        ix=mesh.find_y(mesh.x[0,:],[tx])[0]
        iy=mesh.find_y(mesh.y[:,0],[ty])[0]
        u=flowfield.flow[iy,ix]
        p,ct=Get_pct(ws,ps,cts,u)
        u_storge.append(u)
        p_storge.append(p)
        ct_storge.append(ct)
        kc,bc=Center(tx,ty,direction)
        kw,bw=Wake_area(tx,ty,direction)
        xx=mesh.x[0,:]
        yyc=kc*xx+bc
        yyw=kw*xx+bw
        distance_2_line=distance_line(kw,bw,mesh.x,mesh.y)
        if (direction>=0 and direction<=90) or (direction>270 and direction<=360):
            down_index=np.where(distance_2_line>0)
        else: 
            down_index=np.where(distance_2_line<0)
        r=abs(distance_line(kc,bc,mesh.x[down_index],mesh.y[down_index]))
        xc=abs(distance_line(kw,bw,mesh.x[down_index],mesh.y[down_index]))
        #flowfield.flow[down_index]=flowfield.flow[down_index]+wake.gauss_ge(xc,r,u,D,ct)
        flowfield.flow[down_index]=flowfield.flow[down_index]+wake_model(xc,r,u,d,ct)
        flowfield.flow[down_index]=flowfield.flow[down_index]
    return u_storge,p_storge,ct_storge

def wind_farm_powercurver_showpower(flowfield,mesh,turbine_sites,direction,D,wtg_file,wake_model):
    ws,ps,cts=power_curver(wtg_file)
    u_storge=[]
    p_storge=[]
    ct_storge=[]
    turbine_sites=Layout_by_direction(turbine_sites, direction)
    flow=flowfield.flow.copy()
    for i in range(len(turbine_sites)):
        tx=float(turbine_sites[i][0])
        ty=float(turbine_sites[i][1])
        d=float(D[i])
        ix=mesh.find_y(mesh.x[0,:],[tx])[0]
        iy=mesh.find_y(mesh.y[:,0],[ty])[0]
        u=flow[iy,ix]
        p,ct=Get_pct(ws,ps,cts,u)
        u_storge.append(u)
        p_storge.append(p)
        ct_storge.append(ct)
        kc,bc=Center(tx,ty,direction)
        kw,bw=Wake_area(tx,ty,direction)
        xx=mesh.x[0,:]
        yyc=kc*xx+bc
        yyw=kw*xx+bw
        distance_2_line=distance_line(kw,bw,mesh.x,mesh.y)
        if (direction>=0 and direction<=90) or (direction>270 and direction<=360):
            down_index=np.where(distance_2_line>0)
        else: 
            down_index=np.where(distance_2_line<0)
        r=abs(distance_line(kc,bc,mesh.x[down_index],mesh.y[down_index]))
        xc=abs(distance_line(kw,bw,mesh.x[down_index],mesh.y[down_index]))

        #flowfield.flow[down_index]=flowfield.flow[down_index]+wake.gauss_ge(xc,r,u,D,ct)
        flow[down_index]=flow[down_index]+wake_model(xc,r,u,d,ct)
        flow[down_index]=flow[down_index]
    return u_storge,p_storge,ct_storge