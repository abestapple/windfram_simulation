import numpy as np
from windfarm_sim.utils_tool import Center,Wake_area,distance_line,Layout_by_direction,Layout_by_direction_index
from windfarm_sim.PoweCurver import power_curver,Get_pct

def wind_farm(flowfield,mesh,turbine_sites,direction,D,hub,ct,yaw_,wake_model,superpositionModel,deflectionmodel,turbulent_model):
    turbine_sites,sort_index=Layout_by_direction_index(turbine_sites, direction)
    velocity_defict=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
    ti_defict=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
    yaw=np.array(yaw_)[sort_index]
    D=np.array(D)[sort_index]
    hub=np.array(hub)[sort_index]
    flow_init=flowfield.flow.copy()
    flow_ti_init=flowfield.ti_flow.copy()
    for i in range(len(turbine_sites)):
        tx=float(turbine_sites[i][0])
        ty=float(turbine_sites[i][1])
        d=float(D[i])
        ix=mesh.find_y(mesh.x[0,:],[tx])[0]
        iy=mesh.find_y(mesh.y[:,0],[ty])[0]
        u=flowfield.flow[iy,ix]
        Ia=flowfield.ti_flow[iy,ix]
        dirct=direction-yaw[i]
        kc,bc=Center(tx,ty,direction)
        kw,bw=Wake_area(tx,ty,dirct)
        xx=mesh.x[0,:]
        yyc=kc*xx+bc
        yyw=kw*xx+bw
        distance_2_line=distance_line(kw,bw,mesh.x,mesh.y)
        if (dirct>=0 and dirct<=90) or (dirct>270 and dirct<=360):
            down_index=np.where(distance_2_line>0)
        else: 
            down_index=np.where(distance_2_line<0)
        r=distance_line(kc,bc,mesh.x[down_index],mesh.y[down_index])
        xc=abs(distance_line(kw,bw,mesh.x[down_index],mesh.y[down_index]))
        model=wake_model(u,d,hub[i],ct,Ia,yaw[i],deflectionmodel)
        ti_model=turbulent_model(u,d,ct,Ia,yaw[i],deflectionmodel)
        #k,eps=model.wake_expansion()
        inddd=np.where(model.wake_expansion(xc)>abs(r))
        xc1=xc[inddd]
        r1=r[inddd]
        wake_index=(down_index[0][inddd],down_index[1][inddd])
        wake_deficit_temp=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
        wake_ti_deficit_temp=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
        wake_flow=model.deficit_(xc1,r1,hub[i])

        wake_flow_ti=ti_model.ti_deficit_(xc1,r1)
        wake_deficit_temp[wake_index]=wake_deficit_temp[wake_index]+wake_flow
        wake_ti_deficit_temp[wake_index]=wake_ti_deficit_temp[wake_index]+wake_flow_ti
        #if superpositionModel=="LinearSum":
        velocity_defict[wake_index]=superpositionModel(velocity_defict[wake_index],wake_deficit_temp[wake_index])
        #ti_defict[wake_index]=wake_ti_deficit_temp[wake_index]
        ti_defict[wake_index]=np.sqrt(ti_defict[wake_index]**2+wake_ti_deficit_temp[wake_index]**2)
        #ti_defict[wake_index]=ti_defict[wake_index]+wake_ti_deficit_temp[wake_index]
        #elif superpositionModel=="SquaredSum":
        #    velocity_defict[wake_index]=-np.sqrt(velocity_defict[wake_index]**2+wake_deficit_temp[wake_index]**2)
        flowfield.flow[wake_index]=velocity_defict[wake_index]+flow_init[wake_index]     
        flowfield.ti_flow[wake_index]=np.sqrt(ti_defict[wake_index]**2+flow_ti_init[wake_index]**2) 
        #flowfield.flow[wake_index]=flowfield.flow[wake_index]+wake_flow
        #flowfield.flow[down_index]=flowfield.flow[down_index]+wake.gauss_ge(xc,r,u,D,ct)
        #flowfield.flow[down_index]=flowfield.flow[down_index]+wake_flow
        #flowfield.flow[down_index]=flowfield.flow[down_index]

