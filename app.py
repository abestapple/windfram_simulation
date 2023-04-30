import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
from windFarm_sim import Mesh,Flowfield,Wake_defict,wind_farm,wind_farm_powercurver,wind_farm_powercurver_showpower
from st_aggrid import AgGrid,GridOptionsBuilder

st.set_page_config(page_title="风电场计算",layout="wide")
st.title('风电场模拟计算')
wtgfiles={"NREL5MW":"NREL-5MW.wtg","NREL15MW":"NREL-15MW.wtg","Vestas-V80":"Vestas-V80.wtg"}
if 'wtgfiles' not in st.session_state:
	st.session_state["wtgfiles"]=wtgfiles
wake=Wake_defict()

config = {
    "font.family": 'serif', # 衬线字体
    "font.size": 12, # 相当于小四大小
    "font.serif": ['SimSun'], # 宋体
    "mathtext.fontset": 'stix', # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
    'axes.unicode_minus': False # 处理负号，即-号
}

def convert_df(df):
    return df.to_csv().encode('utf-8')

if 'x' not in st.session_state:
    st.session_state["x"]=[200]
    st.session_state["y"]=[200]
    st.session_state["d"]=[126]
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
    st.session_state["x"].append("")
    st.session_state["y"].append("")
    st.session_state["d"].append("")

