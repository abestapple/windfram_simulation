# 风电场在线模拟计算程序 windfram_simulation
采用streamlit库实现了风电场计算程序的在线使用。
[使用地址](https://abestapple-windfram-simulation-app-snatpw.streamlit.app/)

## 已实现功能
1. 单风向/单风速数据下的风电场尾流计算。
2. 支持风电场机位点手动添加或者文件导入。
3. 支持输入风时间序列数据的加入。
4. 支持风力机功率曲线的用户自定义。
5. 支持风电场范围、分辨率的自定义。
6. 已加入基于Guass的尾流模型和Park等多种尾流模型。
  - Gauss_Bastankhah
  - guass_XA
  - GaussGe
  - Park
  - Modified_Park
  - Larsen
  - Frandsen
  - Bastankhah_yaw (paper:Experimental and theoretical study of wind turbine wakes in yawed conditions) 
  - QianIshihara (paper:Wind farm power maximization through wake steering with a new multiple wake model for prediction of turbulence intensity)
![结果](https://github.com/abestapple/windfram_simulation/blob/main/image/single_wake_velocity.png)
##注意！ 当计算偏航尾流时,请采用Bastankhah_yaw QianIshihara这两种尾流模型。
7. 偏转（偏航）尾流模型可供选择有：
  - Bastankhah_yaw (paper:Experimental and theoretical study of wind turbine wakes in yawed conditions)
  - Jimenez
  - Qian_Ishihara (paper:Wind farm power maximization through wake steering with a new multiple wake model for prediction of turbulence intensity)
![速度场结果](https://github.com/abestapple/windfram_simulation/blob/main/image/yaw_single_wake_velocity.png)
![湍流场结果](https://github.com/abestapple/windfram_simulation/blob/main/image/yaw_single_wake_ti.png)
8. 湍流模型：
  - Qian_Ishihara_turbulent_model (paper:Wind farm power maximization through wake steering with a new multiple wake model for prediction of turbulence intensity)
![结果](https://github.com/abestapple/windfram_simulation/blob/main/image/single_wake_ti.png)
9. 叠加模型有LinearSum和SquaredSum两种模型可供选择。
## 风场模拟： 
![风场模拟结果](https://github.com/abestapple/windfram_simulation/blob/main/image/windfarm_vel.png)
![风场模拟结果](https://github.com/abestapple/windfram_simulation/blob/main/image/windfarm_ti.png)
