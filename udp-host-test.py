#!/usr/bin/python
#coding:utf-8

# https://www.cnblogs.com/kellyseeme/p/5525025.html
# https://www.cnblogs.com/xiao-apple36/p/8683198.html 实现了server 多线程
from socket import *  
  
HOST = '10.0.5.2'  
PORT = 9999  
  
s = socket(AF_INET,SOCK_DGRAM)  
s.bind((HOST,PORT))  
print '...waiting for message..'  
while True:  
    data,address = s.recvfrom(1024)  
    print data,address  
    s.sendto('this is the UDP server',address)  
s.close()



# from socket import *  
  
# HOST='192.168.31.69'  
# PORT=9999  
  
# s = socket(AF_INET,SOCK_DGRAM)  
# s.connect((HOST,PORT))  
# while True:  
    # message = raw_input('send message:>>')  
    # s.sendall(message)  
    # data = s.recv(1024)  
    # print data  
# s.close()  


