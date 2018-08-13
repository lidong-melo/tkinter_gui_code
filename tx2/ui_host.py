#!/usr/bin/python3
#coding:utf-8

import tkinter as tk
import tkinter
from tkinter import Button, PhotoImage, Label
import datetime


from socket import *
import json
import time
import _thread
import platform
import param_host
import wifi
import subprocess


# HOST = '192.168.31.209'
# PORT = 60000
#address_list = ['192.168.2.207', 10000]
address_list = ['10.0.5.2', 10000]
param = {'thread_quit': False}
#param2 = {'msg_type':'t2r', 'doa_angle':True} 

timeout = {'no_face_15min': -1}

state = {'tx2_state':'READY', 'reset_tx2_state':False,}

watch_dog = {'timeout':30, 'interval':30}

def thread_update_timeout(): 
    while param['thread_quit'] == False:
        time.sleep(1)
        for key, value in timeout.items():
            if value > 0:
                timeout[key] -= 1
        pass
        
def button_click(button_idx):
    tx2_udp_send(param_host.msg_to_raspi[button_idx])

        
 
    
def fun_thread_quit_check():
# if ui quit, tell other threads to quit
        try:
            root.cget('bg')
        except:
            param['thread_quit'] = True
            s.close()

def tx2_udp_send(msg_dict):
    json_string = json.dumps(msg_dict)
    address_tuple = tuple(address_list)
    try:
        s.sendto(json_string.encode(), address_tuple)
        print('send', address_tuple, json_string)
    except:
        print('disconnect')       

        
def thread_udp_recv():
    while param['thread_quit'] == False:
        try:
            recv_data,address_recv = s.recvfrom(1024)
            
            # update client ip -->
            address_list.clear()
            address_list_temp = list(address_recv)
            address_list.append(address_list_temp[0])
            address_list.append(address_list_temp[1])
            print('recv',address_list,recv_data)
            # <-- update client ip
            
            # parse recv msg
            recv_str = recv_data.decode()
            ##print('str:',recv_str)
            recv_msg_dict = json.loads(recv_str)
            ##print('dict:',recv_msg_dict)
            parse_udp_msg(recv_msg_dict)
            recv_msg_dict.clear()
        except:
            pass
    my_udp_socket.close()

    
def parse_udp_msg(msg):
    ##print('parse -->')
    # 按照状态机接收解析消息，如果不对应则抛弃。
    # 方法1：在字典中找列表中的值
    # for key in msg_list_for_state_machine[status['meeting_status']]:
        # print('123',key)
        # if msg.get(key):
            # msg_from_tx2[key] = msg[key]
    
    # 方法2：在列表中找字典中的key
    for key in msg:
        #print(param_host.param1)
        #print(param_host.msg_from_raspi)
        if param_host.msg_list_for_state_machine[state['tx2_state']].count(key) != 0:
            param_host.msg_from_raspi[key] = msg[key]
            #print(param_host.msg_from_raspi[key])
            
            
    ##print('<-- parse')
    

def update_label_status(state):
    label_status.config(text=str(state))
    
    
def tx2_status_watch_dog():
    print('state-->raspi:',param_host.msg_from_raspi['raspi_state'], 'tx2:',state['tx2_state'])
    if state['tx2_state'] == param_host.msg_from_raspi['raspi_state']:
        param_host.msg_from_raspi['raspi_state'] = 'READY'
        watch_dog['timeout'] = watch_dog['interval']
    elif watch_dog['timeout'] > 0:
        watch_dog['timeout'] -= 1
    else:
        watch_dog['timeout'] = watch_dog['interval']
        state['reset_tx2_state'] = True
    
        
        

    
# def thread_udp_recv():
    # while param['thread_quit'] == False:
        # print ('...waiting for message..'  )
        # try:
            # data,address_recv = s.recvfrom(1024)
            # address_list.clear()
            # address_list_temp = list(address_recv)
            # address_list.append(address_list_temp[0])
            # address_list.append(address_list_temp[1])
            # print('recv',address_list)
            
        # except:
            # pass

# UI init
# msg_to_raspi = [
# {"SYSTEM_IS_READY": True},
# {"MEETING_IS_RECORDING": True},
# {'MEETING_IS_PAUSED':True},
# {"TX2_END_MEETING":True},
# {"MEETING_IS_END":True},
# {'ERROR_CODE':0},
# {'VOLUME_IS_UP':0}, 
# {'VOLUME_IS_DOWN':0}
# ]
    
#udp inits
if platform.system() == "Linux":
    server = {'IP':'10.0.5.1', 'PORT':9999}
else:
    server = {'IP':gethostbyname(gethostname()), 'PORT':60000}
    print(server)
  
