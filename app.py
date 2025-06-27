import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
#from st_aggrid import AgGrid,GridOptionsBuilder
import matplotlib.ticker as ticker
import math
import plotly.graph_objs as go

from windfarm_sim.windfarm import wind_farm,wind_farm_powercurver,VPCT_Turbines,Timeseries_windfarm,VPCT_Turbines_ct
from windfarm_sim.Field import Mesh,Flowfield
from windfarm_sim.wake_deficit import Bastankhah,guass_Ge,Jensen,Park,Modified_Park,Larsen,Frandsen,guass_XA,Bastankhah_yaw,QianIshihara,Jensen_Gauss,Park_Gauss,Jensen_2D_k,Gauss,flex_gauss
from windfarm_sim.superposition import LinearSum,SquaredSum
from windfarm_sim.turbulent_model import Qian_Ishihara_turbulent_model
from windfarm_sim.deflectionModel import guass_Bastankhah_yaw,Jimenez,Qian_Ishihara
from windfarm_sim.utils_tool import plot_turbine
#from login import check_password
import hmac  
st.set_page_config(page_title="风电场计算",layout="wide")
def check_password(): 
    st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
	.e8zbici0{visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>""", unsafe_allow_html=True)
    def login_form(): 
	#st.set_page_config(page_title="风电场计算",layout="wide")
        col0,col1, col2 = st.columns([0.25,0.5,0.25]) 
        with col1: 
        	with st.form("Credentials"):  
            		col0,col1, col2 = st.columns([0.3,0.6,0.1])
            		with col0:  
                		st.write("  ")  
            		with col1:  
                		st.header(":blue[WINDFARM ANALYSIS]")
            		with col2:
                		st.write("  ")    
            		st.text_input("Username", key="username")  
            		st.text_input("Password", type="password", key="password")  
            		# 将按钮靠右放置  
            		cols = st.columns([4, 1])  
            		cols[1].form_submit_button("Login", on_click=password_entered)  
            		# st.form_submit_button("登录", on_click=password_entered)   
    def password_entered():  
        """Checks whether a password entered by the user is correct."""  
        if st.session_state["username"] in st.secrets[  
            "passwords"  
        ] and hmac.compare_digest(  
            st.session_state["password"],  
            st.secrets.passwords[st.session_state["username"]],  
        ):  
            st.session_state["password_correct"] = True  
            del st.session_state["password"]  
            del st.session_state["username"]  
        else:  
            st.session_state["password_correct"] = False  
    if st.session_state.get("password_correct", False):  
        # st.success("登录成功！")  
        return True  
    # Show inputs for username + password.  
    login_form()  
    if "password_correct" in st.session_state:  
        st.error("😕 账号不存在或者密码不正确")  
    return False 
if not check_password():  
    st.stop()

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
	.e8zbici0{visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)



st.title('风电场模拟计算')
wtgfiles={"NREL5MW":"NREL-5MW.wtg","NREL15MW":"NREL-15MW.wtg","Vestas-V80":"Vestas-V80.wtg","H165-4.0MW_1.04":"H165-4.0MW_1.04.wtg","H165-4.0MW_1.225":"H165-4.0MW_1.225.wtg"}
if 'wtgfiles' not in st.session_state:
	st.session_state["wtgfiles"]=wtgfiles

config = {
    "font.family": 'serif', # 衬线字体
    "font.size": 12, # 相当于小四大小
    "font.serif": ['SimSun'], # 宋体
    "mathtext.fontset": 'stix', # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
    'axes.unicode_minus': False # 处理负号，即-号
}

font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 10,
}

def convert_df(df):
    return df.to_csv().encode('utf-8')

if 'x' not in st.session_state:
    st.session_state["x"]=[200]
    st.session_state["y"]=[400]
    st.session_state["d"]=[126]
    st.session_state["H"]=[100]
    st.session_state["yaw"]=[0]
if 'df' not in st.session_state:
    st.session_state["df"]=0
#df = pd.DataFrame({"X": st.session_state["x"], "Y": st.session_state["y"]})

if "u_storge_all" not in st.session_state:
	st.session_state["u_storge_all"]=0
	st.session_state["p_storge_all"]=0
	st.session_state["ct_storge_all"]=0

def add():
    n=len(st.session_state["x"])
    for i in range(n):
        st.session_state["x"][i]=list(st.session_state["df"].X)[i]
        st.session_state["y"][i]=list(st.session_state["df"].Y)[i]
        st.session_state["d"][i]=list(st.session_state["df"].D)[i]
        st.session_state["H"][i]=list(st.session_state["df"].D)[i]
        st.session_state["yaw"][i]=list(st.session_state["df"].Yaw)[i]
    st.session_state["x"].append("")
    st.session_state["y"].append("")
    st.session_state["d"].append("")
    st.session_state["H"].append("")
    st.session_state["yaw"].append("")

grid_options = {
    "columnDefs": [
        {
            "headerName": "X",
            "field": "X",
            "editable": True,
            "width":54
        },
        {
            "headerName": "Y",
            "field": "Y",
            "editable": True,
            "width":54
        }, 
        {
            "headerName": "D",
            "field": "D",
            "editable": True,
            "width":54
        }, 
        {
            "headerName": "H",
            "field": "H",
            "editable": True,
            "width":54
        }, 
        {
            "headerName": "Yaw",
            "field": "Yaw",
            "editable": True,
            "width":54
        }, 
    ],
}



with st.sidebar:
	with st.expander("风场尺度参数设置"):
		form = st.form(key="form_settings")
		nx = form.text_input(
			"输入X方向网格格点数",
        	1000,
        	key="nx",
        	on_change=None
    	)
		ny = form.text_input(
			"输入Y方向网格格点数",
        	400,
        	key="ny",
        	on_change=None
    	)
		dx = form.text_input(
			"输入X方向网格分辨率",
        	3,
        	key="dx",
        	on_change=None
    	)
		dy = form.text_input(
			"输入Y方向网格分辨率",
        	3,
        	key="dy",
        	on_change=None
    	)
		form.form_submit_button(label="激活设置")
	with st.expander("流场参数配置"):
		optionflow = st.selectbox(
    '流场数据源配置',
    ('单风速/风向', '风速和风向时间序列',))
		if optionflow=="单风速/风向":
			form = st.form(key="form_flow")
			vel = form.text_input(
			"风速大小",
        	10,
        	key="vel",
        	on_change=None
    		)
			Ti = form.text_input(
			"湍流强度",
        	0.08,
        	key="ti",
        	on_change=None
    		)
			direction = form.text_input(
			"风向",
        	270,
        	key="direction",
        	on_change=None
    		)
			form.form_submit_button(label="激活设置")
		else:
			uploaded_series = st.file_uploader("上传风速风向时间序列数据")
			#if uploaded_series is not None:
				#timeseries = pd.read_csv(uploaded_series)

	with st.expander("风电场计算方案配置"):
		tab1, tab2, tab3 = st.tabs(["尾流模型", "风力机类型", "风力机机位"])
		with tab1:
			option = st.selectbox(
			'尾流模型',
			('Bastankhah_guass','Gauss','guass_XA','GaussGe','flex_gauss','Jensen','Jensen_2D_k','Jensen_Gauss','Park','Park_Gauss','Modified_Park','Larsen','Frandsen','Bastankhah_yaw','QianIshihara'))
			if option=="GaussGe":
				wakemodel=guass_Ge
			if option=="Bastankhah_guass":
				wakemodel=Bastankhah
			if option=="Jensen":
				wakemodel=Jensen
			if option=="Park":
				wakemodel=Park		
			if option=="Modified_Park":
				wakemodel=Modified_Park
			if option=="Larsen":
				wakemodel=Larsen
			if option=="Frandsen":
				wakemodel=Frandsen
			if option=="guass_XA":
				wakemodel=guass_XA
			if option=="Bastankhah_yaw":
				wakemodel=Bastankhah_yaw
			if option=="QianIshihara":
				wakemodel=QianIshihara
			if option=="Gauss":
				wakemodel=Gauss
			if option=="Jensen_Gauss":
				wakemodel=Jensen_Gauss
			if option=="Park_Gauss":
				wakemodel=Park_Gauss
			if option=="Jensen_2D_k":
				wakemodel=Jensen_2D_k
			if option=="flex_gauss":
				wakemodel=flex_gauss
			#print(Gauss)
			option_superpos = st.selectbox(
			'叠加模型',
			('LinearSum', 'SquaredSum'))
			if option_superpos=="LinearSum":
				superpositionModel=LinearSum
			if option_superpos=="SquaredSum":
				superpositionModel=SquaredSum	

			option_Deflection = st.selectbox(
			'偏转尾流模型',
			('guass_Bastankhah_yaw', 'Jimenez','Qian_Ishihara'))
			if option_Deflection=="guass_Bastankhah_yaw":
				DeflectionModel=guass_Bastankhah_yaw
			if option_Deflection=="Jimenez":
				DeflectionModel=Jimenez	
			if option_Deflection=="Qian_Ishihara":
				DeflectionModel=Qian_Ishihara	
			option_turbulentmodel = st.selectbox(
			'湍流强度模型',
			('Qian_Ishihara_turbulent_model',))
			if option_turbulentmodel=="Qian_Ishihara_turbulent_model":
				turbulentmodel=Qian_Ishihara_turbulent_model
		with tab2:
			genre = st.radio(
			"类型选择",
			('固定值', '性能曲线'))
			if genre=="固定值":
				form = st.form(key="form_configure")
				ct = form.text_input(
				"推力系数",
				0.5,
				key="ct",
				on_change=None
				)
				form.form_submit_button(label="激活设置")
			else:
				optionpower = st.selectbox(
				'性能曲线',
				tuple(st.session_state["wtgfiles"].keys()))
				#st.write(random.random())
				power_curver=st.session_state["wtgfiles"].get(optionpower)
				uploaded_file = st.file_uploader("上传性能曲线")
				if uploaded_file is not None:
					#st.write(uploaded_file.name)
					power_curver = uploaded_file.name
					st.session_state["wtgfiles"][uploaded_file.name[:-4]]=uploaded_file.name
										
		with tab3:
			uploaded_pos = st.file_uploader("上传机位点")
			if uploaded_pos is not None:
				dataframe_pos = pd.read_csv(uploaded_pos,header=None)
				dataframe_pos.columns=["X","Y","D","H","Yaw"]
				st.session_state["x"]=list(dataframe_pos.X)
				st.session_state["y"]=list(dataframe_pos.Y)
				st.session_state["d"]=list(dataframe_pos.D)
				st.session_state["H"]=list(dataframe_pos.H)
				st.session_state["yaw"]=list(dataframe_pos.Yaw)
			if st.button("增加机位"):
				add()
			else:
				pass
			df = pd.DataFrame({"X": st.session_state["x"], "Y": st.session_state["y"],"D": st.session_state["d"],"H": st.session_state["H"],"Yaw": st.session_state["yaw"]})
			new_df = st.data_editor(df,use_container_width=False, hide_index=True, num_rows="dynamic")
			#gb = GridOptionsBuilder.from_dataframe(df)
			#selection_mode = 'single' # 定义单选模式，多选为'multiple'
			#enable_enterprise_modules = True 
			#gb.configure_selection(selection_mode, use_checkbox=True) # 定义use_checkbox
			#gb.configure_side_bar()
			#gb.configure_grid_options(domLayout='normal')
			#gb.configure_pagination(paginationAutoPageSize=True)
			#gridOptions = gb.build()
			#grid_return = AgGrid(df, grid_options,theme="streamlit")
			#new_df = grid_return["data"]
			st.session_state["df"]=new_df


#@st.cache_data
def Creat(nx,ny,dx,dy,velocity,direction,Ia,turbine_sites,D,hub,ct,yaw,wakemodel,_superpositionModel,_deflectionmodel,turbulentmodel):

	flowfield=Flowfield(velocity,Ia,nx,ny,dx,dy)
	#flowfield.change_flow([10,20],[50,30],[11,11])
	mesh=Mesh(nx,ny,dx,dy)
	radio=nx/ny
	figsize=(8, 6.9/radio) if radio>=1 else (4.5*radio,4)
	wind_farm(flowfield,mesh,turbine_sites,direction,D,hub,ct,yaw,wakemodel,_superpositionModel,_deflectionmodel,turbulentmodel)
	fig, ax = plt.subplots(figsize=figsize)
	plot_turbine(ax,turbine_sites,direction,D,yaw)
	#cb=ax.contourf(mesh.x,mesh.y,flowfield.flow,levels=50,cmap="Spectral_r")
	cb=ax.contourf(mesh.x,mesh.y,flowfield.flow,levels=50,cmap="jet")
	ax.set_xlim([mesh.x.min(),mesh.x.max()])
	ax.set_ylim([mesh.y.min(),mesh.y.max()])
	ax.tick_params(axis='x',colors='white')
	ax.tick_params(axis='y',colors='white')
	ax.axvline(linewidth=2,color='white')
	ax.axhline(linewidth=2,color='white')
	#plt.tick_params(labelsize=5)
	plt.yticks(fontproperties = 'Times New Roman', size = 5)
	plt.xticks(fontproperties = 'Times New Roman', size = 5)
	fig.patch.set_facecolor('#0E1117')
	cbbar=fig.colorbar(cb,pad=0.01)
	cbytick_obj = plt.getp(cbbar.ax, 'yticklabels' ) #Set y tick label color
	plt.setp(cbytick_obj, color='white')
	cbbar.ax.tick_params(which = 'major', length = 4, color = "white",labelsize=6)
	tick_locator = ticker.MaxNLocator(nbins=5)  # colorbar上的刻度值个数
	cbbar.locator = tick_locator
	cbbar.update_ticks()

	fig1, ax1 = plt.subplots(figsize=figsize)
	plot_turbine(ax1,turbine_sites,direction,D,yaw)
	cb1=ax1.contourf(mesh.x,mesh.y,flowfield.ti_flow,levels=50,cmap="jet")
	ax1.set_xlim([mesh.x.min(),mesh.x.max()])
	ax1.set_ylim([mesh.y.min(),mesh.y.max()])
	ax1.tick_params(axis='x',colors='white')
	ax1.tick_params(axis='y',colors='white')
	ax1.axvline(linewidth=2,color='white')
	ax1.axhline(linewidth=2,color='white')
	#plt.tick_params(labelsize=5)
	plt.yticks(fontproperties = 'Times New Roman', size = 5)
	plt.xticks(fontproperties = 'Times New Roman', size = 5)
	fig1.patch.set_facecolor('#0E1117')
	cbbar1=fig1.colorbar(cb1,pad=0.01)
	cbytick_obj1 = plt.getp(cbbar1.ax, 'yticklabels' ) #Set y tick label color
	plt.setp(cbytick_obj1, color='white')
	cbbar1.ax.tick_params(which = 'major', length = 4, color = "white",labelsize=6)
	tick_locator1 = ticker.MaxNLocator(nbins=5)  # colorbar上的刻度值个数
	cbbar1.locator = tick_locator1
	cbbar1.update_ticks()

	#plt.rcParams.update(config)
	return fig,fig1

#@st.cache_data
def Creat_powercurver(nx,ny,dx,dy,velocity,direction,Ia,turbine_sites,D,hub,wtg_file,yaw,wakemodel,_superpositionModel,_deflectionmodel,turbulentmodel):
	flowfield=Flowfield(velocity,Ia,nx,ny,dx,dy)
	#flowfield.change_flow([10,20],[50,30],[11,11])
	mesh=Mesh(nx,ny,dx,dy)
	radio=nx/ny
	figsize=(8, 6.9/radio) if radio>=1 else (4.5*radio,4)
	wind_farm_powercurver(flowfield,mesh,turbine_sites,direction,D,hub,wtg_file,yaw,wakemodel,_superpositionModel,_deflectionmodel,turbulentmodel)
	fig, ax = plt.subplots(figsize=figsize)
	plot_turbine(ax,turbine_sites,direction,D,yaw)
	cb=ax.contourf(mesh.x,mesh.y,flowfield.flow,levels=50,cmap="jet")
	ax.set_xlim([mesh.x.min(),mesh.x.max()])
	ax.set_ylim([mesh.y.min(),mesh.y.max()])
	ax.tick_params(axis='x',colors='white')
	ax.tick_params(axis='y',colors='white')
	ax.axvline(linewidth=2,color='white')
	ax.axhline(linewidth=2,color='white')
	#plt.tick_params(labelsize=5)
	plt.yticks(fontproperties = 'Times New Roman', size = 5)
	plt.xticks(fontproperties = 'Times New Roman', size = 5)
	fig.patch.set_facecolor('#0E1117')
	cbbar=fig.colorbar(cb,pad=0.01)
	cbytick_obj = plt.getp(cbbar.ax, 'yticklabels' ) #Set y tick label color
	plt.setp(cbytick_obj, color='white')
	cbbar.ax.tick_params(which = 'major', length = 4, color = "white",labelsize=6)
	tick_locator = ticker.MaxNLocator(nbins=5)  # colorbar上的刻度值个数
	cbbar.locator = tick_locator
	cbbar.update_ticks()

	fig1, ax1 = plt.subplots(figsize=figsize)
	plot_turbine(ax1,turbine_sites,direction,D,yaw)
	cb1=ax1.contourf(mesh.x,mesh.y,flowfield.ti_flow,levels=50,cmap="jet")
	ax1.set_xlim([mesh.x.min(),mesh.x.max()])
	ax1.set_ylim([mesh.y.min(),mesh.y.max()])
	ax1.tick_params(axis='x',colors='white')
	ax1.tick_params(axis='y',colors='white')
	ax1.axvline(linewidth=2,color='white')
	ax1.axhline(linewidth=2,color='white')
	#plt.tick_params(labelsize=5)
	plt.yticks(fontproperties = 'Times New Roman', size = 5)
	plt.xticks(fontproperties = 'Times New Roman', size = 5)
	fig1.patch.set_facecolor('#0E1117')
	cbbar1=fig1.colorbar(cb1,pad=0.01)
	cbytick_obj1 = plt.getp(cbbar1.ax, 'yticklabels' ) #Set y tick label color
	plt.setp(cbytick_obj1, color='white')
	cbbar1.ax.tick_params(which = 'major', length = 4, color = "white",labelsize=6)
	tick_locator1 = ticker.MaxNLocator(nbins=5)  # colorbar上的刻度值个数
	cbbar1.locator = tick_locator1
	cbbar1.update_ticks()

	return fig,fig1

def Creat_powercurver_showpower(nx,ny,dx,dy,velocity,direction,turbine_sites,D,wtg_file,wakemodel):
	flowfield=Flowfield(velocity,nx,ny,dx,dy)
	#flowfield.change_flow([10,20],[50,30],[11,11])
	mesh=Mesh(nx,ny,dx,dy)
	u_storge,p_storge,ct_storge=wind_farm_powercurver_showpower(flowfield,mesh,turbine_sites,direction,D,wtg_file,wakemodel)
	return u_storge,p_storge,ct_storge

new_df_=new_df.copy()
for i in range(new_df_.shape[1]):
    new_df_.iloc[:,i].replace("", np.nan, inplace=True)
new_df_=new_df_.dropna(axis=0, how='any')
new_df_=new_df_.astype('float')
turbine_sites=list(zip(list(new_df_.X),list(new_df_.Y)))


Ds=list(new_df_.D)
yaws=list(new_df_.Yaw)
Hhubs=list(new_df_.H)
D=list(map(lambda x: float(x),Ds))
yaw=list(map(lambda x: float(x),yaws))
Hhub=list(map(lambda x: float(x),Hhubs))
nx=int(nx)
ny=int(ny)
dx=float(dx)
dy=float(dy)

if optionflow=="单风速/风向":
	velocity=float(vel)
	direction=float(direction)
	Ti=float(Ti)
	if genre=="固定值":
		ct=float(ct)
		#print("ww",wakemodel)
		fig,fig1=Creat(nx,ny,dx,dy,velocity,direction,Ti,turbine_sites,D,Hhub,ct,yaw,wakemodel,superpositionModel,DeflectionModel,turbulentmodel)
	else:
		fig,fig1=Creat_powercurver(nx,ny,dx,dy,velocity,direction,Ti,turbine_sites,D,Hhub,power_curver,yaw,wakemodel,superpositionModel,DeflectionModel,turbulentmodel)
	#vert_space = '<div style="margin: 0 1000px 100px 100px;"></div>'
	#st.markdown(vert_space, unsafe_allow_html=True)
	tab1, tab2 = st.tabs(["Velocity field", "Turbulent field"])
	with tab1:
		st.pyplot(fig,use_container_width=False)
	with tab2:
		st.pyplot(fig1,use_container_width=False)
	if option not in ["Modified_Park","Park","Frandsen","Jensen"]:
		C1, C2= st.columns(2)
		with C1:
			options = st.multiselect(
    			'显示所选位置的尾流廓线',
    			['0.5D', '1D', '2D', '3D','4D','5D', '6D', '8D','10D','12D', '14D', '16D','20D'],
    			['1D', '2D','4D','6D','8D'])
		with C2:
			turbine_id=st.selectbox(
				'选择显示的风力机编号',
				tuple(range(len(turbine_sites)))
			)
		display_pos=list(map(lambda x: float(x[:-1])*D[turbine_id],options))
		display_pos.sort()
		r=np.linspace(-1.5*D[turbine_id],1.5*D[turbine_id],51)
		#figc, axc = plt.subplots(figsize=(5,2))	
		#axc.set_ylabel("Velocity Deficit",fontsize=8)
		#figc.patch.set_facecolor('#0E1117')
		#figc.patch.set_facecolor('#454141')
		#axc.axvline(linewidth=2,color='white')
		#axc.axhline(linewidth=2,color='white')
		#axc.tick_params(axis='x',colors='white')
		#axc.tick_params(axis='y',colors='white')
		if genre=="固定值":
			trace_all=[]
			u_st1=VPCT_Turbines_ct(turbine_sites,D,Hhub,ct,velocity,direction,Ti,yaw,wakemodel,superpositionModel,DeflectionModel,turbulentmodel)
			for xi in display_pos:
				model=wakemodel(u_st1[turbine_id],D[turbine_id],Hhub[turbine_id],ct,Ti,yaw[turbine_id],DeflectionModel)			
				trace = go.Scatter(
					x = r/D[turbine_id],
					y = model.deficit_(xi,r,Hhub[turbine_id])/u_st1[turbine_id],
					mode = 'lines + markers',
					name = '{}Ds'.format(xi/D[turbine_id])
				)
				trace_all.append(trace)
				#axc.plot(r,wakemodel(np.array(xi),r,velocity,D[turbine_id],ct),label="{}D".format(xi/D[turbine_id]),marker="o",markersize=2)
				#print(r/D[turbine_id],model.deficit_(xi,r,Hhub[turbine_id])/u_st1[turbine_id])
		else:
			trace_all=[]
			u_st,p_st,ct_st,_=VPCT_Turbines(turbine_sites,D,Hhub,power_curver,velocity,direction,Ti,yaw,wakemodel,superpositionModel,DeflectionModel,turbulentmodel)
			for xi in display_pos:
				model=wakemodel(u_st[turbine_id],D[turbine_id],Hhub[turbine_id],ct_st[turbine_id],Ti,yaw[turbine_id],DeflectionModel)
				trace = go.Scatter(
					x = r/D[turbine_id],
					y = model.deficit_(xi,r,Hhub[turbine_id])/u_st[turbine_id],
					mode = 'lines + markers',
					name = '{}D'.format(xi/D[turbine_id])
				)
				trace_all.append(trace)
				#axc.plot(r,wakemodel(np.array(xi),r,ustorge[turbine_id],D[turbine_id],ctstorge[turbine_id]),label="{}D".format(xi/D[turbine_id]))
		#plt.legend(labelcolor='linecolor')
		#plt.rcParams['legend.fontsize'] = 6			
		#st.pyplot(figc,use_container_width=True)
		st.plotly_chart(trace_all, use_container_width=True)

else:
	if uploaded_series is not None:
		series=pd.read_csv(uploaded_series,header=None)
		series.columns=["Time","U","DIR","Ti"]
		series.index=series.Time
		if genre=="固定值":
			if 'ind' not in st.session_state:
				st.session_state["ind"]=list(series.index)[0]
			st.session_state["ind"]= st.select_slider(
				'Select time',
				options=list(series.index))			
			ct=float(ct)
			fig,fig1=Creat(nx,ny,dx,dy,series.U[st.session_state["ind"]],series.DIR[st.session_state["ind"]],series.Ti[st.session_state["ind"]],turbine_sites,D,Hhub,ct,yaw,wakemodel,superpositionModel,DeflectionModel,turbulentmodel)
			tab1, tab2 = st.tabs(["Velocity", "Turbulent"])
			with tab1:
				st.pyplot(fig,use_container_width=False)
			with tab2:
				st.pyplot(fig1,use_container_width=False)		
		else:
			if 'ind' not in st.session_state:
				st.session_state["ind"]=list(series.index)[0]
			st.session_state["ind"]= st.select_slider(
				'Select time',
				options=list(series.index))
			fig,fig1=Creat_powercurver(nx,ny,dx,dy,series.U[st.session_state["ind"]],series.DIR[st.session_state["ind"]],series.Ti[st.session_state["ind"]],turbine_sites,D,Hhub,power_curver,yaw,wakemodel,superpositionModel,DeflectionModel,turbulentmodel)
			tab1, tab2 = st.tabs(["Velocity", "Turbulent"])
			with tab1:
				st.pyplot(fig,use_container_width=False)
			with tab2:
				st.pyplot(fig1,use_container_width=False)	
			u_storge_all,p_storge_all,ct_storge_all=Timeseries_windfarm(turbine_sites,D,Hhub,power_curver,list(series.U),list(series.DIR),list(series.Ti),yaw,wakemodel,superpositionModel,DeflectionModel,turbulentmodel)
			colr, cole= st.columns(2)
			turbine_id=st.selectbox(
				'选择显示的风力机编号',
				tuple(range(len(turbine_sites)))
				)

			result=pd.DataFrame(p_storge_all)
			result.index=series.index
			result_Csv = convert_df(result)
			st.download_button(
    			label="输出功率结果到文件",
    			data=result_Csv,
    			file_name='Result_power.csv',
    			mime='text/csv',
			)			
			with colr:
				st.subheader("风力机中心速度")
				x1 = np.array(series.index)
				y1 = np.array(pd.DataFrame(u_storge_all).iloc[:,turbine_id])
				#fig_plot1, ax1 = plt.subplots(figsize=(6,1.5))
				#ax1.plot(x1,y1,color='green', marker='o')	
				#ax1.set_xlabel("Velocity time series")
				#ax1.grid(ls = '-.', lw = 0.25)		
				#st.pyplot(fig_plot1,use_container_width=True)
				trace2 = go.Scatter(
					x = x1,
					y = y1,
					mode = 'lines + markers',
					name = 'line + markers'
				)
				st.plotly_chart([trace2], use_container_width=True)	
			with cole:
				st.subheader("风力机功率")
				x2 = np.array(series.index)
				y2 = np.array(pd.DataFrame(p_storge_all).iloc[:,turbine_id])
				#fig_plot2, ax2 = plt.subplots(figsize=(6,1.5))
				#ax2.plot(x2,y2,color='#ad4545', marker='.')	
				#ax2.set_xlabel("Power time series")	
				#ax2.grid(ls = '-.', lw = 0.25)		
				#st.pyplot(fig_plot2,use_container_width=True)
				trace1 = go.Scatter(
					x = x2,
					y = y2,
					mode = 'lines + markers',
					name = 'line + markers'
				)
				st.plotly_chart([trace1], use_container_width=True)								
			st.subheader("风电场发电量")
			x3 = np.array(series.index)
			y3 = np.array(pd.DataFrame(p_storge_all).sum(axis=1))
			trace0 = go.Scatter(
				x = x3,
				y = y3,
				mode = 'lines + markers',
				name = '发电量'
			)
			st.plotly_chart([trace0], use_container_width=True)
			#fig_plot3, ax3 = plt.subplots(figsize=(6,1.5))
			#ax3.plot(x3,y3,color='#d06868', marker="*")	
			#ax3.grid(ls = '-.', lw = 0.25)		
			#st.pyplot(fig_plot3,use_container_width=True)			
			#st.write(pd.DataFrame(u_storge_all))
			#st.write(np.array(series.index),np.array(u_storge_all))


