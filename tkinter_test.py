#!/usr/bin/python
#coding:utf-8


import tkinter as tk
from PIL import ImageTk, Image ## to use png format, import imageTK
from tkinter import Button, PhotoImage,Label
import platform
from socket import *
import _thread
import random
import time
import json
import datetime

## global variable
global_var = {'meeting_status':False, 'old_time':0, 'new_time':0, 'time_str':'00:00:00', 'angle':0}
server = {'IP':'192.168.31.209', 'PORT':60000}
key_word = {'doa':'doa'}
param1 = {'msg_type':'r2t','status':False, 'volumn':0, 'datetime':time.time()}
param2 = {'msg_type':'t2r', 'doa_angle':0}

def rotate_pic(angle):
    global_var['angle'] = angle
    photo_bg.paste(image_bg.rotate(global_var['angle']))
    label_bg.config(image = photo_bg) 
    label_angle.config(text = str(angle))


def fun_udp_msg_send(udp_msg):
   my_udp_socket.sendall(udp_msg.encode())



def thread_udp_recv():
    while True:
        try:
            recv_data = my_udp_socket.recv(1024)
            recv_str = recv_data.decode()
            print(recv_str)            
            recv_param = json.loads(recv_str)
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
            
            '''
            recv_str = recv_data.decode()
            print(recv_str)
            if recv_str.find(key_word['doa']) != -1:
                index_start = recv_str.find('doa=')+4
                aaa = recv_str[index_start:len(recv_str)]
                print (index_start, aaa)
                angle = int(aaa)
                try:
                    rotate_pic(angle)
                except:
                    pass
            '''
        except:
            pass
    my_udp_socket.close()



def thread_random_rotate():
    while True:
        time.sleep(0.3)
        angle = random.randint(0,360)
        pass
        try:
            pass
            rotate_pic(angle)
        except:
            pass
      


def thread_time_update():
    while global_var['meeting_status'] == True:
        global_var['new_time'] = datetime.datetime.now()
        time_delta = global_var['new_time'] - global_var['old_time']
        m, s = divmod(time_delta.seconds, 60)
        h, m = divmod(m, 60)
        global_var['time_str'] = '{0:02d}:{1:02d}:{2:02d}'.format(h, m, s)
        print(global_var['time_str'])
        label_time.config(text = global_var['time_str'])
        time.sleep(1)
   

def fun_meeting_control():
    global meeting_status # True is start, False is stop
    if global_var['meeting_status'] == False:
        global_var['meeting_status'] = True
        fun_udp_msg_send('start') 
        photoimage_button.config(file='image_button_stop-1.png')
        global_var['time_str'] = '00:00:00'
        ## initial time
        global_var['old_time'] = datetime.datetime.now()
        global_var['new_time'] = global_var['old_time']        
        _thread.start_new_thread(thread_time_update, ())
    else:
        fun_udp_msg_send('stop')
        global_var['meeting_status'] = False
        photoimage_button.config(file='image_metal_button-1.png')
        



## check system version
sysstr = platform.system()
if(sysstr =="Windows"):
    print ("Call Windows tasks")
elif(sysstr == "Linux"):
    print ("Call Linux tasks")
else:
    print ("Other System tasks")   


## init window
root = tk.Tk()
root.config(width = 320, height = 240)


## adapt to raspberry pi
if(sysstr == "Linux"):
    root.attributes("-fullscreen", True)
    root.config(cursor="none")
    ##server = {'IP':'10.0.5.1', 'PORT':9999}
	




## clock background
image_bg = Image.open("clock.png")
photo_bg = ImageTk.PhotoImage(image_bg)
label_bg = Label(image = photo_bg)
label_bg.image = photo_bg # keep a reference!
label_bg.place(x=40,y=0)


#button
photoimage_button = PhotoImage(file="image_metal_button-1.png")
button_cmd = Button(root, text="OK", command=fun_meeting_control, image = photoimage_button)
button_cmd.place(x=110,y=70)
#button.config(image = 'image_metal_button.png')
button_cmd.config(width = 100, height = 100, borderwidth = 0, highlightthickness = 0)

label_angle = Label(root, font='Arial -20 bold')
label_angle.place(x=0,y=0)

label_time = Label(root, font='Arial -14 bold', text='00:00:00')
label_time.place(x=0,y=220)



## create UDP socket
my_udp_socket = socket(AF_INET,SOCK_DGRAM)
my_udp_socket.connect((server['IP'],server['PORT']))


## create UDP recv thread
_thread.start_new_thread(thread_udp_recv, ())

#_thread.start_new_thread(thread_random_rotate, ())



root.mainloop()


