#!/usr/bin/env python3
# coding=utf-8
"""
@date: 20170822
@author: 李天琦
@update: 
"""

import os

def get_path(key):
    """
    以调用此方法的文件为参照，获取某一绝对路径

    参数：
        key: 指定相对目录级别
             key=1: 文件绝对路径（带文件名）
			 key=2: 文件所在文件夹路径
			 key=3: 再上一级目录
    输出:
	    所需路径
    """ 
	
    path = os.path.realpath(__file__)    # 本文件绝对路径

    father_path = os.path.abspath(os.path.dirname(path)+os.path.sep+".")

    grader_father = os.path.abspath(os.path.dirname(path)+os.path.sep+"..")    # 上两级目录

    if key == 1:
        return path
    elif key == 2:
        return father_path
    elif key == 3:
        return grader_father
    else:
        print("get_path error!!!")
        return '/'


if __name__ == "__main__":
    key = input("input mode: (1,2,3)")
    path = get_path(int(key))
    print(path)