def wind_farm_powercurver(flowfield,mesh,turbine_sites,direction,D,hub,wtg_file,yaw_,wake_model,superpositionModel,deflectionmodel,turbulent_model):
    ws,ps,cts=power_curver(wtg_file)
    turbine_sites,sort_index=Layout_by_direction_index(turbine_sites, direction)
    velocity_defict=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
    ti_defict=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
    flow_init=flowfield.flow.copy()
    yaw=np.array(yaw_)[sort_index]
    D=np.array(D)[sort_index]
    hub=np.array(hub)[sort_index]
    flow_ti_init=flowfield.ti_flow.copy()
    for i in range(len(turbine_sites)):
        tx=float(turbine_sites[i][0])
        ty=float(turbine_sites[i][1])
        d=float(D[i])
        ix=mesh.find_y(mesh.x[0,:],[tx])[0]
        iy=mesh.find_y(mesh.y[:,0],[ty])[0]
        u=flowfield.flow[iy,ix]
        Ia=flowfield.ti_flow[iy,ix]
        dirct=direction-yaw[i]
        p,ct=Get_pct(ws,ps,cts,u)
        kc,bc=Center(tx,ty,direction)
        kw,bw=Wake_area(tx,ty,dirct)
        xx=mesh.x[0,:]
        yyc=kc*xx+bc
        yyw=kw*xx+bw
        distance_2_line=distance_line(kw,bw,mesh.x,mesh.y)
        if (dirct>=0 and dirct<=90) or (dirct>270 and dirct<=360):
            down_index=np.where(distance_2_line>0)
        else: 
            down_index=np.where(distance_2_line<0)
        r=distance_line(kc,bc,mesh.x[down_index],mesh.y[down_index])
        xc=abs(distance_line(kw,bw,mesh.x[down_index],mesh.y[down_index]))
        model=wake_model(u,d,hub[i],ct,Ia,yaw[i],deflectionmodel)
        ti_model=turbulent_model(u,d,ct,Ia,yaw[i],deflectionmodel)
        #k,eps=model.wake_expansion()
        inddd=np.where(model.wake_expansion(xc)>abs(r))
        xc1=xc[inddd]
        r1=r[inddd]
        wake_index=(down_index[0][inddd],down_index[1][inddd])
        wake_deficit_temp=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
        wake_ti_deficit_temp=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
        wake_flow=model.deficit_(xc1,r1,hub[i])
        wake_flow_ti=ti_model.ti_deficit_(xc1,r1)
        wake_deficit_temp[wake_index]=wake_deficit_temp[wake_index]+wake_flow
        wake_ti_deficit_temp[wake_index]=wake_ti_deficit_temp[wake_index]+wake_flow_ti
        #if superpositionModel=="LinearSum":
        velocity_defict[wake_index]=superpositionModel(velocity_defict[wake_index],wake_deficit_temp[wake_index])
        ti_defict[wake_index]=np.sqrt(ti_defict[wake_index]**2+wake_ti_deficit_temp[wake_index]**2)
        #elif superpositionModel=="SquaredSum":
        #    velocity_defict[wake_index]=-np.sqrt(velocity_defict[wake_index]**2+wake_deficit_temp[wake_index]**2)
        flowfield.flow[wake_index]=velocity_defict[wake_index]+flow_init[wake_index]
        flowfield.ti_flow[wake_index]=np.sqrt(ti_defict[wake_index]**2+flow_ti_init[wake_index]**2)


def VPCT_Turbines_ct(Turbine_Sites,D,hub,ct,u,direction,ia,yaw_,wake_model,superpositionModel,deflectionmodel,turbulent_model):
    turbine_sites,sort_index=Layout_by_direction_index(Turbine_Sites.copy(),direction)
    turbine_sites_=Turbine_Sites.copy()
    velocity_defict=np.zeros(len(turbine_sites_))
    ti_defict=np.zeros(len(turbine_sites_))
    yaw=np.array(yaw_)[sort_index]
    D=np.array(D)[sort_index]
    hub=np.array(hub)[sort_index]
    U=np.zeros(len(turbine_sites_))
    U[:]=u
    Ia=np.zeros(len(turbine_sites_))
    Ia[:]=ia
    inds=1
    for i in range(len(turbine_sites_)-1):
        ind=inds
        tx,ty=turbine_sites.pop(0)
        kc,bc=Center(tx,ty,direction)
        kw,bw=Wake_area(tx,ty,direction)
        for tx1,ty1 in turbine_sites:
            r=distance_line(kc,bc,tx1,ty1)
            x=abs(distance_line(kw,bw,tx1,ty1))
            #print(r,x)
            model=wake_model(U[i],D[i],hub[i],ct,Ia[i],yaw[i],deflectionmodel)
            ti_model=turbulent_model(U[i],D[i],ct,Ia[i],yaw[i],deflectionmodel)
            #k,eps=model.wake_expansion()
            if abs(r)>(model.wake_expansion(x)):
                wake_flow=0
            else:
                #wake_flow=model.deficit_(x,r)
                wake_flow=model.deficit_(x,r,hub[i])
            #U[ind]=U[ind]+wake_flow
            wake_flow_ti=ti_model.ti_deficit_(x,r)
            velocity_defict_temp=np.zeros(len(turbine_sites_))
            velocity_defict_temp[ind]=velocity_defict_temp[ind]+wake_flow
            ti_defict_temp=np.zeros(len(turbine_sites_))
            ti_defict_temp[ind]=ti_defict_temp[ind]+wake_flow_ti
            
            #if superpositionModel=="LinearSum":
            velocity_defict[ind]=superpositionModel(velocity_defict[ind],velocity_defict_temp[ind])
            ti_defict[ind]=np.sqrt(ti_defict[ind]**2+ti_defict_temp[ind]**2)
            #elif superpositionModel=="SquaredSum":
            #    velocity_defict[ind]=-np.sqrt(velocity_defict[ind]**2+velocity_defict_temp[ind]**2)
            U=np.array(velocity_defict)+u
            #print(velocity_defict_temp,velocity_defict)
            Ia=np.sqrt(ti_defict**2+np.array(Ia)**2)
            ind=ind+1
        inds=inds+1
    return list(U[sort_index])

