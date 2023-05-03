import numpy as np
from windfarm_sim.utils_tool import Center,Wake_area,distance_line,Layout_by_direction,Layout_by_direction_index
from windfarm_sim.PoweCurver import power_curver,Get_pct

def wind_farm(flowfield,mesh,turbine_sites,direction,D,ct,wake_model,superpositionModel):
    turbine_sites=Layout_by_direction(turbine_sites, direction)
    velocity_defict=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
    flow_init=flowfield.flow.copy()
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
        model=wake_model(u,d,ct)
        k,eps=model.wake_expansion()
        inddd=np.where((xc*k+eps)>r)
        xc1=xc[inddd]
        r1=r[inddd]
        wake_index=(down_index[0][inddd],down_index[1][inddd])
        wake_deficit_temp=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
        wake_flow=model.deficit_(xc1,r1)
        wake_deficit_temp[wake_index]=wake_deficit_temp[wake_index]+wake_flow
        if superpositionModel=="LinearSum":
            velocity_defict[wake_index]=velocity_defict[wake_index]+wake_deficit_temp[wake_index]
        elif superpositionModel=="SquaredSum":
            velocity_defict[wake_index]=-np.sqrt(velocity_defict[wake_index]**2+wake_deficit_temp[wake_index]**2)
        flowfield.flow[wake_index]=velocity_defict[wake_index]+flow_init[wake_index]        
        #flowfield.flow[wake_index]=flowfield.flow[wake_index]+wake_flow
        #flowfield.flow[down_index]=flowfield.flow[down_index]+wake.gauss_ge(xc,r,u,D,ct)
        #flowfield.flow[down_index]=flowfield.flow[down_index]+wake_flow
        #flowfield.flow[down_index]=flowfield.flow[down_index]

def wind_farm_powercurver(flowfield,mesh,turbine_sites,direction,D,wtg_file,wake_model,superpositionModel):
    ws,ps,cts=power_curver(wtg_file)
    turbine_sites=Layout_by_direction(turbine_sites, direction)
    velocity_defict=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
    flow_init=flowfield.flow.copy()
    for i in range(len(turbine_sites)):
        tx=float(turbine_sites[i][0])
        ty=float(turbine_sites[i][1])
        d=float(D[i])
        ix=mesh.find_y(mesh.x[0,:],[tx])[0]
        iy=mesh.find_y(mesh.y[:,0],[ty])[0]
        u=flowfield.flow[iy,ix]
        p,ct=Get_pct(ws,ps,cts,u)
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
        model=wake_model(u,d,ct)
        k,eps=model.wake_expansion()
        inddd=np.where((xc*k+eps)>r)
        xc1=xc[inddd]
        r1=r[inddd]
        wake_index=(down_index[0][inddd],down_index[1][inddd])
        wake_deficit_temp=np.zeros([mesh.x.shape[0],mesh.x.shape[1]])
        wake_flow=model.deficit_(xc1,r1)
        wake_deficit_temp[wake_index]=wake_deficit_temp[wake_index]+wake_flow
        if superpositionModel=="LinearSum":
            velocity_defict[wake_index]=velocity_defict[wake_index]+wake_deficit_temp[wake_index]
        elif superpositionModel=="SquaredSum":
            velocity_defict[wake_index]=-np.sqrt(velocity_defict[wake_index]**2+wake_deficit_temp[wake_index]**2)
        flowfield.flow[wake_index]=velocity_defict[wake_index]+flow_init[wake_index]

