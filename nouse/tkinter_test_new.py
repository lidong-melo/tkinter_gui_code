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

import sys
import subprocess

## 顺序为 width，height，x，y
pos_root = [320, 240]
pos_label_wifi = [18, 18, 151, 5]
pos_button_volume_down = [50, 50, 36, 96]
pos_button_volume_up = [50, 50, 234, 96]

pos_button_mute = [50, 50, 135, 24]
pos_button_unmute = [50, 50, 135, 24]
pos_label_muted = [64, 16, 128, 69]
pos_button_meeting_start = [120, 120, 100, 60]
pos_button_meeting_end = [64, 64, 128, 88]
pos_button_pause = [50, 50, 135, 166]
pos_button_resume = [50, 50, 135, 166]
pos_label_volume = [200, 84, 60, 138]
pos_label_error = [18, 18, 151, 222]



param = {'volume':0, 'volume_adjust_timeout':0}


def fun_meeting_start():
    show_widget_list(list_meeting_start_show)
    hide_widget_list(list_meeting_start_hide)
    pass

def fun_meeting_end():
    show_widget_list(list_meeting_end_show)
    hide_widget_list(list_meeting_end_hide)
    pass

def fun_volume_up():
    volume_adjust_show()
    param['volume_adjust_timeout'] = 2
    if param['volume'] < 9:
        param['volume'] += 1
        photo_path = 'icons/volume_' + str(param['volume']) + '.png'
        photoimage_label_volume.config(file=photo_path)
    pass

def fun_volume_down():
    volume_adjust_show()
    param['volume_adjust_timeout'] = 2
    if param['volume'] > 0 :
        param['volume'] -= 1
        photo_path = 'icons/volume_' + str(param['volume']) + '.png'
        photoimage_label_volume.config(file=photo_path)
    pass


def fun_mute():
    show_widget_list(list_mute_show)
    hide_widget_list(list_mute_hide)
    pass

def fun_unmute():
    show_widget_list(list_unmute_show)
    hide_widget_list(list_unmute_hide)
    pass

def fun_pause():
    show_widget_list(list_pause_show)
    hide_widget_list(list_pause_hide)
    for widget in list_all_widgets:
        widget.config(bg = '#541F1F')
        try:
            widget.config(activebackground=widget.cget('background'))
        except:
            pass

def fun_resume():
    show_widget_list(list_resume_show)
    hide_widget_list(list_resume_hide)    
    for widget in list_all_widgets:
        widget.config(bg = '#000000')
        try:
            widget.config(activebackground=widget.cget('background'))
        except:
            pass

def volume_adjust_show():
    label_volume.place(x = pos[id(label_volume)][2], y = pos[id(label_volume)][3])
    photoimage_button_volume_down.config(file = 'icons/volume_down.png')
    photoimage_button_volume_up.config(file = 'icons/volume_up.png')
    pass

def volume_adjust_hide():
    label_volume.place_forget()
    photoimage_button_volume_down.config(file = 'icons/volume_down_inactive.png')
    photoimage_button_volume_up.config(file = 'icons/volume_up_inactive.png')
    pass

def thread_update_ui():
    while 1 :
        time.sleep(1)
        if param['volume_adjust_timeout'] > 0:
            param['volume_adjust_timeout'] -= 1
            if param['volume_adjust_timeout'] == 0:
                try:
                    volume_adjust_hide()
                except:
                    pass

def show_widget_list(widget_list):
    for widget in widget_list:
        print(pos[id(widget)])
        widget.place(x = pos[id(widget)][2], y = pos[id(widget)][3])


def hide_widget_list(widget_list):
    for widget in widget_list:
        print(pos[id(widget)])
        widget.place_forget()
 


root = tk.Tk()
root.config(width = pos_root[0], height = pos_root[1], bg='black')

sysstr = platform.system()
## adapt to raspberry pi
if(sysstr == "Linux"):
    root.attributes("-fullscreen", True)
    root.config(cursor="none")
    ##server = {'IP':'10.0.5.1', 'PORT':9999}

    


