#!/usr/bin/python3
#coding:utf-8

import param_host
import os
    
import datetime
import time
import _thread
import msg_list
import wifi
import udp_host
import subprocess
import serial_host
#import psutil
#import serial
import rpc_caller



# def fun_thread_quit_check():
# # if ui quit, tell other threads to quit
    # try:
        # pass
        # time.sleep(1)
        # # if param_host.param1['display'] == True:
            # # root.cget('bg')
    # except:
        # param_host.flag['thread_quit'] = True
        # s.close()

    
    
    
def tx2_status_watch_dog():
    #print('state-->raspi:',msg_list.msg_from_raspi['raspi_state'], 'tx2:',param_host.state['tx2_state'])
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
#{'name':'thread_quit_check', 'enable':False, 'interval':1, 'countdown':1, 'callback':fun_thread_quit_check},#3
#{'name':'update_label_status', 'enable':False, 'interval':1, 'countdown':1, 'callback':update_label_status, 'arg':param_host.state},#4
{'name':'tx2_status_watch_dog', 'enable':False, 'interval':1, 'countdown':1, 'callback':tx2_status_watch_dog},#3
]

def set_timer_task(task_id, enable, reset):
    list_timer_task[task_id]['enable'] = enable
    if reset == True:# 重置时间
        list_timer_task[task_id]['countdown'] = list_timer_task[task_id]['interval']


def thread_get_rssi():
#time cost is 1.71s, need sudo, otherwise it would be fail and the time cost is 17ms
    while param_host.flag['thread_quit'] != True: 
        # time cost is 17ms
        rssi = wifi.get_rssi()
        
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

                            

def start_new_meeting():
#time cost is 1.71s, need sudo, otherwise it would be fail and the time cost is 17ms
    pid = find_meeting_process()
    if pid == 0:
        #serial_host.serial_reset()
        #time.sleep(0.1)
        try:
            proc = subprocess.Popen(['/home/nvidia/melo-device-demo/bin/melo-mvp', '-upload', '-fusion_log'], cwd='/home/nvidia/melo-device-demo/bin/', env=dict(os.environ, DISPLAY=':0',XAUTHORITY='/home/nvidia/.Xauthority'))
            time.sleep(2)
            print('~~~~time delay 2s')
        except:
            #开启失败
            pid = -2
            pass
    return pid


def find_meeting_process():
    try:
        # time cost 0.03s
        res = subprocess.Popen('ps -ef | grep melo-mvp',stdout=subprocess.PIPE,shell=True)
        output_lines = res.stdout.readlines()
        for line in output_lines:
            if str(line).find('grep') == -1:
                arr = str(line).split()
                #print('pid =',int(arr[1]))
                return int(arr[1])
        return 0
    except:
        return -1
       

def end_meeting():
    error_code = 0
    try:
        print('~~~~~~~~~~~~~~~~~~~~~~try to stop')
        pid_to_kill = find_meeting_process()
        if pid_to_kill == 0:
            print("can't find meeting process")
        elif pid_to_kill == -1:
            print('error when list task')
        else:
            command = 'kill ' + str(pid_to_kill)
            print('command:',command)
            os.system(command)
            #print('~~~~~~~~~~~~~~~~~~~~~~stop ok')
            #time.sleep(2)
            retry  = 0
            while 1:
                time.sleep(0.5)
                pid_to_kill = find_meeting_process()
                if pid_to_kill == 0:
                    print("meeting is stop")
                    break
                else:
                    print('meeting is still alive-----',retry)
                retry += 1
                if retry > 20:
                    break
                
            print('~~delay 2s')
    except:
        return error_code
        



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
        time.sleep(0.05)
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
                err = start_new_meeting()
                if err == -1:
                    print('list task error')
                elif err == -2:
                    print('launch app error')
                elif err == 0:
                    print('launch meeting ok')
                else:
                    print('another meeting is running!!!!!!!!!')
                
                if err >= 0:
                    param_host.state['tx2_state'] = 'RECORDING'
                    serial_host.serial_send_cmd('led on\n')
                    #serial_host.serial_send('led on\n')
                    time.sleep(0.1)
                    udp_host.tx2_udp_send(msg_list.msg_to_raspi[1])
                else:
                    param_host.state['tx2_state'] = 'RESET'
                
        elif param_host.state['tx2_state'] == 'RECORDING' :
            pid = find_meeting_process()
            if pid == 0:
                set_timer_task(1, True, False)#end meeting
            elif pid == -1:
                print('error should output')
            else:
                pass
                #print('meeting is alive')
            if msg_list.msg_from_raspi['MEETING_IS_ENDING'] == True:
                msg_list.msg_from_raspi['MEETING_IS_ENDING'] = False
                param_host.state['tx2_state'] = 'END'           
            if msg_list.msg_from_raspi['MEETING_IS_PAUSING'] == True:
                msg_list.msg_from_raspi['MEETING_IS_PAUSING'] = False 
                #proc = subprocess.Popen(['/home/nvidia/melo-device-demo/bin/backend-test-client', 'pause'], cwd='/home/nvidia/melo-device-demo/bin/', env=dict(os.environ, DISPLAY=':0',XAUTHORITY='/home/nvidia/.Xauthority'))
                rpc_caller.rpc_pause()
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
                #proc = subprocess.Popen(['/home/nvidia/melo-device-demo/bin/backend-test-client', 'resume'], cwd='/home/nvidia/melo-device-demo/bin/', env=dict(os.environ, DISPLAY=':0',XAUTHORITY='/home/nvidia/.Xauthority'))                         
                rpc_caller.rpc_resume()
                param_host.state['tx2_state'] = 'RECORDING'
                udp_host.tx2_udp_send(msg_list.msg_to_raspi[1])
                
        elif param_host.state['tx2_state'] == 'END' :#结束会议
            end_meeting()
            serial_host.serial_send_cmd('led off\n')
            #serial_host.serial_send('led off\n')
            time.sleep(0.1)
            set_timer_task(1, False, False)#end meeting 
            udp_host.tx2_udp_send(msg_list.msg_to_raspi[4])
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
#set_timer_task(3, True, True)#thread_quit_check 
#set_timer_task(4, True, True)#update label_status
set_timer_task(3, True, True)#tx2_status_watch_dog
#serial_host.serial_init()
#_thread.start_new_thread(serial_host.thread_serial_recv, ())
#serial_send('tx2 ready!\n')
#serial_send('tx2 ready!\n')

#serial_host.serial_reset()

#main loop
while 1:
    time.sleep(10)
    pass
#serial_host.serial_uninit()