#udp init
s = socket(AF_INET,SOCK_DGRAM)  
s.bind((server['IP'], server['PORT']))
#_thread.start_new_thread(fun_thread_quit_check, ())
_thread.start_new_thread(thread_udp_recv, ())



# Timer task
list_timer_task = [
{'name':'send_msg_system_ready', 'enable':False, 'interval':1, 'countdown':1, 'callback':tx2_udp_send, 'arg':param_host.msg_to_raspi[0]},#0
{'name':'send_msg_end_meeting', 'enable':False, 'interval':1, 'countdown':1, 'callback':tx2_udp_send, 'arg':param_host.msg_to_raspi[3]},#1 end meeting
{'name':'send_msg_tx2_status', 'enable':False, 'interval':3, 'countdown':3, 'callback':tx2_udp_send, 'arg':state},#2
{'name':'thread_quit_check', 'enable':False, 'interval':1, 'countdown':1, 'callback':fun_thread_quit_check},#3
{'name':'update_label_status', 'enable':False, 'interval':1, 'countdown':1, 'callback':update_label_status, 'arg':state},#4
{'name':'tx2_status_watch_dog', 'enable':False, 'interval':1, 'countdown':1, 'callback':tx2_status_watch_dog},#5

]

def set_timer_task(task_id, enable, reset):
    list_timer_task[task_id]['enable'] = enable
    if reset == True:# 重置时间
        list_timer_task[task_id]['countdown'] = list_timer_task[task_id]['interval']
        
def thread_timer_task():
    while param['thread_quit'] == False :
        time.sleep(1)
        for task in list_timer_task:
            if task['enable'] == True:
                if task['countdown'] > 0 :
                    task['countdown'] -= 1
                    if task['countdown'] == 0:
                        task['countdown'] = task['interval']
                        if 'arg' in task.keys():
                            task['callback'](task['arg'])
                            #print('task_arg_run')
                        else:
                            task['callback']()
                            #print('task_noarg_run')

                            
def play_sound(file_name):
    #full_file_name = "/home/nvidia/lidong/"
    #full_file_name += file_name
    if platform.system() == "Linux":
        proc = subprocess.Popen(["aplay", "-Dhw:2,0", "/home/nvidia/lidong/"+file_name], stdout=subprocess.PIPE, universal_newlines=True)
                            
def start_new_meeting():
    #print('play sound')
    play_sound("Speech On.wav")
    
    pass

def end_meeting():
    play_sound("Speech Off.wav")
    pass 

#aplay -Dhw:2,0 Speech\ On.wav 
# def volume_up():
    # print('volume up')

    # pass
    
# def volume_down():
    # print('volume down')

    # pass    

# def mute():
    # print('mute')


# def unmute():
    # print('unmute')


def thread_ui_reaction():
    while param['thread_quit'] != True:
        time.sleep(0.02)
        if param_host.msg_from_raspi['VOLUME_IS_UP'] != -1:
            param_host.param1['volume'] = param_host.msg_from_raspi['VOLUME_IS_UP']
            param_host.msg_from_raspi['VOLUME_IS_UP'] = -1
            param_host.msg_to_raspi[6]['VOLUME_IS_UP'] = param_host.param1['volume']
            play_sound("Speech On.wav")
            #out, err = proc.communicate()
            tx2_udp_send(param_host.msg_to_raspi[6])
            #print('out',out)
            #print('err',err)

        if param_host.msg_from_raspi['VOLUME_IS_DOWN'] != -1:
            param_host.param1['volume'] = param_host.msg_from_raspi['VOLUME_IS_DOWN']
            param_host.msg_from_raspi['VOLUME_IS_DOWN'] = -1
            param_host.msg_to_raspi[7]['VOLUME_IS_DOWN'] = param_host.param1['volume']
            play_sound("Speech Off.wav")
            #out, err = proc.communicate()
            tx2_udp_send(param_host.msg_to_raspi[7])
            #print('out',out)
            #print('err',err)

        if param_host.msg_from_raspi['MUTE'] == True:
            param_host.msg_from_raspi['MUTE'] = False
            param_host.param1['mute'] = True
            play_sound("Speech On.wav")
            #out, err = proc.communicate()
            param_host.msg_to_raspi[9]['MUTE'] = True
            tx2_udp_send(param_host.msg_to_raspi[9])
            #print('out',out)
            #print('err',err)

        if param_host.msg_from_raspi['UNMUTE'] == True:
            param_host.msg_from_raspi['UNMUTE'] = False
            param_host.param1['mute'] = False
            play_sound("Speech Off.wav")
            #out, err = proc.communicate()
            param_host.msg_to_raspi[10]['UNMUTE'] = True
            tx2_udp_send(param_host.msg_to_raspi[10])
            #print('out',out)
            #print('err',err)
    