## 顺序不能调整，因为有图层index的逻辑关系
photoimage_label_wifi = PhotoImage(file="icons/wifi_off.png")
label_wifi = Label(root, text="OK", image = photoimage_label_wifi)
#label_wifi.config(activebackground=label_wifi.cget('background'))
#label_wifi.place(x=pos_label_wifi[2], y=pos_label_wifi[3])
#label_wifi.config(width = pos_label_wifi[0], height = pos_label_wifi[1])



photoimage_button_mute = PhotoImage(file="icons/button_mute.png")
button_mute = Button(root, text="OK", command=fun_mute, image = photoimage_button_mute, bg='black')

photoimage_button_unmute = PhotoImage(file="icons/button_unmute.png")
button_unmute = Button(root, text="OK", command=fun_unmute, image = photoimage_button_unmute, bg='black')



photoimage_label_muted = PhotoImage(file="icons/label_muted.png")
label_muted = Label(root, text="OK", image = photoimage_label_muted)


photoimage_button_volume_down = PhotoImage(file="icons/volume_down_inactive.png")
button_volume_down = Button(root, text="OK", command=fun_volume_down, image = photoimage_button_volume_down)

photoimage_button_volume_up = PhotoImage(file="icons/volume_up_inactive.png")
button_volume_up = Button(root, text="OK", command=fun_volume_up, image = photoimage_button_volume_up)


photoimage_label_volume = PhotoImage(file="icons/volume_0.png")
label_volume = Label(root, text="OK", image = photoimage_label_volume)


photoimage_button_pause = PhotoImage(file="icons/button_pause.png")
button_pause = Button(root, text="OK", command=fun_pause, image = photoimage_button_pause)


photoimage_button_resume = PhotoImage(file="icons/button_resume.png")
button_resume = Button(root, text="OK", command=fun_resume, image = photoimage_button_resume)


photoimage_label_error = PhotoImage(file="icons/error_01.png")
label_error = Label(root, text="OK", image = photoimage_label_error)


photoimage_button_end = PhotoImage(file="icons/button_end_meeting.png")
button_meeting_end = Button(root, text="OK", command=fun_meeting_end, image = photoimage_button_end)

photoimage_button_start = PhotoImage(file="icons/button_start_meeting.png")
button_meeting_start = Button(root, text="OK", command=fun_meeting_start, image = photoimage_button_start)


list_all_widgets = [root, label_wifi, button_mute, button_unmute, label_muted, label_volume, button_meeting_end, button_volume_down, button_volume_up, button_pause, button_resume, button_meeting_start, label_error]

list_meeting_start_show = [button_mute, button_meeting_end, button_pause]
list_meeting_start_hide = [button_unmute,  label_muted, button_resume, button_meeting_start]

list_meeting_end_show = [button_meeting_start]
list_meeting_end_hide = [button_unmute, label_muted, button_resume, button_mute, button_meeting_end, button_pause]

list_volume_adjust_show = [label_volume]
list_volume_adjust_hide = [label_volume]

list_mute_show = [button_unmute, label_muted]
list_mute_hide = [button_mute]

list_unmute_show = [button_mute]
list_unmute_hide = [button_unmute, label_muted]

list_pause_show = [button_resume]
list_pause_hide = [button_pause]

list_resume_show = [button_pause]
list_resume_hide = [button_resume]

list_home = [label_wifi, label_volume, button_volume_down, button_volume_up, button_meeting_start]



pos = {
id(label_wifi): [18, 18, 151, 5],
id(button_volume_down): [50, 50, 36, 96],
id(button_volume_up): [50, 50, 234, 96],
id(button_mute): [50, 50, 135, 24],
id(button_unmute): [50, 50, 135, 24],
id(label_muted): [64, 16, 128, 69],
id(button_meeting_start): [120, 120, 100, 60],
id(button_meeting_end): [64, 64, 128, 88],
id(button_pause): [50, 50, 135, 166],
id(button_resume): [50, 50, 135, 166],
id(label_volume): [200, 84, 60, 138],
id(label_error): [18, 18, 151, 222]}
print(pos)

