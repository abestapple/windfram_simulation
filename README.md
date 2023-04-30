# 风电场在线模拟计算程序 windfram_simulation
采用streamlit库实现了风电场计算程序的在线使用。
[地址](https://abestapple-windfram-simulation-app-snatpw.streamlit.app/)

## 已实现功能
1. 单风向/单风速数据下的风电场尾流计算。
2. 支持风电场机位点手动添加或者文件导入。
3. 支持输入风时间序列数据的加入。
4. 支持风力机功率曲线的用户自定义。
5. 支持风电场范围、分辨率的自定义。
6. 已加入基于Guass的尾流模型和Park等四种尾流模型，后续计划加入更多的尾流模型可供选择。
## 注意： 
1. 对于叠加尾流模型，此程序默认采用了线性尾流叠加模型，其他叠加模型不可选择。
2. 多核并行计算是未来考虑加入的功能。
![风场模拟结果](https://github.com/abestapple/windfram_simulation/blob/main/simulation_result.png)
