import json
from netmiko import Netmiko
from multiprocessing.dummy import Pool as ThreadPool
import time
import ttp

f_2 = open("multiple_device_list_huawei.txt","r")
multiple_device_list = f_2.readlines()

f_3 = open("Syslog_Basarisiz_baglanti.txt","a")

with open("user_pass.txt", "r") as f5:
    user_pass = f5.readlines()

for list_user_pass in user_pass:
    if "username" in list_user_pass:
        username = list_user_pass.split(":")[1].strip()
    if "password" in list_user_pass:
        password = list_user_pass.split(":")[1].strip()

file1 = open("Syslog_Huawei_OK.txt", "a")

def _ssh_(nodeip):

    try:
        huawei = {
            'device_type': 'huawei', 'ip': nodeip, 'username':
            username, 'password': password, 'secret':password, "conn_timeout": 20}
        huawei_connect = Netmiko(**huawei)
        print(nodeip.strip() + "  " + "is reachable")
    except Exception as e:
        print (e)
        f_3.write(nodeip.strip() + "\n")
        return

    prompt_huawei_fnk = huawei_connect.find_prompt()
    hostname_fnk = prompt_huawei_fnk.strip("<" + ">")
    print(hostname_fnk)
    huawei_connect.send_command_timing("sys")
    print("entered config mode")
    huawei_connect.send_command_timing("info-center loghost 192.168.0.X")
    huawei_connect.send_command_timing("quit")

    data_to_parse = huawei_connect.send_command_timing('display current-configuration | inc 192.168.0.X')
    output = ''.join(data_to_parse)
    output2 = output.splitlines()
    output3 = ''.join(output2)
    output4 = output3.split(" ")
    if "10.222.246.12" in output4:
        print("config done")
        file1.write(nodeip + "\n")
    else:
        print(nodeip + "config:nok")

    huawei_connect.send_command_timing("save")
    huawei_connect.send_command_timing("yes")
    huawei_connect.disconnect()

myPool = ThreadPool(200)
result1 = myPool.map(_ssh_,multiple_device_list)


