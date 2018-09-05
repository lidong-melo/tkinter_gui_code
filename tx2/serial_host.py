#!/usr/bin/python3
#coding:utf-8
import serial
#import time
#import re
#import _thread

            
def serial_recv(serial_port):
    while True:
        line = serial_port.readline()
        try:
            print(line.decode('utf-8'),end='')
        except:
            pass
        # if ( re.search(b'can not recognize!',line)):
            # print ('----------------A113 can not recognize')#error 1
            # sendAT_Cmd(ser,'start record\r')
        # elif ( re.search(b'Device or resource busy',line)):
            # print ('----------------A113 busy')#error 1
            # sendAT_Cmd(ser,'stop\r')
 
def serial_send(serial_port, send_str):
    serial_port.write(send_str.encode('utf-8'))

def serial_init():
    serial_port = serial.Serial("/dev/ttyACM0",115200,timeout=5)
    #serial_port = serial.Serial("COM11",115200,timeout=5)
    print(type(serial_port)) #<class 'serial.serialwin32.Serial'>  #<class 'serial.serialposix.Serial'>
    return serial_port

    
#hi = serial_init()
#ser = serial.Serial("/dev/ttyACM0",115200,timeout=5)
#_thread.start_new_thread(serial_recv, (serial_port,))
#time.sleep(1)
#serial_send(serial_port,'\r')#避免开机乱码导致第一条命令接收不到
#time.sleep(1)

#while 1:
    # print('-----send start record')
    # sendAT_Cmd(ser,'start record\r')
    # time.sleep(10)
    # print('-----send stop')
    # sendAT_Cmd(ser,'stop\r')
    # time.sleep(10)    
    # pass