for widget in list_home:
    print(pos[id(widget)])
    widget.place(x = pos[id(widget)][2], y = pos[id(widget)][3])
    widget.config(width = pos[id(widget)][0], height = pos[id(widget)][1])


# change all widgets bg & activebg
for widget in list_all_widgets:
    widget.config(bg = 'black', borderwidth = 0, highlightthickness = 0)
    try:
        widget.config(activebackground=widget.cget('background'))
    except:
        pass

    
_thread.start_new_thread(thread_update_ui, ())


root.mainloop()





'''
## global variable
global_var = {'meeting_status':False, 'old_time':0, 'new_time':0, 'time_str':'00:00:00', 'angle':0}
server = {'IP':'192.168.31.209', 'PORT':60000}
key_word = {'doa':'doa'}
param1 = {'msg_type':'r2t','status':False, 'volumn':0, 'datetime':time.time()}
param2 = {'msg_type':'t2r', 'doa_angle':0}

def fun_rotate_pic(angle):
    global_var['angle'] = angle
    photo_bg.paste(image_bg.rotate(global_var['angle']))
    label_bg.config(image = photo_bg) 
    label_angle.config(text = str(angle))


def fun_udp_msg_send(udp_msg):
   my_udp_socket.sendall(udp_msg.encode())

   
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

    else:
        fun_udp_msg_send('stop')
        global_var['meeting_status'] = False
        photoimage_button.config(file='image_metal_button-1.png')


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
                fun_rotate_pic(global_var['angle'])
            elif recv_param['msg_type'] == 'r2t':
                print (recv_param['status'])
                global_var['meeting_status'] = recv_param['status']
            else:
                print('wrong param')
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
            fun_rotate_pic(angle)
        except:
            pass
      

def thread_time_update():
    while True:
        while global_var['meeting_status'] == True:
            global_var['new_time'] = datetime.datetime.now()
            time_delta = global_var['new_time'] - global_var['old_time']
            m, s = divmod(time_delta.seconds, 60)
            h, m = divmod(m, 60)
            global_var['time_str'] = '{0:02d}:{1:02d}:{2:02d}'.format(h, m, s)
            print(global_var['time_str'])
            label_time.config(text = global_var['time_str'])
            time.sleep(1)


## check system version
sysstr = platform.system()
if(sysstr =="Windows"):
    print ("Call Windows tasks")
elif(sysstr == "Linux"):
    print ("Call Linux tasks")
else:
    print ("Other System tasks")   

global_var['old_time'] = datetime.datetime.now()
global_var['new_time'] = global_var['old_time']


## init window
root = tk.Tk()
root.config(width = 320, height = 240)


## adapt to raspberry pi
if(sysstr == "Linux"):
    root.attributes("-fullscreen", True)
    root.config(cursor="none")
    ##server = {'IP':'10.0.5.1', 'PORT':9999}
	

## clock background
image_bg = Image.open("icons/button_end_meeting.png")
photo_bg = ImageTk.PhotoImage(image_bg)
label_bg = Label(image = photo_bg)
label_bg.image = photo_bg # keep a reference!
label_bg.place(x=40,y=0)


## button
photoimage_button = PhotoImage(file="image_metal_button-1.png")
button_cmd = Button(root, text="OK", command=fun_meeting_control, image = photoimage_button)
button_cmd.config(activebackground=button_cmd.cget('background'))
button_cmd.place(x=110,y=70)
button_cmd.config(width = 100, height = 100)


## label angle
label_angle = Label(root, font='Arial -20 bold')
label_angle.place(x=0,y=0)


## label time
label_time = Label(root, font='Arial -14 bold', text='00:00:00')
label_time.place(x=0,y=220)



## create UDP socket
my_udp_socket = socket(AF_INET,SOCK_DGRAM)
my_udp_socket.connect((server['IP'],server['PORT']))


## create UDP recv thread
_thread.start_new_thread(thread_udp_recv, ())
_thread.start_new_thread(thread_time_update, ())
#_thread.start_new_thread(thread_random_rotate, ())
'''
