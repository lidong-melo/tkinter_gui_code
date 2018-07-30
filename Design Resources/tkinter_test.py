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

param = {'volume':0}





def fun_meeting_start():
    #button_start.config(visible = 'no')
    button_meeting_start.place_forget()
    button_meeting_end.place(x=pos_button_meeting_end[2], y=pos_button_meeting_end[3])
    pass

def fun_meeting_end():
    button_meeting_end.place_forget()
    button_meeting_start.place(x=pos_button_meeting_start[2], y=pos_button_meeting_start[3])
    pass

def fun_mute():
    pass

def fun_volume_up():
    if param['volume'] < 9:
        param['volume'] += 1
        photo_path = 'icons/volume_' + str(param['volume']) + '.png'
        photoimage_label_volume.config(file=photo_path)
        #photoimage_button_volume_down.config(file = 'icons/volume_down.png')
        #button_volume_down.config(status = True)
    if param['volume'] == 9:
        photoimage_button_volume_up.config(file = 'icons/volume_up_inactive.png')
        #button_volume_up.config(status = False)
    pass

def fun_volume_down():
    if param['volume'] > 0 :
        param['volume'] -= 1
        photo_path = 'icons/volume_' + str(param['volume']) + '.png'
        photoimage_label_volume.config(file=photo_path)
        #photoimage_button_volume_up.config(file = 'icons/volume_up.png')
        #button_volume_up.config(status = True)
    if param['volume'] == 0:
        photoimage_button_volume_down.config(file = 'icons/volume_down_inactive.png')
        #button_volume_down.config(status = False)
    pass


def fun_mute():
    button_mute.place_forget()
    button_unmute.place(x=pos_button_unmute[2], y=pos_button_unmute[3])
    label_muted.place(x=pos_label_muted[2], y=pos_label_muted[3])
    pass

def fun_unmute():
    button_unmute.place_forget()
    button_mute.place(x=pos_button_mute[2], y=pos_button_mute[3])
    label_muted.place_forget()
    pass

def fun_pause():
    button_pause.place_forget()
    button_resume.place(x=pos_button_resume[2], y=pos_button_resume[3])
    for widget in list_widgets:
        widget.config(bg = '#541F1F')
        try:
            widget.config(activebackground=widget.cget('background'))
        except:
            pass

def fun_resume():
    button_resume.place_forget()
    button_pause.place(x=pos_button_pause[2], y=pos_button_pause[3])
    for widget in list_widgets:
        widget.config(bg = '#000000')
        try:
            widget.config(activebackground=widget.cget('background'))
        except:
            pass

root = tk.Tk()
root.config(width = pos_root[0], height = pos_root[1], bg='black')


## 顺序不能调整，因为有图层index的逻辑关系
photoimage_label_wifi = PhotoImage(file="icons/wifi_off.png")
label_wifi = Label(root, text="OK", image = photoimage_label_wifi)
#label_wifi.config(activebackground=label_wifi.cget('background'))
label_wifi.place(x=pos_label_wifi[2], y=pos_label_wifi[3])
label_wifi.config(width = pos_label_wifi[0], height = pos_label_wifi[1])



photoimage_button_mute = PhotoImage(file="icons/button_mute.png")
button_mute = Button(root, text="OK", command=fun_mute, image = photoimage_button_mute, bg='black')
#button_mute.config(activebackground=button_mute.cget('background'))
#button_mute.place(x=pos_button_mute[2], y=pos_button_mute[3])
button_mute.config(width =pos_button_mute[0], height = pos_button_mute[1])

photoimage_button_unmute = PhotoImage(file="icons/button_unmute.png")
button_unmute = Button(root, text="OK", command=fun_unmute, image = photoimage_button_unmute, bg='black')
button_unmute.place(x=pos_button_unmute[2], y=pos_button_unmute[3])
button_unmute.config(width =pos_button_unmute[0], height = pos_button_unmute[1])



photoimage_label_muted = PhotoImage(file="icons/label_muted.png")
label_muted = Label(root, text="OK", image = photoimage_label_muted)
#label_muted.place(x=pos_label_muted[2], y=pos_label_muted[3])
label_muted.config(width = pos_label_muted[0], height = pos_label_muted[1])

photoimage_label_volume = PhotoImage(file="icons/volume_0.png")
label_volume = Label(root, text="OK", image = photoimage_label_volume)
label_volume.place(x=pos_label_volume[2], y=pos_label_volume[3])
label_volume.config(width = pos_label_volume[0], height = pos_label_volume[1])





photoimage_button_end = PhotoImage(file="icons/button_end_meeting.png")
button_meeting_end = Button(root, text="OK", command=fun_meeting_end, image = photoimage_button_end)
button_meeting_end.config(width = pos_button_meeting_end[0], height = pos_button_meeting_end[1])



photoimage_button_volume_down = PhotoImage(file="icons/volume_down_inactive.png")
button_volume_down = Button(root, text="OK", command=fun_volume_down, image = photoimage_button_volume_down)
button_volume_down.place(x=pos_button_volume_down[2], y=pos_button_volume_down[3])
button_volume_down.config(width = pos_button_volume_down[0], height = pos_button_volume_down[1])



photoimage_button_volume_up = PhotoImage(file="icons/volume_up.png")
button_volume_up = Button(root, text="OK", command=fun_volume_up, image = photoimage_button_volume_up)
button_volume_up.place(x=pos_button_volume_up[2], y=pos_button_volume_up[3])
button_volume_up.config(width = pos_button_volume_up[0], height = pos_button_volume_up[1])


photoimage_button_pause = PhotoImage(file="icons/button_pause.png")
button_pause = Button(root, text="OK", command=fun_pause, image = photoimage_button_pause)
button_pause.place(x=pos_button_pause[2], y=pos_button_pause[3])
button_pause.config(width = pos_button_pause[0], height = pos_button_pause[1])

photoimage_button_resume = PhotoImage(file="icons/button_resume.png")
button_resume = Button(root, text="OK", command=fun_resume, image = photoimage_button_resume)
#button_resume.place(x=pos_button_resume[2], y=pos_button_resume[3])
button_resume.config(width = pos_button_resume[0], height = pos_button_resume[1])



photoimage_button_start = PhotoImage(file="icons/button_start_meeting.png")
button_meeting_start = Button(root, text="OK", command=fun_meeting_start, image = photoimage_button_start)
button_meeting_start.place(x=pos_button_meeting_start[2], y=pos_button_meeting_start[3])
button_meeting_start.config(width = pos_button_meeting_start[0], height = pos_button_meeting_start[1])



photoimage_label_error = PhotoImage(file="icons/error_01.png")
label_error = Label(root, text="OK", image = photoimage_label_error)
#label_error.place(x=pos_label_error[2], y=pos_label_error[3])
label_error.config(width = pos_label_error[0], height = pos_label_error[1])


list_widgets = [root, label_wifi, button_mute, button_unmute, label_muted, label_volume, button_meeting_end, button_volume_down, button_volume_up, button_pause, button_resume, button_meeting_start, label_error]

# change all widgets bg & activebg
for widget in list_widgets:
    widget.config(bg = 'black', borderwidth = 0, highlightthickness = 0)
    try:
        widget.config(activebackground=widget.cget('background'))
    except:
        pass


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
