#!/usr/bin/python3
#coding:utf-8
import serial
import time
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
    try:
        serial_port.write(send_str.encode('utf-8'))
    except:
        print ('serial send fail')

def serial_init():
    try:
        serial_port = serial.Serial("/dev/ttyACM0",115200,timeout=5)
        #print(type(serial_port))  #<class 'serial.serialposix.Serial'>
        ret_list = [True, serial_port]
    except:
        ret_list = [False]
    return ret_list
    
    
def serial_reset():
    ret_list = serial_init()
    if ret_list[0] == True:
        print('serial open ok!')
        serial_port = ret_list[1]
        serial_send(serial_port,'stop\n')
        time.sleep(0.1)
        #serial_host.serial_send(serial_port,'start record\n')
        #time.sleep(5)
        #serial_host.serial_send(serial_port,'stop\n')
        serial_port.close()
    else:
        print('serial open fail！')  


def serial_send_cmd(cmd_str):
    ret_list = serial_init()
    if ret_list[0] == True:
        print('serial open ok!')
        serial_port = ret_list[1]
        serial_send(serial_port, cmd_str)
        time.sleep(0.1)
        serial_port.close()
    else:
        print('serial open fail！')