def Rotor_average(func,x,r,D,hhub):
    rlist=np.linspace(-1,1,11)*D/2+r
    hlist=np.array(list(filter(lambda x: x*1!=0.,np.linspace(-1,1,11))))*D/2+hhub
    deficit_hor=func(x,rlist,hhub)
    deficit_ver=func(x,r,hlist)
    return (deficit_hor.mean()+deficit_ver.mean())/2
def VPCT_Turbines(Turbine_Sites,D,hub,wtg_file,u,direction,ia,yaw_,wake_model,superpositionModel,deflectionmodel,turbulent_model):
    ws,ps,cts=power_curver(wtg_file)
    turbine_sites,sort_index=Layout_by_direction_index(Turbine_Sites.copy(),direction)
    yaw=np.array(yaw_)[sort_index]
    D=np.array(D)[sort_index]
    hub=np.array(hub)[sort_index]
    turbine_sites_=Turbine_Sites.copy()
    velocity_defict=np.zeros(len(turbine_sites_))
    ti_defict=np.zeros(len(turbine_sites_))
    U=np.zeros(len(turbine_sites_))
    U[:]=u
    Ia=np.zeros(len(turbine_sites_))
    Ia[:]=ia
    inds=1
    for i in range(len(turbine_sites_)-1):
        ind=inds
        tx,ty=turbine_sites.pop(0)
        kc,bc=Center(tx,ty,direction)
        kw,bw=Wake_area(tx,ty,direction)
        for tx1,ty1 in turbine_sites:
            
            r=distance_line(kc,bc,tx1,ty1)
            x=abs(distance_line(kw,bw,tx1,ty1))
            #print(r,x)
            p,ct=Get_pct(ws,ps,cts,U[i])
            model=wake_model(U[i],D[i],hub[i],ct,Ia[i],yaw[i],deflectionmodel)
            ti_model=turbulent_model(U[i],D[i],ct,Ia[i],yaw[i],deflectionmodel)
            #k,eps=model.wake_expansion()
            if abs(r)>(model.wake_expansion(x)):
                wake_flow=0
            else:
                wake_flow=model.deficit_(x,r,hub[i])
                #wake_flow=Rotor_average(model.deficit_,x,r,D[i+1],hub[i+1])
            #U[ind]=U[ind]+wake_flow

            wake_flow_ti=ti_model.ti_deficit_(x,r)
            #wake_flow_ti=Rotor_average(ti_model.ti_deficit_,x,r,D[i+1])
            velocity_defict_temp=np.zeros(len(turbine_sites_))
            velocity_defict_temp[ind]=velocity_defict_temp[ind]+wake_flow

            ti_defict_temp=np.zeros(len(turbine_sites_))
            ti_defict_temp[ind]=ti_defict_temp[ind]+wake_flow_ti

            #if superpositionModel=="LinearSum":
            velocity_defict[ind]=superpositionModel(velocity_defict[ind],velocity_defict_temp[ind])
            #print(ti_defict_temp,ti_defict)
            ti_defict[ind]=np.sqrt(ti_defict[ind]**2+ti_defict_temp[ind]**2)
            #print("......")
            #elif superpositionModel=="SquaredSum":
            #    velocity_defict[ind]=-np.sqrt(velocity_defict[ind]**2+velocity_defict_temp[ind]**2)
            U=np.array(velocity_defict)+u
            #print(velocity_defict_temp,velocity_defict)
            #Ia=np.sqrt(ti_defict**2+np.array(Ia)**2)
            #print(Ia)
            ind=ind+1
        Ia[inds]=np.sqrt(ti_defict[inds]**2+np.array(Ia[inds])**2)
        inds=inds+1
    storge_p=[]
    storge_ct=[]
    U=U[sort_index]
    Ia=Ia[sort_index]
    for u_ in U:
        p_,ct_=Get_pct(ws,ps,cts,u_)
        storge_p.append(p_)
        storge_ct.append(ct_)
    return list(U),storge_p,storge_ct,list(Ia)

def Timeseries_windfarm(Turbine_Sites,D,hub,wtg_file,u_series,direction_series,ia_series,yaw,wake_model,superpositionModel,deflectionmodel,turbulentmodel):
    if len(u_series)!=len(direction_series):
        print("时间序列长度不一致")
    else:
        all_u=[]
        all_p=[]
        all_ct=[]
        for u,dirs,ia in zip(u_series,direction_series,ia_series):
            u_temp,p_temp,ct_temp,_=VPCT_Turbines(Turbine_Sites,D,hub,wtg_file,u,dirs,ia,yaw,wake_model,superpositionModel,deflectionmodel,turbulentmodel)
            all_u.append(u_temp)
            all_p.append(p_temp)
            all_ct.append(ct_temp)

    return np.array(all_u),np.array(all_p),np.array(all_ct)


