#!/usr/bin/env python3
# coding=utf-8

"""
@date: 20170818
@author: 李天琦
@update: 
"""

import os

def generate_policy(policy_name = None):
    """
    Generate QoS policy with make.sh and backup the sh_pir.csv file

    Input: 
        policy_name: The specified policy name
    Output:
        policy file and corresponding csv file
    """
	
    path = os.path.realpath(__file__)    # 本文件绝对路径

    #father_path = os.path.abspath(os.path.dirname(path)+os.path.sep+".")
    grader_father = os.path.abspath(os.path.dirname(path)+os.path.sep+"..")    # 上两级目录
    make_sh_path = grader_father + "/script/make.sh"    # make.sh绝对路径



    print("call the make.sh script...")

    os.system(make_sh_path + " " +  policy_name)

    print("done")


if __name__ == "__main__":
    file_name = input("input the qos policy name that you want to save as:")
    generate_policy(file_name)
