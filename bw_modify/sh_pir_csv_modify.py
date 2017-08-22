# _*_ coding:utf-8 _*_
"""
@date: 20170622
@author: 李天琦
@update: 20170817
"""

import os
import csv
from bw_to_pir import bw_to_pir
from csv_to_dict import csv_to_dict
import shutil
from get_path import get_path


N = 4000    # 修改这个值后要将csv文件删除，否则文件行数不会更新
#path = os.path.realpath(__file__)    # 本文件绝对路径

#father_path = os.path.abspath(os.path.dirname(path)+os.path.sep+".")
#grader_father = os.path.abspath(os.path.dirname(path)+os.path.sep+"..")    # 上两级目录
#sh_pir = "../data/sh_pir.csv"
sh_pir = get_path(3) + "/data/sh_pir.csv"    # sh_pir.csv绝对路径

temp_csv = get_path(3) + "/data/temp/temp.csv"    # 临时文件绝对路径

def pir_csv_modify(def_bw = None, spec_bw = None, bw_csv = None, ref_csv = sh_pir):
    """
    修改sh_pir.csv文件

    参数：
        def_bw: 默认带宽值，对应大多数的一样的带宽值，不传此参数时，不对pir整体修改
        spec_bw: 指定特定的带宽值，字典类型，{"shaper编号（取0-4000）", 带宽值}
        bw_csv: 可指定包含带宽值的csv文件，格式为两列，第一列为shaper id，第二列为带宽值(M)
        ref_csv: 指定的修改参考文件，比如可用于指定参考当前使用中的规则，即读取当前规则的pir进行修改
    输出: 
        csv文件
    """

    print("ready to modify...")

    # 如果csv文件不存在，创建一个全0的初始文件（这里是指data目录中的）
    if not os.path.exists(sh_pir):
        print("no sh_pir.csv, creating a new file...")

        with open(sh_pir, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for i in range(N):
                writer.writerow(['0x0000'])
                
            print("successfully created!")

    def modify_with_def(def_bw, pir):
        """
        用默认值修改
        """
        def_pir = bw_to_pir(def_bw)
        for i in range(N):
            pir[i] = [def_pir]


    def modify_with_spec(spec_bw, pir):
        """
        用指定值修改
        """
        for i in spec_bw:
            print("modifying pir" + i + "...")
            spec_pir = bw_to_pir(spec_bw[i])
            pir[int(i)] = [spec_pir]


    def modify_with_file(bw_csv, pir):
        """
        用csv文件修改
        """
        # 转换csv到dict
        bw_dict = csv_to_dict(bw_csv)
        # 调用指定带宽模式
        modify_with_spec(bw_dict, pir)



    # 对csv文件修改
    print("opening ref_csv...")


    pir = []

    # 这里读取的应该是指定的参考csv文件
    with open(ref_csv, 'r') as csvfile:
        print("successfully opened!")

        reader = csv.reader(csvfile)
        #writer = csv.writer(csvfile)

        print("reading pir...")

        
        # 读取pir值到数组
        for line in reader:
            pir.append(line)
        
        print("successfully read!")

	# 如果传入def_bw值，对所有pir值更新
    if def_bw != None:
        print("modifying default pir...")
        modify_with_def(def_bw, pir)
        print("done!")

    # 如果传入指定带宽，对相应pir值修改
    if spec_bw != None:
        print("modifying specified pir...")
        modify_with_spec(spec_bw, pir)
        print("done!")

    # 如果传入带宽文件，根据文件进行修改
    if bw_csv != None:
        print("modifying with " + bw_csv + '...')
        modify_with_file(bw_csv, pir)
        print("done!")

    with open(temp_csv, 'w') as tempfile:
        writer = csv.writer(tempfile)
        # 写入临时csv文件
        print("writing temp csv file..")
        for row in pir:
            writer.writerow(row)

        print("successfully writed!")

    # 临时文件覆盖原始文件
    print("overwriting original file...")
    os.remove(sh_pir)
    #os.rename(temp_csv, sh_pir)
    shutil.move(temp_csv, sh_pir)
    print("successfully overwrited!")

    print("completed!")


# 测试几种工作方式
if __name__ == "__main__":
    #print(sh_pir)
    #print(path)

    print("please select the mode:\n1.modify default bandwith only.\n2.modify specified bandwith only.\n3.modify both.\n4.modify with file.\n5.test ref_csv.")
    mode = input()
    if mode == '1':
        def_bw = input("please input default bandwith:")
        pir_csv_modify(def_bw = def_bw)
    elif mode == '2':
        spec_bw = input("please input specified bandwith:")
        pir_csv_modify(spec_bw = eval(spec_bw))
    elif mode == '3':
        def_bw = input("please input default bandwith:")
        spec_bw = input("please input specified bandwith:")
        pir_csv_modify(def_bw = def_bw, spec_bw = eval(spec_bw))
    elif mode == '4':
        filename = input("please input file name:")
        pir_csv_modify(bw_csv = filename)
    elif mode == '5':
        ref_csv = input("please input ref_csv:")
        filename = input("please input bandwidth file name:")
        pir_csv_modify(bw_csv = filename, ref_csv = ref_csv)
    else:
        print("error mode!")


