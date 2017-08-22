#!/usr/bin/env python3
# coding=utf-8
"""
@date: 20170822
@author: 李天琦
@update: 
"""

from deploy_qos import deploy_qos
import os
from bw_modify.sh_pir_csv_modify import pir_csv_modify
from bw_modify.get_path import get_path
from generate_policy.generate_policy import generate_policy

#qos_list = []

def page_home():
    """
    显示第一页，策略列表和选项提示：新增，选择
    """
    os.system('clear')
    print()
    print("=" * 28 + "首页" + "=" * 28)
    print()
    print("可选择的QoS策略如下：        ")
    qos_list = []
    qos_list = deploy_qos.show_qos_policy()
    print()
    print("=" * 60)
    print("-" * 33)
    print("| -> 输入 [C] 进入策略选择界面  |        ")
    print("| -> 输入 [N] 进入新增策略界面  |        ")
    print("| -> 输入 [Q] 退出              |        ")
    print("-" * 33)
    
    while True:
        key = input("请选择操作(C/N/Q):        \n")
        if key == 'c' or key == 'C':
            page_choose()
            break
        elif key == 'n' or key == 'N':
            page_new()
            #print("new_page")
            break
        elif key == 'q' or key == 'Q':
            break
        else:
            print("选择错误!  ")

            
    # return qos_list


def page_choose():
    """
    显示列表和提示：输入序号选择
    """

    os.system('clear')
    print()
    print("=" * 26 + "选择策略" + "=" * 26)
    print()
    print("可选择的QoS策略如下：        ")
    qos_list = []
    qos_list = deploy_qos.show_qos_policy()
    print()
    print("=" * 60)
    print("--------------------------------        ")
    print("| -> 输入 [序号] 选择对应策略  |        ")
    print("| -> 输入 [H]    返回首页      |        ")
    print("| -> 输入 [Q]    退出          |        ")
    print("--------------------------------        ")
	
    while True:
        key = input("请选择操作:        \n")
        if key == 'h' or key == 'H':
            page_home()
            break
        elif key == 'q' or key == 'Q':
            break
        elif int(key) > 0 and int(key) <= len(qos_list):
            page_operate(key, qos_list)
            break
        else:
            print("选择错误！  ")
		
		
def page_operate(key, qos_list):
    """
    操作策略的界面：部署，修改，删除（未实现）
    """
    os.system('clear')
    print()
    print("=" * 26 + "策略操作" + "=" * 26)
    print()
    print("你选择了" + "[" + key + "] " + qos_list[int(key) - 1])
    print()
    print("=" * 60)
    print("-------------------------        ")
    print("| -> 输入 [D] 部署策略  |        ")
    print("| -> 输入 [M] 修改策略  |        ")
    print("| -> 输入 [R] 返回上页  |        ")
    print("| -> 输入 [H] 返回首页  |        ")
    print("| -> 输入 [Q] 退出      |        ")
    print("-------------------------        ")
	
    while True:
        key1 = input("请选择操作:        \n")
        if key1 == 'r' or key1 == 'R':
            page_choose()
            break
        elif key1 == 'h' or key1 == 'H':
            page_home()
            break
        elif key1 == 'q' or key1 == 'Q':
            break
        elif key1 == 'd' or key1 == 'D':
            page_deploy(key, qos_list)
            break
        elif key1 == 'm' or 'M':
            print(key)
            page_modify(key, qos_list)
            #print("modify page")
            break
        else:
            print("选择错误！  ")
			

