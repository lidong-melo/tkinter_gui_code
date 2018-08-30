#!/usr/bin/python3
#coding:utf-8

import tkinter as tk
from tkinter import Button, PhotoImage, Label
import datetime


# from socket import *
# import json
import time
import _thread
import platform
import param_host
import msg_list
import wifi
import udp_host
import subprocess

#import serial


def fun_thread_quit_check():
# if ui quit, tell other threads to quit
        try:
            root.cget('bg')
        except:
            param_host.flag['thread_quit'] = True
            s.close()

    

def update_label_status(state):
    label_status.config(text=str(state))
    
    
def tx2_status_watch_dog():
    print('state-->raspi:',msg_list.msg_from_raspi['raspi_state'], 'tx2:',param_host.state['tx2_state'])
    if param_host.state['tx2_state'] == msg_list.msg_from_raspi['raspi_state']:
        msg_list.msg_from_raspi['raspi_state'] = 'READY'
        param_host.watch_dog['timeout'] = param_host.watch_dog['interval']
    elif param_host.watch_dog['timeout'] > 0:
        param_host.watch_dog['timeout'] -= 1
    else:
        param_host.watch_dog['timeout'] = param_host.watch_dog['interval']
        param_host.state['reset_tx2_state'] = True
    
    
# Timer task
list_timer_task = [
{'name':'send_msg_system_ready', 'enable':False, 'interval':1, 'countdown':1, 'callback':udp_host.tx2_udp_send, 'arg':msg_list.msg_to_raspi[0]},#0
{'name':'send_msg_end_meeting', 'enable':False, 'interval':1, 'countdown':1, 'callback':udp_host.tx2_udp_send, 'arg':msg_list.msg_to_raspi[3]},#1 end meeting
{'name':'send_msg_tx2_status', 'enable':False, 'interval':3, 'countdown':3, 'callback':udp_host.tx2_udp_send, 'arg':param_host.state},#2
{'name':'thread_quit_check', 'enable':False, 'interval':1, 'countdown':1, 'callback':fun_thread_quit_check},#3
{'name':'update_label_status', 'enable':False, 'interval':1, 'countdown':1, 'callback':update_label_status, 'arg':param_host.state},#4
{'name':'tx2_status_watch_dog', 'enable':False, 'interval':1, 'countdown':1, 'callback':tx2_status_watch_dog},#5
]

def set_timer_task(task_id, enable, reset):
    list_timer_task[task_id]['enable'] = enable
    if reset == True:# 重置时间
        list_timer_task[task_id]['countdown'] = list_timer_task[task_id]['interval']


def thread_get_rssi():
#time cost is 1.71s, need sudo, otherwise it would be fail and the time cost is 17ms
    while param_host.flag['thread_quit'] != True: 
        # time cost is 17ms
        if(platform.system() == "Linux"):
            rssi = wifi.get_rssi()
        else:
            rssi = '255'# pc调试用
        if rssi.isdigit():
            msg_list.msg_to_raspi[8]['WIFI_RSSI'] = rssi
            udp_host.tx2_udp_send(msg_list.msg_to_raspi[8])
        else:
            msg_list.msg_to_raspi[8]['WIFI_RSSI'] = 255
            udp_host.tx2_udp_send(msg_list.msg_to_raspi[8])
        time.sleep(3)
        
def thread_timer_task():
    while param_host.flag['thread_quit'] == False :
        time.sleep(1)
        for task in list_timer_task:
            if task['enable'] == True:
                if task['countdown'] > 0 :
                    task['countdown'] -= 1
                    if task['countdown'] == 0:
                        task['countdown'] = task['interval']
                        if 'arg' in task.keys():
                            task['callback'](task['arg'])
                        else:
                            task['callback']()

                            
def play_sound(file_name):
    pass
    # if platform.system() == "Linux":
        # proc = subprocess.Popen(["aplay", "-Dhw:2,0", "/home/nvidia/lidong/"+file_name], stdout=subprocess.PIPE, universal_newlines=True)
                            
def start_new_meeting():
    play_sound("Speech On.wav")
    
    pass

def end_meeting():
    play_sound("Speech Off.wav")
    pass 



