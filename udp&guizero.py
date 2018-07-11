#!/usr/bin/python
#coding:utf-8

from guizero import App, Text, PushButton
import time
import datetime
from socket import *
import _thread


global_var = {'meeting_status':0, 'old_time':0, 'new_time':0, 'time_str':'00:00:00', 'send_flag':False}
server = {'IP':'127.0.0.1', 'PORT':9999}

def fun_udp_msg_send(udp_msg):  
    msg_meeting_status.value = udp_msg
    global_var['send_flag'] = True
    pass

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
        button_cmd.text = 'meeting stop'
        button_cmd.bg = 'red'
        fun_udp_msg_send('start')
        global_var['old_time'] = datetime.datetime.now()
        msg_time_elapse.repeat(1000, fun_calculate_time_elapse)
        ## reset elapse time
        global_var['time_str'] = '00:00:00'
        msg_time_elapse.value = global_var['time_str']        
    else:
        global_var['meeting_status'] = False
        button_cmd.text = 'meeting start'
        button_cmd.bg = 'white'
        fun_udp_msg_send('stop')
        msg_time_elapse.cancel(fun_calculate_time_elapse)

def thread_udp_send():
    while True:
        if global_var['send_flag'] == True: # True means msg is need to send, False means send is over.
            my_socket.sendall(msg_meeting_status.value.encode())
            global_var['send_flag'] = False
            print ('true')
        else:
            print ('false')
            time.sleep(1)
        ##data = my_socket.recv(1024)
        ##print(data)
    my_socket.close()


## create window
app = App(title = 'meeting console', width = 320, height = 240)

## create text
msg_meeting_status = Text(app, text='stop')
msg_time_elapse = Text(app, text='00:00:00')

## creat button
button_cmd = PushButton(app, command = fun_meeting_control, text = 'meeting start')
button_cmd.bg = 'white'


my_socket = socket(AF_INET,SOCK_DGRAM)
my_socket.connect((server['IP'],server['PORT']))
                             
_thread.start_new_thread(thread_udp_send, ())



## full screen
##app.tk.attributes("-fullscreen",True)
app.display()


