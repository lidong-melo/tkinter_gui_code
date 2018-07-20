#!/usr/bin/python
#coding:utf-8

# https://www.cnblogs.com/kellyseeme/p/5525025.html
# https://www.cnblogs.com/xiao-apple36/p/8683198.html 实现了server 多线程
from socket import *
import json
import random
import time
  
HOST = '192.168.31.209'  
PORT = 60000

param2 = {'msg_type':'t2r', 'doa_angle':0} 

s = socket(AF_INET,SOCK_DGRAM)  
s.bind((HOST,PORT))  

while True:
    print ('...waiting for message..'  )
    data,address = s.recvfrom(1024)
    while True:
        sleep_time = random.uniform(0.5, 3)
        time.sleep(sleep_time)
        angle = random.randint(0,360)
        param2['doa_angle'] = angle
        json_string = json.dumps(param2)
        s.sendto(json_string.encode(), address)
        try:
            s.sendto(json_string.encode(), address)
            print ('send', json_string)
        except:
            break
s.close()