def thread_ui_reaction():
    while param_host.flag['thread_quit'] != True:
        time.sleep(0.02)
        if msg_list.msg_from_raspi['VOLUME_IS_UP'] != -1:
            param_host.param1['volume'] = msg_list.msg_from_raspi['VOLUME_IS_UP']
            msg_list.msg_from_raspi['VOLUME_IS_UP'] = -1
            msg_list.msg_to_raspi[6]['VOLUME_IS_UP'] = param_host.param1['volume']
            play_sound("Speech On.wav")
            udp_host.tx2_udp_send(msg_list.msg_to_raspi[6])


        if msg_list.msg_from_raspi['VOLUME_IS_DOWN'] != -1:
            param_host.param1['volume'] = msg_list.msg_from_raspi['VOLUME_IS_DOWN']
            msg_list.msg_from_raspi['VOLUME_IS_DOWN'] = -1
            msg_list.msg_to_raspi[7]['VOLUME_IS_DOWN'] = param_host.param1['volume']
            play_sound("Speech Off.wav")
            udp_host.tx2_udp_send(msg_list.msg_to_raspi[7])


        if msg_list.msg_from_raspi['MUTE'] == True:
            msg_list.msg_from_raspi['MUTE'] = False
            param_host.param1['mute'] = True
            play_sound("Speech On.wav")
            msg_list.msg_to_raspi[9]['MUTE'] = True
            udp_host.tx2_udp_send(msg_list.msg_to_raspi[9])


        if msg_list.msg_from_raspi['UNMUTE'] == True:
            msg_list.msg_from_raspi['UNMUTE'] = False
            param_host.param1['mute'] = False
            play_sound("Speech Off.wav")
            msg_list.msg_to_raspi[10]['UNMUTE'] = True
            udp_host.tx2_udp_send(msg_list.msg_to_raspi[10])

    
#state machine
#mute 和 vol+- 还未实现
def thread_tx2_state_machine():
    while param_host.flag['thread_quit'] != True:
        time.sleep(0.02)
        if param_host.state['reset_tx2_state'] == True:#异常，强制关闭会议后退出
            param_host.state['reset_tx2_state'] = False
            param_host.state['tx2_state'] = 'RESET'
        if param_host.state['tx2_state'] == 'READY' :
            #if a113 is ready && raspi is ready 暂时只实现了raspi部分
            if msg_list.msg_from_raspi['RASPI_IS_READY'] == True:
                msg_list.msg_from_raspi['RASPI_IS_READY'] = False
                param_host.state['tx2_state'] = 'IDLE'
                #set_timer_task(0, True, False)
                udp_host.tx2_udp_send(msg_list.msg_to_raspi[0])

        elif param_host.state['tx2_state'] == 'IDLE' :
            if msg_list.msg_from_raspi['MEETING_IS_STARTING'] == True:
                print('meeting is starting')
                msg_list.msg_from_raspi['MEETING_IS_STARTING'] = False
                param_host.state['tx2_state'] = 'RECORDING'
                udp_host.tx2_udp_send(msg_list.msg_to_raspi[1])
                start_new_meeting()
                
        elif param_host.state['tx2_state'] == 'RECORDING' :
            if param_host.param1['no_face_15min'] == True: # 15min noface
                set_timer_task(1, True, False)#end meeting
                #udp_host.tx2_udp_send(msg_list.msg_to_raspi[4])  
            if msg_list.msg_from_raspi['MEETING_IS_ENDING'] == True:
                msg_list.msg_from_raspi['MEETING_IS_ENDING'] = False            
                param_host.state['tx2_state'] = 'END'               
            if msg_list.msg_from_raspi['MEETING_IS_PAUSING'] == True:
                msg_list.msg_from_raspi['MEETING_IS_PAUSING'] = False            
                param_host.state['tx2_state'] = 'PAUSED'
                udp_host.tx2_udp_send(msg_list.msg_to_raspi[2])
                
        elif param_host.state['tx2_state'] == 'RECORDING' :
            if msg_list.msg_from_raspi['MEETING_IS_ENDING'] == True:
                msg_list.msg_from_raspi['MEETING_IS_ENDING'] = False            
                param_host.state['tx2_state'] = 'END'
            

                
        elif param_host.state['tx2_state'] == 'PAUSED' :
            if msg_list.msg_from_raspi['MEETING_IS_ENDING'] == True:
                msg_list.msg_from_raspi['MEETING_IS_ENDING'] = False
                param_host.state['tx2_state'] = 'END'
                
            elif msg_list.msg_from_raspi['MEETING_IS_RESUMING'] == True:
                msg_list.msg_from_raspi['MEETING_IS_RESUMING'] = False            
                param_host.state['tx2_state'] = 'RECORDING'
                udp_host.tx2_udp_send(msg_list.msg_to_raspi[1])
                
        elif param_host.state['tx2_state'] == 'END' :#结束会议
            set_timer_task(1, False, False)#end meeting 
            udp_host.tx2_udp_send(msg_list.msg_to_raspi[4])
            end_meeting()
            param_host.state['tx2_state'] = 'IDLE'
            
        elif param_host.state['tx2_state'] == 'RESET' :
            print('reset tx2')
            end_meeting()
            param_host.state['tx2_state'] = 'READY'
    # 退出状态机，重置环境, 记录error log
    
    

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
def button_click(button_idx):
    udp_host.tx2_udp_send(msg_list.msg_to_raspi[button_idx])
    
root = tk.Tk()
root.config(width = 250, height = 300)

buttons = []
for i in range(len(msg_list.msg_to_raspi)):
    buttons.append(Button(root, text=list(msg_list.msg_to_raspi[i].keys())[0], command=lambda x=i: button_click(x)))
    buttons[i].place(x=30,y=30*i+30)

label_status = Label(root, text='')

label_status.place(x=30,y=5)

root.mainloop()
