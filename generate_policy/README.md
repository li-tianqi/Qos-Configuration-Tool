> /generate_policy目录  
# 生成QoS规则文件的功能
- 编译c文件
- 生成对应qos_name.out的规则文件
- 备份csv文件


---
[20170818]  

通过指定要保存的规则文件名（不必包括后缀），调用make.sh  
- 编译生成qos_policy目录下的规则文件
- 备份对应的sh_pir.csv文件


**正式应用时修改script/make.sh文件中的源文件路径即可**