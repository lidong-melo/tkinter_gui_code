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

timeout = {'no_face_15min': -1}


def thread_update_timeout():
    while param['thread_quit'] == False:
        time.sleep(1)
        for key, value in timeout.items():
            if value > 0:
                timeout[key] -= 1
        pass
        
def button_click(button_idx):
    tx2_udp_send(msg_list[button_idx])

        
 
    
def fun_thread_quit_check():
# if ui quit, tell other threads to quit
    while param['thread_quit'] == False:
        time.sleep(0.1)
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
    while param['quit_flag'] == False:
        try:
            recv_data,address_recv = s.recv(1024)
            # update client ip -->
            address_list.clear()
            address_list_temp = list(address_recv)
            address_list.append(address_list_temp[0])
            address_list.append(address_list_temp[1])
            print('recv',address_list)
            # <-- update client ip
            
            # parse recv msg
            recv_str = recv_data.decode()
            print('str:',recv_str)
            recv_msg_dict = json.loads(recv_str)
            print('dict:',recv_msg_dict)
            parse_udp_msg(recv_msg_dict)
            recv_msg_dict.clear()
        except:
            pass
    my_udp_socket.close()

    
def parse_udp_msg(msg):
    print('parse -->')
    # 按照状态机接收解析消息，如果不对应则抛弃。
    # 方法1：在字典中找列表中的值
    # for key in param.msg_list_for_state_machine[param.param3['meeting_status']]:
        # print('123',key)
        # if msg.get(key):
            # param.msg_from_tx2[key] = msg[key]
    
    # 方法2：在列表中找字典中的key
    for key in msg:
        if msg_list_for_state_machine[param.param3['meeting_status']].count(key) != 0:
            msg_from_tx2[key] = msg[key]
    print('<-- parse')
    
    
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
msg_list = [
{"SYSTEM_IS_READY": True},
{"MEETING_IS_RECORDING": True},
{"TX2_END_MEETING":True},
{"MEETING_IS_END":True}
]
    
#udp init
if(platform.system() == "Linux"):
    server = {'IP':'10.0.5.1', 'PORT':9999}
else:
    server = {'IP':gethostbyname(gethostname()), 'PORT':60000}
    print(server)
  
#udp init
s = socket(AF_INET,SOCK_DGRAM)  
s.bind((server['IP'], server['PORT']))
_thread.start_new_thread(fun_thread_quit_check, ())
_thread.start_new_thread(thread_udp_recv, ())



# Timer task
list_timer_task = [
{'name':'tx2_udp_send', 'enable':False, 'interval':1, 'countdown':1, 'callback':tx2_udp_send, 'arg':msg_list[0]},
# {'name':'update_label_time', 'enable':False, 'interval':1, 'countdown':1, 'callback':fun_update_label_time},
# {'name':'change_volume_icon', 'enable':False, 'interval':2, 'countdown':2, 'callback':fun_change_volume_icon},
# {'name':'thread_quit_check', 'enable':False, 'interval':1, 'countdown':1, 'callback':fun_thread_quit_check}

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
                            print('task_arg_run')
                        else:
                            task['callback']()
                            print('task_noarg_run')

#state machine
def thread_tx2_state_machine():
    pass
    while param['thread_quit'] != True:
        time.sleep(0.02)
        if tx2_state == 'READY' :
            set_timer_task(0, True, False)
            pass
        elif tx2_state == 'IDLE' :
            set_timer_task(0, False, False)
            pass
        elif tx2_state == 'RECORDING' :
            pass
        elif tx2_state == 'PAUSED' :
            pass
        elif tx2_state == 'END' :
            pass
    # 退出状态机，重置环境, 记录error log
    
    
tx2_state = 'READY'
_thread.start_new_thread(thread_tx2_state_machine, ())  
_thread.start_new_thread(thread_timer_task, ())  




root = tk.Tk()
root.config(width = 800, height = 600)

buttons = []
for i in range(len(msg_list)):
    buttons.append(Button(root, text=list(msg_list[i].keys())[0], command=lambda x=i: button_click(x)))
    buttons[i].place(x=50,y=50*i+100)



root.mainloop()
