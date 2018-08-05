#!/usr/bin/python
#coding:utf-8

#from guizero import App, Text, PushButton
from guizero import *
import time
import datetime
from socket import *
import _thread
#import tkinter
from PIL import Image

## global variable
global_var = {'meeting_status':False, 'old_time':0, 'new_time':0, 'time_str':'00:00:00', 'send_flag':False}
#server = {'IP':'192.168.31.209', 'PORT':9999}
server = {'IP':'10.0.5.1', 'PORT':9999}


def fun_udp_msg_send(udp_msg):
   my_socket.sendall(udp_msg.encode())

def fun_calculate_time_elapse():
   global_var['new_time'] = datetime.datetime.now()
   time_delta = global_var['new_time'] - global_var['old_time']
   m, s = divmod(time_delta.seconds, 60)
   h, m = divmod(m, 60)
   global_var['time_str'] = '{0:02d}:{1:02d}:{2:02d}'.format(h, m, s)
   print (global_var['time_str'])
   msg_time_elapse.value = global_var['time_str']


def fun_meeting_control():
   global meeting_status # True is start, False is stop
   if global_var['meeting_status'] == False:
       global_var['meeting_status'] = True
       fun_udp_msg_send('start')
       ## enable timer
       global_var['old_time'] = datetime.datetime.now()
       msg_time_elapse.repeat(1000, fun_calculate_time_elapse)
       ## update UI
       button_cmd.text = 'meeting stop'
       button_cmd.image = 'image_button_stop.png'
       global_var['time_str'] = '00:00:00'
       msg_time_elapse.value = global_var['time_str']
   else:
       fun_udp_msg_send('stop')
       ## disable timer
       msg_time_elapse.cancel(fun_calculate_time_elapse)
       ## update UI
       global_var['meeting_status'] = False
       button_cmd.text = 'meeting start'
       button_cmd.image = 'image_metal_button.png'


def thread_udp_send():
   while True:
       recv_data = my_socket.recv(1024)
       print(recv_data)
   my_socket.close()


## create window
app = App(title = 'meeting console', width = 320, height = 240, layout="grid")
## full screen
app.tk.attributes("-fullscreen",True)


## hide mouse
app.tk.config(cursor="none")

## create text
msg_time_elapse = Text(app, text='00:00:00', grid=[0,0])

## create button
button_cmd = PushButton(app, command = fun_meeting_control, text = 'meeting start', grid=[0,1])
button_cmd.image = 'image_metal_button.png'
button_cmd.tk.configure(width = 160, height = 160, borderwidth = 0, highlightthickness = 0)


## create UDP socket
my_socket = socket(AF_INET,SOCK_DGRAM)
my_socket.connect((server['IP'],server['PORT']))

## create UDP recv thread
_thread.start_new_thread(thread_udp_send, ())

#pic = Picture(app, image = 'image_metal_button.png', grid =[0,2])
#pic.tk.rotate(30)

img = Image.open(image = 'image_metal_button.png')

app.display()

