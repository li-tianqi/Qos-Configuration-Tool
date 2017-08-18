#!/usr/bin/env python3
# coding=utf-8

"""
@date: 20170818
@author: 李天琦
@update: 
"""

import os

path = os.path.realpath(__file__)    # 本文件绝对路径
#father_path = os.path.abspath(os.path.dirname(path)+os.path.sep+".")
grader_father = os.path.abspath(os.path.dirname(path)+os.path.sep+"..")  # 上两级目录
qos_policy_path = grader_father + "/qos_policy/"    # 绝对路径

deploy_sh_path = grader_father + "/script/deploy_qos.sh"
# print(qos_policy_path)
policy_list = []

def show_qos_policy():
    print("you can choose policy as follow:")
    for i in os.listdir(qos_policy_path):
        #print(i)
        if os.path.isdir(qos_policy_path + i):
            policy_list.append(i)
            print(i)

def deploy(qos_name = None):
    print("call deploy_qos.sh script...")
    os.system(qos_policy_path + " " + qos_name)
    print("done")


if __name__ == "__main__":
    show_qos_policy()
    while True:
        qos = input("choose policy:")
        if qos in policy_list:
            deploy(qos)
            break