#state machine
#mute 和 vol+- 还未实现
def thread_tx2_state_machine():
    while param['thread_quit'] != True:
        time.sleep(0.02)
        if state['reset_tx2_state'] == True:#异常，强制关闭会议后退出
            state['reset_tx2_state'] = False
            state['tx2_state'] = 'RESET'
        if state['tx2_state'] == 'READY' :
            if param_host.msg_from_raspi['RASPI_IS_READY'] == True:
                param_host.msg_from_raspi['RASPI_IS_READY'] = False
                state['tx2_state'] = 'IDLE'
                #set_timer_task(0, True, False)
                tx2_udp_send(param_host.msg_to_raspi[0])

        elif state['tx2_state'] == 'IDLE' :
            if param_host.msg_from_raspi['MEETING_IS_STARTING'] == True:
                print('meeting is starting')
                param_host.msg_from_raspi['MEETING_IS_STARTING'] = False
                state['tx2_state'] = 'RECORDING'
                tx2_udp_send(param_host.msg_to_raspi[1])
                start_new_meeting()
        elif state['tx2_state'] == 'RECORDING' :
            if param_host.param1['no_face_15min'] == True:
                set_timer_task(1, True, False)#end meeting
                #tx2_udp_send(param_host.msg_to_raspi[4])  
            if param_host.msg_from_raspi['MEETING_IS_ENDING'] == True:
                param_host.msg_from_raspi['MEETING_IS_ENDING'] = False            
                state['tx2_state'] = 'END'               
            if param_host.msg_from_raspi['MEETING_IS_PAUSING'] == True:
                param_host.msg_from_raspi['MEETING_IS_PAUSING'] = False            
                state['tx2_state'] = 'PAUSED'
                tx2_udp_send(param_host.msg_to_raspi[2])
        elif state['tx2_state'] == 'PAUSED' :
            if param_host.msg_from_raspi['MEETING_IS_ENDING'] == True:
                param_host.msg_from_raspi['MEETING_IS_ENDING'] = False            
                state['tx2_state'] = 'END'
                
            elif param_host.msg_from_raspi['MEETING_IS_RESUMING'] == True:
                param_host.msg_from_raspi['MEETING_IS_RESUMING'] = False            
                state['tx2_state'] = 'RECORDING'
                tx2_udp_send(param_host.msg_to_raspi[1])
        elif state['tx2_state'] == 'END' :#结束会议
            set_timer_task(1, False, False)#end meeting
            tx2_udp_send(param_host.msg_to_raspi[4])
            end_meeting()
            state['tx2_state'] = 'IDLE'
        elif state['tx2_state'] == 'RESET' :
            print('reset tx2')
            #set_timer_task(1, False, False)#end meeting
            #tx2_udp_send(param_host.msg_to_raspi[4])
            end_meeting()
            state['tx2_state'] = 'READY'
    # 退出状态机，重置环境, 记录error log


def thread_get_rssi():
    while param['thread_quit'] != True: 
        if(platform.system() == "Linux"):
            rssi = wifi.get_rssi()
        else:
            rssi = '255'# pc调试用
        if rssi.isdigit():
            param_host.msg_to_raspi[8]['WIFI_RSSI'] = rssi
            tx2_udp_send(param_host.msg_to_raspi[8])
        else:
            param_host.msg_to_raspi[8]['WIFI_RSSI'] = 255
            tx2_udp_send(param_host.msg_to_raspi[8])
            # param_host.msg_to_raspi[5]['ERROR_CODE'] = 55
            # tx2_udp_send(param_host.msg_to_raspi[5])
        time.sleep(3)
    
    
    

# init thread
_thread.start_new_thread(thread_tx2_state_machine, ())
_thread.start_new_thread(thread_ui_reaction, ())
_thread.start_new_thread(thread_timer_task, ())
_thread.start_new_thread(thread_get_rssi, ())

set_timer_task(2, True, True)#loop send state
set_timer_task(3, True, True)#thread_quit_check 
set_timer_task(4, True, True)#update label_status
set_timer_task(5, True, True)#tx2_status_watch_dog

#init UI
root = tk.Tk()
root.config(width = 250, height = 300)

buttons = []
for i in range(len(param_host.msg_to_raspi)):
    buttons.append(Button(root, text=list(param_host.msg_to_raspi[i].keys())[0], command=lambda x=i: button_click(x)))
    buttons[i].place(x=30,y=30*i+30)

label_status = Label(root, text='')

label_status.place(x=30,y=5)

root.mainloop()