grid_options = {
    "columnDefs": [
        {
            "headerName": "X",
            "field": "X",
            "editable": True,
            "width":90
        },
        {
            "headerName": "Y",
            "field": "Y",
            "editable": True,
            "width":90
        }, 
        {
            "headerName": "D",
            "field": "D",
            "editable": True,
            "width":90
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
        	1,
        	key="dx",
        	on_change=None
    	)
		dy = form.text_input(
			"输入Y方向网格分辨率",
        	1,
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
			('GaussBastankhah', 'GaussGe','Park','Modified_Park'))
			if option=="GaussGe":
				wakemodel=wake.gauss_ge
			if option=="GaussBastankhah":
				wakemodel=wake.guass_Bastankhah
			if option=="Park":
				wakemodel=wake.Park		
			if option=="Modified_Park":
				wakemodel=wake.Modified_Park			
		with tab2:
			genre = st.radio(
			"类型选择",
			('固定值', '性能曲线'))
			if genre=="固定值":
				form = st.form(key="form_configure")
				ct = form.text_input(
				"推力系数",
				0.7,
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
				dataframe_pos.columns=["X","Y","D"]
				st.session_state["x"]=list(dataframe_pos.X)
				st.session_state["y"]=list(dataframe_pos.Y)
				st.session_state["d"]=list(dataframe_pos.D)
			if st.button("增加机位"):
				add()
			else:
				pass
			df = pd.DataFrame({"X": st.session_state["x"], "Y": st.session_state["y"],"D": st.session_state["d"]})
			gb = GridOptionsBuilder.from_dataframe(df)
			selection_mode = 'single' # 定义单选模式，多选为'multiple'
			enable_enterprise_modules = True 
			gb.configure_selection(selection_mode, use_checkbox=True) # 定义use_checkbox
			gb.configure_side_bar()
			gb.configure_grid_options(domLayout='normal')
			gb.configure_pagination(paginationAutoPageSize=True)
			gridOptions = gb.build()
			grid_return = AgGrid(df, grid_options,theme="streamlit")
			new_df = grid_return["data"]
			st.session_state["df"]=new_df

def Creat(nx,ny,dx,dy,velocity,direction,turbine_sites,D,ct,wakemodel):

	flowfield=Flowfield(velocity,nx,ny,dx,dy)
	#flowfield.change_flow([10,20],[50,30],[11,11])
	mesh=Mesh(nx,ny,dx,dy)
	radio=nx/ny
	figsize=(8.2, 7/radio) if radio>=1 else (4.5*radio,4)
	wind_farm(flowfield,mesh,turbine_sites,direction,D,ct,wakemodel)
	fig, ax = plt.subplots(figsize=figsize)
	cb=ax.contourf(mesh.x,mesh.y,flowfield.flow,levels=50,cmap="Spectral")
	ax.set_xlim([mesh.x.min(),mesh.x.max()])
	ax.set_ylim([mesh.y.min(),mesh.y.max()])
	fig.colorbar(cb,pad=0.01)
	plt.rcParams.update(config)
	return fig

def Creat_powercurver(nx,ny,dx,dy,velocity,direction,turbine_sites,D,wtg_file,wakemodel):
	flowfield=Flowfield(velocity,nx,ny,dx,dy)
	#flowfield.change_flow([10,20],[50,30],[11,11])
	mesh=Mesh(nx,ny,dx,dy)
	radio=nx/ny
	figsize=(8.2, 7/radio) if radio>=1 else (4.5*radio,4)
	u_storge,p_storge,ct_storge=wind_farm_powercurver(flowfield,mesh,turbine_sites,direction,D,wtg_file,wakemodel)
	fig, ax = plt.subplots(figsize=figsize)
	cb=ax.contourf(mesh.x,mesh.y,flowfield.flow,levels=50,cmap="Spectral")
	ax.set_xlim([mesh.x.min(),mesh.x.max()])
	ax.set_ylim([mesh.y.min(),mesh.y.max()])
	fig.colorbar(cb,pad=0.01)
	plt.rcParams.update(config)
	return fig,u_storge,p_storge,ct_storge

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
turbine_sites=list(zip(list(new_df_.X),list(new_df_.Y)))

Ds=list(new_df_.D)
D=list(map(lambda x: float(x),Ds))
nx=int(nx)
ny=int(ny)
dx=float(dx)
dy=float(dy)

if optionflow=="单风速/风向":
	velocity=float(vel)
	direction=float(direction)
	if genre=="固定值":
		ct=float(ct)
		fig=Creat(nx,ny,dx,dy,velocity,direction,turbine_sites,D,ct,wakemodel)
	else:
		fig,ustorge,pstorge,ctstorge=Creat_powercurver(nx,ny,dx,dy,velocity,direction,turbine_sites,D,power_curver,wakemodel)
	#vert_space = '<div style="margin: 0 1000px 100px 100px;"></div>'
	#st.markdown(vert_space, unsafe_allow_html=True)
	st.pyplot(fig,use_container_width=False)

	if option not in ["Modified_Park","Park"]:
		options = st.multiselect(
    		'显示所选位置的尾流廓线',
    		['0.5D', '1D', '2D', '3D','4D','5D', '6D', '8D','10D','12D', '14D', '16D','20D'],
    		['1D', '2D','4D','6D','8D'])
		turbine_id=st.selectbox(
			'选择显示的风力机编号',
			tuple(range(len(turbine_sites)))
		)
		display_pos=list(map(lambda x: float(x[:-1])*D[turbine_id],options))
		display_pos.sort()
		r=np.linspace(-2*D[turbine_id],2*D[turbine_id],100)
		figc, axc = plt.subplots(figsize=(5,2))	
		axc.set_ylabel("速度亏损",fontsize=8)
		#plt.rcParams.update(config)
		if genre=="固定值":
			for xi in display_pos:
				axc.plot(r,wakemodel(np.array(xi),r,velocity,D[turbine_id],ct),label=xi/D[turbine_id])
			plt.legend()
		else:
			for xi in display_pos:
				axc.plot(r,wakemodel(np.array(xi),r,ustorge[turbine_id],D[turbine_id],ctstorge[turbine_id]),label=xi/D[turbine_id])
			plt.legend(prop = {'size':4})			
		st.pyplot(figc,use_container_width=True)
else:
	if uploaded_series is not None:
		series=pd.read_csv(uploaded_series,header=None)
		series.columns=["Time","U","DIR"]
		series.index=series.Time
		if genre=="固定值":
			if 'ind' not in st.session_state:
				st.session_state["ind"]=list(series.index)[0]
			ct=float(ct)
			fig=Creat(nx,ny,dx,dy,series.U[st.session_state["ind"]],series.DIR[st.session_state["ind"]],turbine_sites,D,ct,wakemodel)
			st.pyplot(fig,use_container_width=False)
			st.session_state["ind"] = st.select_slider(
				'Select time',
				options=list(series.index))			
		else:
			if 'ind' not in st.session_state:
				st.session_state["ind"]=list(series.index)[0]
			fig,_,_,_=Creat_powercurver(nx,ny,dx,dy,series.U[st.session_state["ind"]],series.DIR[st.session_state["ind"]],turbine_sites,D,power_curver,wakemodel)
			st.pyplot(fig,use_container_width=False)	
			st.session_state["ind"]= st.select_slider(
				'Select time',
				options=list(series.index))
			u_storge_all,p_storge_all,ct_storge_all=[],[],[]
			for i in list(series.index):
				u_storge,p_storge,ct_storge=Creat_powercurver_showpower(nx,ny,dx,dy,series.U[i],series.DIR[i],turbine_sites,D,power_curver,wakemodel)
				u_storge_all.append(u_storge)
				p_storge_all.append(p_storge)
				ct_storge_all.append(ct_storge)
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
				x1 = np.array(series.index)
				y1 = np.array(pd.DataFrame(u_storge_all).iloc[:,turbine_id])
				fig_plot1, ax1 = plt.subplots(figsize=(6,1.5))
				ax1.plot(x1,y1,color='green', marker='o')	
				ax1.set_xlabel("速度时间序列")
				ax1.grid(ls = '-.', lw = 0.25)		
				st.pyplot(fig_plot1,use_container_width=True)
			with cole:
				x2 = np.array(series.index)
				y2 = np.array(pd.DataFrame(p_storge_all).iloc[:,turbine_id])
				fig_plot2, ax2 = plt.subplots(figsize=(6,1.5))
				ax2.plot(x2,y2,color='#ad4545', marker='.')	
				ax2.set_xlabel("功率时间序列")	
				ax2.grid(ls = '-.', lw = 0.25)		
				st.pyplot(fig_plot2,use_container_width=True)
			
			#st.write(pd.DataFrame(u_storge_all))
			#st.write(np.array(series.index),np.array(u_storge_all))