def page_modify(key, qos_list):
    """
    修改策略界面：基于选定的策略做修改
    """
    os.system('clear')
    print()
    print("=" * 26 + "修改策略" + "=" * 26)
    print()
    print("基于" + "[" + key + "] " + qos_list[int(key) - 1] + "修改...        ")
    print()
    print("=" * 60)
	
    print("请编辑要修改的带宽值...        ")
    print("- 编辑格式为<shaper id,bandwidth>        \n- 一个id占一行        \n- id范围0-3999        ")
    print("注：编辑窗口为vim，使用方法请自行学习        ")
    input("按 [enter] 开始编辑...        ")
    os.system(get_path(3) + "/script/edit_bw_csv.sh")

    #print(key)
    #print(pir_file)
    pir_file = get_path(3) + "/qos_policy/" + qos_list[int(key) - 1] + "/sh_pir.csv"

    pir_csv_modify(bw_csv = get_path(3) + "/test_data/bandwidth.csv", ref_csv = pir_file)
	
    print("生成策略文件...            ")
    qos_name = input("输入要保存的策略名称(不要用中文):                \n")
    generate_policy(qos_name)
	
    os.system('clear')
    print()
    print("=" * 26 + "修改策略" + "=" * 26)
    print()
    print("修改成功！    ")	
    print("=" * 60)
	
    print("---------------------------------        ")
    print("| -> 输入 [C] 进入策略选择界面  |        ")
    print("| -> 输入 [H] 返回首页          |        ")
    print("| -> 输入 [Q] 退出              |        ")
    print("---------------------------------        ")
	
    while True:
        key = input("请选择操作:        \n")
        if key == 'c' or key == 'C':
            page_choose()
            break
        elif key == 'h' or key == 'H':
            page_home()
            break
        elif key == 'q' or key == 'Q':
            break
        else:
            print("选择错误！  ")
	

	
			
			
def page_deploy(key, qos_list):
    """
    策略部署界面：测试功能可查看id对应pir值（不是带宽）
    """
    os.system('clear')
    print()
    print("=" * 26 + "策略部署" + "=" * 26)
    print()
    print("成功部署" + "[" + key + "] " + qos_list[int(key) - 1])
    print()
    print("=" * 60)
    print("---------------------------------        ")
    print("| -> 输入 [F] 查看对应shaper值  |        ")
    print("| -> 输入 [C] 进入策略选择界面  |        ")
    print("| -> 输入 [R] 返回上页          |        ")
    print("| -> 输入 [H] 返回首页          |        ")
    print("| -> 输入 [Q] 退出              |        ")
    print("---------------------------------        ")
	
    while True:
        key1 = input("请选择操作:        \n")
        if key1 == 'r' or key1 == 'R':
            page_operate(key, qos_list)
            break
        elif key1 == 'h' or key1 == 'H':
            page_home()
            break
        elif key1 == 'q' or key1 == 'Q':
            break
        elif key1 == 'c' or key1 == 'C':
            page_choose()
            break
        elif key1 == 'f' or key1 == 'F':
            deploy_qos.deploy(qos_list[int(key) - 1])
            os.system('clear')
            print()
            print("=" * 26 + "策略部署" + "=" * 26)
            print()
            print("成功部署" + "[" + key + "] " + qos_list[int(key) - 1])
            print()
            print("=" * 60)
            print("---------------------------------        ")
            print("| -> 输入 [F] 查看对应shaper值  |        ")
            print("| -> 输入 [C] 进入策略选择界面  |        ")
            print("| -> 输入 [R] 返回上页          |        ")
            print("| -> 输入 [H] 返回首页          |        ")
            print("| -> 输入 [Q] 退出              |        ")
            print("---------------------------------        ")
            #break
        else:
            print("选择错误！  ")
			
			
def page_new():
    """
    新建策略界面：从头建，基于已有修改
    """
    os.system('clear')
    print()
    print("=" * 26 + "新增策略" + "=" * 26)
    print()
    #print("=" * 60)
    print("---------------------------------        ")
    print("| -> 输入 [A] 从头新建策略      |        ")
    print("| -> 输入 [B] 基于已有策略修改  |        ")
    print("| -> 输入 [H] 返回首页          |        ")
    print("| -> 输入 [Q] 退出              |        ")
    print("---------------------------------        ")
	
    while True:
        key = input("请选择操作:        \n")
        if key == 'a' or key == 'A':
            new_from_blank()
            break
        elif key == 'b' or key == 'B':
            new_from_old()
            break
        elif key == 'h' or key == 'H':
            page_home()
            break
        elif key == 'q' or 'Q':
            break
        else:
            print("选择错误！  ")
			
			
