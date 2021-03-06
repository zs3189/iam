# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/3/13 11:22
'''

##远程连接服务器
# 网络请求
# Add "sys.coinit_flags = 0" after your "import sys" line and
# before the "import pythoncom" line. That worked for me, although I don't know why.

import os, sys
import win32api

sys.coinit_flags = 0
import time
import wmi
import logging
from urllib import request
logger = logging.getLogger()  #返回根目录的logger
import requests



def web_request(url, data=None):
    import ssl, json
    ssl._create_default_https_context = ssl._create_unverified_context  # 关闭证书验证
    response = requests.get(url, timeout=5, params=data)
    print(response.text)
    if response.status_code == 404:
        result = {'result': 'wrong account'}
        return result
    else:
        result = response.content
        result = str(result, encoding='utf-8')
        result = json.loads(result)
        return result





def get_unique_id():
    c = wmi.WMI()
    try:
        for physical_disk in c.Win32_DiskDrive():
            # 硬盘序列号
            diskid = physical_disk.SerialNumber.strip()
            print ('disk id:', physical_disk.SerialNumber.strip())
            return diskid
    except:
        pass
    try:
        cpus = c.Win32_Processor()
        return cpus[0].ProcessorId
    except:
        pass
    ##计算机名 + mac地址
    try:
        mac = get_mac_address()
        cname = getname()
        return mac + cname
    except:
        return "wrong"

##获取MAC
import uuid
def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return mac


import ctypes
import os



def setSystemTime(remotetime):
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(remotetime)
    win32api.SetSystemTime(tm_year, tm_mon, tm_wday, tm_mday, tm_hour, tm_min, tm_sec, 0)



# 获取计算机名e
def getname():
    pcName = ctypes.c_char_p(''.encode('utf-8'))
    pcSize = 16
    pcName = ctypes.cast(pcName, ctypes.c_char_p)
    try:
        ctypes.windll.kernel32.GetComputerNameA(pcName, ctypes.byref(ctypes.c_int(pcSize)))
    except Exception:
        print("Sth wrong in getname!")
    return pcName.value.decode('utf-8')





def getip_dianxin(ip):
    ## http://ip.taobao.com/service/getIpInfo.php?ip=110.84.0.129
    url = "http://ip.taobao.com/service/getIpInfo.php?ip={0}".format(ip)
    result = web_request(url)
    '''
    {"code":0,"data":{"ip":"110.84.0.129","country":"中国","area":"",
    "region":"福建","city":"厦门","county":"XX","isp":"电信","country_id":"CN",
    "area_id":"","region_id":"350000","city_id":"350200","county_id":"xx","isp_id":"100017"}}
    '''
    from component.variable import set_val
    try:
        print(result)
        if result['data']['city'] == '上海' and result['data']['isp'] == '电信':
            set_val('guopai_dianxin', True)  ##当前是否处于国拍电信
            # print(result)
        else:
            set_val('guopai_dianxin', False)  ##当前是否处于国拍电信
    except:
        set_val('guopai_dianxin', False)  ##当前是否处于国拍电信

###################-----------------
# def get_cpu_info():
#     tmpdict = {}
#     tmpdict["CpuCores"] = 0
#     c = wmi.WMI()
#     #          print c.Win32_Processor().['ProcessorId']
#     #          print c.Win32_DiskDrive()
#     for cpu in c.Win32_Processor():
#         #                print cpu
#         print ("cpu id:", cpu.ProcessorId.strip())
#         tmpdict["CpuType"] = cpu.Name
#         try:
#             tmpdict["CpuCores"] = cpu.NumberOfCores
#         except:
#             tmpdict["CpuCores"] += 1
#             tmpdict["CpuClock"] = cpu.MaxClockSpeed
#             return tmpdict
#
#
# def _read_cpu_usage():
#     c = wmi.WMI()
#     for cpu in c.Win32_Processor():
#         return cpu.LoadPercentage
#
#
# def get_cpu_usage():
#     cpustr1 = _read_cpu_usage()
#     if not cpustr1:
#         return 0
#     time.sleep(2)
#     cpustr2 = _read_cpu_usage()
#     if not cpustr2:
#         return 0
#     cpuper = int(cpustr1) + int(cpustr2) / 2
#     return cpuper
#
#
# def get_disk_info():
#     tmplist = []
#     encrypt_str = ""
#     c = wmi.WMI()
#     for cpu in c.Win32_Processor():
#         # cpu 序列号
#         encrypt_str = encrypt_str + cpu.ProcessorId.strip()
#         print ("cpu id:", cpu.ProcessorId.strip())
#     for physical_disk in c.Win32_DiskDrive():
#         encrypt_str = encrypt_str + physical_disk.SerialNumber.strip()
#
#         # 硬盘序列号
#         print ('disk id:', physical_disk.SerialNumber.strip())
#         tmpdict = {}
#         tmpdict["Caption"] = physical_disk.Caption
#         tmpdict["Size"] = int(physical_disk.Size) / 1000 / 1000 / 1000
#         tmplist.append(tmpdict)
#     for board_id in c.Win32_BaseBoard():
#         # 主板序列号
#         encrypt_str = encrypt_str + board_id.SerialNumber.strip()
#         print ("main board id:", board_id.SerialNumber.strip())
#     #          for mac in c.Win32_NetworkAdapter():
#
#     # mac 地址（包括虚拟机的）
#     #                    print "mac addr:", mac.MACAddress:
#     for bios_id in c.Win32_BIOS():
#         # bios 序列号
#         encrypt_str = encrypt_str + bios_id.SerialNumber.strip()
#         print ("bios number:", bios_id.SerialNumber.strip())
#     print ("encrypt_str:", encrypt_str)
#
#     # 加密算法
#     # print (zlib.adler32(encrypt_str))
#     return encrypt_str
#
#
if __name__ == "__main__":
    #     a = get_cpu_info()
    # mac = get_mac_address()
    # cname = getname()
    # print ( mac + cname)
    setSystemTime(1111111111)