# _*_ coding:utf-8 _*_

"""
@date: 20170622
@author: 李天琦
"""

from math import ceil

def bw_to_pir(bw):
    """
    带宽数到pir值的转换

    参数: 
        带宽值, 单位(M)
    返回: 
        pir值(E, M组成的4位16进制)

    例如: 输入8, 返回0x13e8  (8M)
    """
    for e in range(16):
        m = ceil((float(bw) * (10**6)) / (4000 * (2**e)))
        if m < 1024:
            return hex(e) + '0'*(5-len(hex(m))) + hex(m)[2:]

    return "error: out of range"


# 测试转换结果
if __name__ == "__main__":
    bw = input('Please input bandwith (M):')
    print(bw_to_pir(float(bw)))
