import json
import xmltodict
from scipy.interpolate import interp1d
import numpy as np
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