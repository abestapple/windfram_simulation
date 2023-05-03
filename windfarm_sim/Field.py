import numpy as np
import matplotlib.pyplot as plt
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