#!/usr/bin/python
#coding:utf-8

# https://www.cnblogs.com/kellyseeme/p/5525025.html
# https://www.cnblogs.com/xiao-apple36/p/8683198.html 实现了server 多线程
from socket import *
import json
import random
import time
import _thread
  
HOST = '192.168.31.209'  
PORT = 60000
address_list = ['192.168.31.209', 10000]
param2 = {'msg_type':'t2r', 'doa_angle':0} 


def thread_udp_recv():
    while True:
        print ('...waiting for message..'  )
        try:
            data,address_recv = s.recvfrom(1024)
            print('recv',address_recv)
            address_list.clear()
            address_list_temp = list(address_recv)
            address_list.append(address_list_temp[0])
            address_list.append(address_list_temp[1])
            print('recv',address_list)
            
        except:
            pass


s = socket(AF_INET,SOCK_DGRAM)  
s.bind((HOST,PORT))
_thread.start_new_thread(thread_udp_recv, ())


while True:

    sleep_time = random.uniform(0.5, 3)
    time.sleep(sleep_time)
    angle = random.randint(0,360)
    param2['doa_angle'] = angle
    json_string = json.dumps(param2)
    address_tuple = tuple(address_list)
    try:
        s.sendto(json_string.encode(), address_tuple)
        print('send', address_tuple, json_string)
    except:
        print('disconnect')
s.close()
