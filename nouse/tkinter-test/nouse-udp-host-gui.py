#!/usr/bin/python
#coding:utf-8


from tkinter import Button, Label
import platform
from socket import *
import _thread
import random
import time
import json

## global variable
global_var = {'meeting_status':False, 'old_time':0, 'new_time':0, 'time_str':'00:00:00', 'angle':0}
server = {'IP':'192.168.31.209', 'PORT':60000}
key_word = {'doa':'doa'}
param1 = {'msg_type':'r2t','status':False, 'volumn':0, 'datetime':time.time()}
param2 = {'msg_type':'t2r', 'doa_angle':0}

address = ('192.168.31.209', 10000)

def fun_udp_msg_send(udp_msg):
   my_udp_socket.sendall(udp_msg.encode())



def thread_udp_recv():
    while True:
        try:
            recv_data = my_udp_socket.recv(1024)
            recv_str = recv_data.decode()
            print(recv_str)            
            recv_param = json.loads(recv_data)
            print (recv_param)
            if recv_param['msg_type'] == 't2r' :
                print (recv_param['doa_angle'])
                global_var['angle'] = recv_param['doa_angle']
                rotate_pic(global_var['angle'])
            elif recv_param['msg_type'] == 'r2t':
                print (recv_param['status'])
                global_var['meeting_status'] = recv_param['status']
            else:
                print('wrong param')
        except:
            pass
    my_udp_socket.close()


def thread_udp_recv():
    while True:
        try:
            data,address = s.recvfrom(1024)
        except:
            pass
    
def udp_server_start():
    data,address = s.recvfrom(1024)
    
def udp_server_stop():
    data,address = s.recvfrom(1024)




## init window
root = tk.Tk()
root.config(width = 320, height = 240)
	

label_recv = Label(root)
label_recv.pack()
label_recv.text = 'recv_txt'


label_send = Label(root)
label_send.pack()
label_send.text = 'recv_txt'


#button
button_1 = Button(root, text="start", command=udp_server_start)
button_1.pack()


button_2 = Button(root, text="stop", command=udp_server_stop)
button_2.pack()



## create UDP socket
    s = socket(AF_INET,SOCK_DGRAM)  
    s.bind((HOST,PORT))


## create UDP recv thread
_thread.start_new_thread(thread_udp_recv, ())
_thread.start_new_thread(thread_random_rotate, ())

root.mainloop()