def new_from_blank():
    """
    从头开始建新策略
    """
    os.system('clear')
    print()
    print("=" * 26 + "新增策略" + "=" * 26)
    print()
    bw = input("输入默认通用带宽值(默认为0)[单位: M]:        \n")
    if bw == '':
        def_bw = 0
    else:
        def_bw = int(bw)

    print("默认带宽为: " + str(def_bw))
	
    print("请编辑其他要修改的带宽值...        ")
    print("- 编辑格式为<shaper id,bandwidth>        \n- 一个id占一行        \n- id范围0-3999        ")
    print("注：编辑窗口为vim，使用方法请自行学习        ")
    while True:
        key = input("按 [enter] 跳过编辑，不设置其他值，输入 [y] 开始编辑...        ")
        if key == '':
            bw_csv = None
            break
        elif key == 'y' or key == 'Y':
            os.system(get_path(3) + "/script/edit_bw_csv.sh")
            bw_csv = get_path(3) + "/test_data/bandwidth.csv"
            break
        else:
            print("输入错误！        ")
			
    pir_csv_modify(def_bw = def_bw, bw_csv = bw_csv)
	
    print("生成策略文件...        ")
    qos_name = input("输入要保存的策略名称(不要用中文):                \n")
    generate_policy(qos_name)
	
    #input()
    os.system('clear')
    print()
    print("=" * 26 + "新增策略" + "=" * 26)
    print()
    print("新增成功！    ")	
    print("=" * 60)
    print("---------------------------------        ")
    print("| -> 输入 [C] 进入策略选择界面  |        ")
    print("| -> 输入 [H] 返回首页          |        ")
    print("| -> 输入 [Q] 退出              |        ")
    print("---------------------------------        ")
	
    while True:
        key = input("请选择操作:        \n")
        if key == 'c' or key == 'C':
            page_choose()
            break
        elif key == 'h' or key == 'H':
            page_home()
            break
        elif key == 'q' or key == 'Q':
            break
        else:
            print("选择错误！  ")
			
			
def new_from_old():
    """
    基于已有策略修改
    """
    os.system('clear')
    print()
    print("=" * 26 + "新增策略" + "=" * 26)
    print()
    print("选择要基于的策略    ")
    qos_list = []
    qos_list = deploy_qos.show_qos_policy()
    print()
    print("=" * 60)
    print("--------------------------------        ")
    print("| -> 输入 [序号] 选择策略      |        ")
    print("| -> 输入 [H]    返回首页      |        ")
    print("| -> 输入 [Q]    退出          |        ")
    print("--------------------------------        ")
	
    while True:
        key = input("请选择操作:        \n")
        if key == 'h' or key == 'H':
            page_home()
            break
        elif key == 'q' or key == 'Q':
            break
        elif int(key) > 0 and int(key) <= len(qos_list):
            pir_file = get_path(3) + "/qos_policy/" + qos_list[int(key) - 1] + "/sh_pir.csv"
            break
        else:
            print("选择错误！  ")
			
    os.system('clear')
    print()
    print("=" * 26 + "新增策略" + "=" * 26)
    print()
    print("基于" + "[" + key + "] " + qos_list[int(key) - 1] + "修改...    ")
			
    print("请编辑要修改的带宽值...        ")
    print("- 编辑格式为<shaper id,bandwidth>        \n- 一个id占一行        \n- id范围0-3999        ")
    print("注：编辑窗口为vim，使用方法请自行学习        ")
    key = input("按 [enter] 开始编辑...        ")
    os.system(get_path(3) + "/script/edit_bw_csv.sh")
	
    pir_csv_modify(bw_csv = get_path(3) + "/test_data/bandwidth.csv", ref_csv = pir_file)
	
    print("生成策略文件...        ")
    qos_name = input("输入要保存的策略名称(不要用中文):                \n")
    generate_policy(qos_name)
	
    os.system('clear')
    print()
    print("=" * 26 + "新增策略" + "=" * 26)
    print()
    print("新增成功！    ")	
    print("=" * 60)
    print("---------------------------------        ")
    print("| -> 输入 [C] 进入策略选择界面  |        ")
    print("| -> 输入 [H] 返回首页          |        ")
    print("| -> 输入 [Q] 退出              |        ")
    print("---------------------------------        ")
	
    while True:
        key = input("请选择操作:        \n")
        if key == 'c' or key == 'C':
            page_choose()
            break
        elif key == 'h' or key == 'H':
            page_home()
            break
        elif key == 'q' or key == 'Q':
            break
        else:
            print("选择错误！  ")
        #break
        #else:
            #print("选择错误！  ")
			
			
			
    
    #print("成功部署" + "[" + key + "] " + qos_list[int(key) - 1])
    #print()


if __name__ == "__main__":
    #qos = 
    page_home()
    #i = input("input num: ")
    #print(qos[int(i)-1])