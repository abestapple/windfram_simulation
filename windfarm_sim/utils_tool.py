import numpy as np
import math
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

def Layout_by_direction_index(turbine_sites, direction):
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
    return new_xy,nindex


def cw_rotate(tx,ty,x, y, ang):
    ang = math.radians(ang)
    new_x = round((x-tx) * math.cos(ang) + (y-ty) * math.sin(ang), 5)+tx
    new_y = round(-(x-tx) * math.sin(ang) + (y-ty) * math.cos(ang), 5)+ty
    return new_x, new_y
def plot_turbine(ax,turbine_sites,direction,D,yaw):
    for i in range(len(turbine_sites)):
        tx=float(turbine_sites[i][0])
        ty=float(turbine_sites[i][1])
        d=float(D[i])
        x1,x2=cw_rotate(tx,ty,tx+d/2, ty, direction-yaw[i])
        x3,x4=cw_rotate(tx,ty,tx-d/2, ty, direction-yaw[i])
        ax.plot([x1,x3],[x2,x4],color="k",lw=1)
        #ax.text(tx,ty,i)