def VPCT_Turbines_ct(Turbine_Sites,D,ct,u,direction,wake_model,superpositionModel):
    turbine_sites,sort_index=Layout_by_direction_index(Turbine_Sites.copy(),direction)
    turbine_sites_=Turbine_Sites.copy()
    velocity_defict=np.zeros(len(turbine_sites_))
    U=np.zeros(len(turbine_sites_))
    U[:]=u
    inds=1
    for i in range(len(turbine_sites_)-1):
        ind=inds
        tx,ty=turbine_sites.pop(0)
        kc,bc=Center(tx,ty,direction)
        kw,bw=Wake_area(tx,ty,direction)
        for tx1,ty1 in turbine_sites:
            r=abs(distance_line(kc,bc,tx1,ty1))
            x=abs(distance_line(kw,bw,tx1,ty1))
            #print(r,x)
            model=wake_model(U[i],D[i],ct)
            k,eps=model.wake_expansion()
            if r>(k*x+eps):
                wake_flow=0
            else:
                wake_flow=model.deficit_(x,r)
            #U[ind]=U[ind]+wake_flow
            velocity_defict_temp=np.zeros(len(turbine_sites_))
            velocity_defict_temp[ind]=velocity_defict_temp[ind]+wake_flow
            if superpositionModel=="LinearSum":
                velocity_defict[ind]=velocity_defict[ind]+velocity_defict_temp[ind]
            elif superpositionModel=="SquaredSum":
                velocity_defict[ind]=-np.sqrt(velocity_defict[ind]**2+velocity_defict_temp[ind]**2)
            U=np.array(velocity_defict)+u
            #print(velocity_defict_temp,velocity_defict)
            ind=ind+1
        inds=inds+1
    return list(U[sort_index])

def VPCT_Turbines(Turbine_Sites,D,wtg_file,u,direction,wake_model,superpositionModel):
    ws,ps,cts=power_curver(wtg_file)
    turbine_sites,sort_index=Layout_by_direction_index(Turbine_Sites.copy(),direction)
    turbine_sites_=Turbine_Sites.copy()
    velocity_defict=np.zeros(len(turbine_sites_))
    U=np.zeros(len(turbine_sites_))
    U[:]=u
    inds=1
    for i in range(len(turbine_sites_)-1):
        ind=inds
        tx,ty=turbine_sites.pop(0)
        kc,bc=Center(tx,ty,direction)
        kw,bw=Wake_area(tx,ty,direction)
        for tx1,ty1 in turbine_sites:
            r=abs(distance_line(kc,bc,tx1,ty1))
            x=abs(distance_line(kw,bw,tx1,ty1))
            #print(r,x)
            p,ct=Get_pct(ws,ps,cts,U[i])
            model=wake_model(U[i],D[i],ct)
            k,eps=model.wake_expansion()
            if r>(k*x+eps):
                wake_flow=0
            else:
                wake_flow=model.deficit_(x,r)
            #U[ind]=U[ind]+wake_flow
            velocity_defict_temp=np.zeros(len(turbine_sites_))
            velocity_defict_temp[ind]=velocity_defict_temp[ind]+wake_flow
            if superpositionModel=="LinearSum":
                velocity_defict[ind]=velocity_defict[ind]+velocity_defict_temp[ind]
            elif superpositionModel=="SquaredSum":
                velocity_defict[ind]=-np.sqrt(velocity_defict[ind]**2+velocity_defict_temp[ind]**2)
            U=np.array(velocity_defict)+u
            #print(velocity_defict_temp,velocity_defict)
            ind=ind+1
        inds=inds+1
    storge_p=[]
    storge_ct=[]
    U=U[sort_index]
    for u_ in U:
        p_,ct_=Get_pct(ws,ps,cts,u_)
        storge_p.append(p_)
        storge_ct.append(ct_)
    return list(U),storge_p,storge_ct

def Timeseries_windfarm(Turbine_Sites,D,wtg_file,u_series,direction_series,wake_model,superpositionModel):
    if len(u_series)!=len(direction_series):
        print("时间序列长度不一致")
    else:
        all_u=[]
        all_p=[]
        all_ct=[]
        for u,dirs in zip(u_series,direction_series):
            u_temp,p_temp,ct_temp=VPCT_Turbines(Turbine_Sites,D,wtg_file,u,dirs,wake_model,superpositionModel)
            all_u.append(u_temp)
            all_p.append(p_temp)
            all_ct.append(ct_temp)

    return np.array(all_u),np.array(all_p),np.array(all_ct)


