# _*_ coding:utf-8 _*_
"""
@date: 20170623
@author: 李天琦
"""

import csv

def csv_to_dict(filename):
    """
    读取两列的csv文件，转换为字典，第一列为key，第二列为value

    参数: 
        filename, csv文件路径
    输出:
        字典

    """

    data_dict = {}

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data_dict[line[0]] = float(line[1])

        return data_dict


if __name__ == "__main__":
    filename = input("please input csvfile name:\n")
    print("the dict is:\n",csv_to_dict(filename))
