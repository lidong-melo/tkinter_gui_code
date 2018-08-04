import tkinter as tk
import tkinter
from tkinter import Button, PhotoImage, Label
import datetime


from socket import *
import json
import time
import _thread
import platform


HOST = '192.168.31.209'  
PORT = 60000
address_list = ['192.168.2.207', 10000]
param = {'thread_quit': False}
param2 = {'msg_type':'t2r', 'doa_angle':True} 

def button_click(button_idx):
    json_string = json.dumps(list_button[button_idx])
    address_tuple = tuple(address_list)
    try:
        s.sendto(json_string.encode(), address_tuple)
        print('send', address_tuple, json_string)
    except:
        print('disconnect')

    
def fun_thread_quit_check():
# if ui quit, tell other threads to quit
    while param['thread_quit'] != True:
        time.sleep(0.1)
        try:
            root.cget('bg')
        except:
            param['thread_quit'] = True
            s.close()

    

def thread_udp_recv():
    while param['thread_quit'] != True:
        print ('...waiting for message..'  )
        try:
            data,address_recv = s.recvfrom(1024)
            address_list.clear()
            address_list_temp = list(address_recv)
            address_list.append(address_list_temp[0])
            address_list.append(address_list_temp[1])
            print('recv',address_list)
            
        except:
            pass

    
    
if(platform.system() == "Linux"):
    server = {'IP':'10.0.5.1', 'PORT':9999}
else:
    server = {'IP':gethostbyname(gethostname()), 'PORT':60000}
    print(server)

    
    
s = socket(AF_INET,SOCK_DGRAM)  
s.bind((server['IP'], server['PORT']))
_thread.start_new_thread(fun_thread_quit_check, ())
_thread.start_new_thread(thread_udp_recv, ())






    

list_button = [
{"SYSTEM_IS_READY": True},
{"MEETING_IS_STARTED": True},
{"TX2_END_MEETING":True},
{"MEETING_IS_END":True}
]


root = tk.Tk()
root.config(width = 800, height = 600)

buttons = []
for i in range(len(list_button)):
    buttons.append(Button(root, text=list(list_button[i].keys())[0], command=lambda x=i: button_click(x)))
    buttons[i].place(x=50,y=50*i+100)



root.mainloop()
