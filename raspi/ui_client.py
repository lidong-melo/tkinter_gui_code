#!/usr/bin/python
#coding:utf-8

import tkinter as tk
from PIL import ImageTk, Image ## to use png format, import imageTK
from tkinter import Button, PhotoImage, Label, Canvas
import _thread
import time
import datetime



import platform_check
import shake_hand
import udp_client
import param
import error
import os

def fun_rotate_pic():
    while param.quit_msg['quit_flag'] == False:
        time.sleep(0.05)
        if param.ui_flag['loading_flag'] == True:
            try:
                photoimage_loading_spinner.paste(image_loading_spinner.rotate(param.param3['angle']))
                param.param3['angle'] += -20
                aaa.delete()
                aaa =canvas_meeting_start_loading.create_image(60, 60, image = photoimage_loading_spinner)
                
            except:
                pass

                
def change_all_widgets_bg(bg_color):
    ### change all widgets bg & activebg
    for widget in list_all_widgets:
        widget.config(bg = bg_color, borderwidth = 0, highlightthickness = 0)
        try:
            widget.config(activebackground = widget.cget('background'))
        except:
            pass


def button_click(button_id):
     if button_id == 'start_meeting':
        param.button_click['start_meeting'] = True
        pass
     elif button_id == 'end_meeting':
        param.button_click['end_meeting'] = True
        pass
     elif button_id == 'pause':
        param.button_click['pause'] = True
        pass
     elif button_id == 'resume':
        param.button_click['resume'] = True
        pass
     elif button_id == 'mute':
        param.button_click['mute'] = True
        pass
     elif button_id == 'unmute':
        param.button_click['unmute'] = True
        pass
     elif button_id == 'volume_up':
        param.button_click['volume_up'] = True
        pass
     elif button_id == 'volume_down':
        param.button_click['volume_down'] = True
        pass


        
            
def fun_update_ui(flag):
    if flag == 'set_to_ready':
        hide_widget_list(list_bootup_greeting_hide)
        show_widget_list(list_bootup_greeting_show)
        
    elif flag == 'set_to_idle':
        hide_widget_list(list_bootup_greeting_show)
        show_widget_list(list_home_show)
        
    elif flag == 'set_to_start_loading':
        show_widget_list(list_start_loading)
        param.ui_flag['loading_flag'] = True
        
    elif flag == 'set_to_recording':
        #fun_update_label_time()
        change_all_widgets_bg('#000000')
        show_widget_list(list_meeting_start_show)
        hide_widget_list(list_meeting_start_hide)
        param.ui_flag['loading_flag'] = False

    elif flag == 'set_to_end_loading':
        show_widget_list(list_end_loading)
        param.ui_flag['loading_flag'] = True 

    elif flag == 'set_to_end':
        change_all_widgets_bg('#000000')
        hide_widget_list(list_resume_hide)
        show_widget_list(list_meeting_end_show)
        hide_widget_list(list_meeting_end_hide)
        param.ui_flag['loading_flag'] = False           
        
    elif flag == 'set_to_vol_up':
        #volume_adjust_show
        label_volume.place(x = pos[id(label_volume)][2], y = pos[id(label_volume)][3])
        photoimage_button_volume_down.config(file = param.pic_path['volume_down'])
        photoimage_button_volume_up.config(file = param.pic_path['volume_up'])
        #param.param1['volume_adjust_timeout'] = 2
        
        set_timer_task(2, True, True)
        if param.param1['volume'] < 9:
            param.param1['volume'] += 1
            photo_path = param.pic_path['volume_'] + str(param.param1['volume']) + '.png'
            photoimage_label_volume.config(file = photo_path)
            
    elif flag == 'set_to_vol_down':
        #volume_adjust_show
        label_volume.place(x = pos[id(label_volume)][2], y = pos[id(label_volume)][3])
        photoimage_button_volume_down.config(file = param.pic_path['volume_down'])
        photoimage_button_volume_up.config(file = param.pic_path['volume_up'])
        #param.param1['volume_adjust_timeout'] = 2
        set_timer_task(2, True, True)
        if param.param1['volume'] > 0 :
            param.param1['volume'] -= 1
            photo_path = param.pic_path['volume_'] + str(param.param1['volume']) + '.png'
            photoimage_label_volume.config(file = photo_path)
            
    elif flag == 'set_to_pause':
        show_widget_list(list_pause_show)
        hide_widget_list(list_pause_hide)
        change_all_widgets_bg('#541F1F')
        
    elif flag == 'set_to_resume':
        show_widget_list(list_resume_show)
        hide_widget_list(list_resume_hide)
        change_all_widgets_bg('#000000')
        
    elif flag == 'set_to_mute':
        show_widget_list(list_mute_show)
        hide_widget_list(list_mute_hide)
        
    elif flag == 'set_to_unmute':
        show_widget_list(list_unmute_show)
        hide_widget_list(list_unmute_hide)
    elif flag == 'set_to_wifi':
        if param.param1['rssi'].isdigit():
            rssi_value = int(param.param1['rssi'])
        if rssi_value < 40 :
            photo_path = param.pic_path['wifi_'] +'strong.png'
        elif rssi_value < 60 :
            photo_path = param.pic_path['wifi_'] +'medium.png'
        elif rssi_value < 255:
            photo_path = param.pic_path['wifi_'] +'low.png'
        else:
            photo_path = param.pic_path['wifi_'] +'off.png'
        photoimage_label_wifi.config(file = photo_path)
    else:
        pass
    
            

def show_widget_list(widget_list):
    for widget in widget_list:
        widget.place(x = pos[id(widget)][2], y = pos[id(widget)][3])


def hide_widget_list(widget_list):
    for widget in widget_list:
        widget.place_forget()


def fun_change_volume_icon():
    print('change_volume')
    try:
        #volume_adjust_hide
        label_volume.place_forget()
        photoimage_button_volume_down.config(file = param.param1['volume_down_inactive'])
        photoimage_button_volume_up.config(file = param.param1['volume_up_inactive'])    
    except:
        pass
        list_timer_task[2]['enable'] = False

                
def fun_thread_quit_check():
    # if ui quit, tell other threads to quit
    try:
        root.cget('bg')
    except:
        print('quit')
        param.quit_msg['quit_flag'] = True
                
def fun_update_label_time():
    ## label time
    if param.state['raspi_state'] == 'PAUSED':
        param.param3['pause_time'] += 1#这个方案可能会导致多减1秒，待后续单独开启线程任务可以解决
    if param.state['raspi_state'] == 'RECORDING':
        param.param3['new_time'] = datetime.datetime.now()
        time_delta = param.param3['new_time'] - param.param3['old_time'] 
        m, s = divmod(time_delta.seconds - param.param3['pause_time'], 60)
        h, m = divmod(m, 60)
        param.param3['time_str'] = '{0:02d} : {1:02d} : {2:02d}'.format(h, m, s)
        try:
            label_time.config(text = param.param3['time_str'])
        except:
            pass          



def set_timer_task(task_id, enable, reset):
    list_timer_task[task_id]['enable'] = enable
    if reset == True:# 重置时间
        list_timer_task[task_id]['countdown'] = list_timer_task[task_id]['interval']



def thread_timer_task():
    while param.quit_msg['quit_flag'] == False :
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
                        
def raspi_state_watch_dog():
    print('state-->raspi:',param.state['raspi_state'], 'tx2:',param.msg_from_tx2['tx2_state'])
    if param.state['raspi_state'] == param.msg_from_tx2['tx2_state']:
        param.msg_from_tx2['tx2_state'] = 'READY'
        param.watch_dog['timeout'] = param.watch_dog['interval']
    elif param.watch_dog['timeout'] > 0:
        param.watch_dog['timeout'] -= 1
    else:
        print("------------------------ a ----------------------")
        param.watch_dog['watch_dog_timeout'] = param.watch_dog['interval']
        param.state['reset_raspi_state'] = True


def thread_update_timeout():
    while param.quit_msg['quit_flag'] == False:
        time.sleep(1)
        for key, value in param.timeout.items():
            if value > 0:
                param.timeout[key] -= 1
        pass

        
# Timer task   
list_timer_task = [
{'name':'udp_send_msg', 'enable':False, 'interval':1, 'countdown':1, 'callback':udp_client.send_msg, 'arg':param.msg_to_tx2[0]},#0
{'name':'update_label_time', 'enable':False, 'interval':1, 'countdown':1, 'callback':fun_update_label_time},#1
{'name':'change_volume_icon', 'enable':False, 'interval':2, 'countdown':2, 'callback':fun_change_volume_icon},#2
{'name':'thread_quit_check', 'enable':False, 'interval':1, 'countdown':1, 'callback':fun_thread_quit_check},#3
{'name':'send_msg_raspi_status', 'enable':False, 'interval':3, 'countdown':3, 'callback':udp_client.send_msg, 'arg':param.state},#4
{'name':'raspi_state_watch_dog', 'enable':False, 'interval':1, 'countdown':1, 'callback':raspi_state_watch_dog},#5
]


def thread_UI_update(): 
    while param.quit_msg['quit_flag'] == False:
        time.sleep(0.02)
        #vol button
        if param.button_click['volume_down'] == True:#vol- button click
            param.button_click['volume_down'] = False
            fun_update_ui('set_to_vol_down')
            param.msg_to_tx2[7]['VOLUME_IS_DOWN'] = param.param1['volume']
            udp_client.send_msg(param.msg_to_tx2[7])

        if param.button_click['volume_up'] == True:#vol+ button click
            param.button_click['volume_up'] = False
            fun_update_ui('set_to_vol_up')
            param.msg_to_tx2[6]['VOLUME_IS_UP'] = param.param1['volume']
            udp_client.send_msg(param.msg_to_tx2[6])
        #mute button    
        if param.button_click['mute'] == True:#mute button click
            param.button_click['mute'] = False
            fun_update_ui('set_to_mute')
            udp_client.send_msg(param.msg_to_tx2[8])
        
        if param.button_click['unmute'] == True:#unmute button click
            param.button_click['unmute'] = False
            fun_update_ui('set_to_unmute')
            udp_client.send_msg(param.msg_to_tx2[9])
        #wifi icon
        if param.msg_from_tx2['WIFI_RSSI'] != -1:# tx2 报错
            print('rssi:',param.msg_from_tx2['WIFI_RSSI'])
            param.param1['rssi'] = param.msg_from_tx2['WIFI_RSSI']
            param.msg_from_tx2['WIFI_RSSI'] = -1
            param.msg_to_tx2[11]['WIFI_RSSI'] = param.param1['rssi']
            fun_update_ui('set_to_wifi')
            udp_client.send_msg(param.msg_to_tx2[11])
        
        #error icon
        if param.msg_from_tx2['ERROR_CODE'] != 0:# tx2 报错
            param.msg_from_tx2['ERROR_CODE'] = 0
            error.error_handler('ERROR_CODE_TX2_ERROR')
            param.msg_to_tx2[5]['ERROR_CODE'] = 0
            udp_client.send_msg(param.msg_to_tx2[5])
                
    
        
        
        
#会议状态相关
def thread_state_machine():
    while param.quit_msg['quit_flag'] == False:
        time.sleep(0.02)
        
        if param.state['reset_raspi_state'] == True:
            param.state['reset_raspi_state'] = False
            param.state['raspi_state'] = 'RESET'
        
        #ready   
        if param.state['raspi_state'] == 'READY':
            #list_timer_task[0]['enable'] = True # 开启udp_send任务
            set_timer_task(0, True, False)
            if param.timeout['bootup_greeting_timeout'] == 0:
                error.error_handler('ERROR_CODE_READY_TIMEOUT')# timeout, report error
                
                ## just for debug #调试用，后续删掉
                param.state['raspi_state'] = 'IDLE'
                print(param.state['raspi_state'])
                fun_update_ui('set_to_idle')

            elif param.msg_from_tx2['SYSTEM_IS_READY'] == True:#recv msg from tx2
                param.msg_from_tx2['SYSTEM_IS_READY'] = False
                param.state['raspi_state'] = 'IDLE'
                print(param.state['raspi_state'])
                fun_update_ui('set_to_idle')

        #idle
        elif param.state['raspi_state'] == 'IDLE':
            # 按键启动会议
            set_timer_task(0, False, False)
            if param.button_click['start_meeting'] == True:#start button click
                param.button_click['start_meeting'] = False
                #param.timeout['START_LOADING'] = 3
                param.state['raspi_state'] = 'START_LOADING'
                print(param.state['raspi_state'])
                udp_client.send_msg(param.msg_to_tx2[1])
                fun_update_ui('set_to_start_loading')

        #start loading
        elif param.state['raspi_state'] == 'START_LOADING':
            if param.timeout['START_LOADING'] == 0:
                error.error_handler('ERROR_CODE_START_MEETING_TIMEOUT')# timeout, report error
                
                ##--> just for debug #调试用，后续删掉
                param.state['raspi_state'] = 'RECORDING'
                print(param.state['raspi_state'])
                param.param3['old_time'] = datetime.datetime.now()
                param.param3['new_time'] = param.param3['old_time']
                param.param3['pause_time'] = 0
                param.param3['time_str'] = '00 : 00 : 00'
                fun_update_ui('set_to_recording')
                ##<--
            elif param.msg_from_tx2['MEETING_IS_RECORDING'] == True:#recv msg from tx2
                param.msg_from_tx2['MEETING_IS_RECORDING'] = False
                param.state['raspi_state'] = 'RECORDING'
                print(param.state['raspi_state'])
                fun_update_ui('set_to_recording')
                ## initial time
                param.param3['old_time'] = datetime.datetime.now()
                param.param3['new_time'] = param.param3['old_time']
                param.param3['pause_time'] = 0
                param.param3['time_str'] = '00 : 00 : 00'

        #recording        
        elif param.state['raspi_state'] == 'RECORDING':
            set_timer_task(1, True, False)
            if param.msg_from_tx2['TX2_END_MEETING'] == True:# 15m no-face detect tx2 end meeting
                param.msg_from_tx2['TX2_END_MEETING'] = False
                #param.timeout['END_LOADING'] = 3
                param.state['raspi_state'] = 'END_LOADING'
                print(param.state['raspi_state'])
                udp_client.send_msg(param.msg_to_tx2[2])
                fun_update_ui('set_to_end_loading')
                
            if param.button_click['end_meeting'] == True:#end button click
                param.button_click['end_meeting'] = False
                #param.timeout['END_LOADING'] = 3
                param.state['raspi_state'] = 'END_LOADING'
                print(param.state['raspi_state'])
                udp_client.send_msg(param.msg_to_tx2[2])
                fun_update_ui('set_to_end_loading')
            
            if param.button_click['pause'] == True:#pause button click
                param.button_click['pause'] = False
                udp_client.send_msg(param.msg_to_tx2[3])
                param.state['raspi_state'] = 'PAUSED'
                print(param.state['raspi_state'])
                fun_update_ui('set_to_pause')
            
        #paused
        elif param.state['raspi_state'] == 'PAUSED':
            if param.msg_from_tx2['TX2_END_MEETING'] == True:# 15m no-face detect tx2 end meeting
                param.msg_from_tx2['TX2_END_MEETING'] = False
                #param.timeout['END_LOADING'] = 3
                param.state['raspi_state'] = 'END_LOADING'
                udp_client.send_msg(param.msg_to_tx2[2])
                fun_update_ui('set_to_end_loading')
                
            if param.button_click['end_meeting'] == True:#end button click
                param.button_click['end_meeting'] = False
                #param.timeout['END_LOADING'] = 3
                param.state['raspi_state'] = 'END_LOADING'
                udp_client.send_msg(param.msg_to_tx2[2])
                fun_update_ui('set_to_end_loading')

            if param.button_click['resume'] == True:#resume button click
                param.button_click['resume'] = False
                param.state['raspi_state'] = 'RECORDING'
                udp_client.send_msg(param.msg_to_tx2[4])
                fun_update_ui('set_to_resume')      
        
        #end loading
        elif param.state['raspi_state'] == 'END_LOADING':
            if param.timeout['END_LOADING'] == 0:
                error.error_handler('ERROR_CODE_END_MEETING_TIMEOUT')# timeout, report error
                
                ##--> just for debug #调试用，后续删掉
                param.state['raspi_state'] = 'END'
                fun_update_ui('set_to_end')
                ##<--
            elif param.msg_from_tx2['MEETING_IS_END'] == True:#recv msg from tx2
                param.msg_from_tx2['MEETING_IS_END'] = False
                param.state['raspi_state'] = 'END'
                fun_update_ui('set_to_end')
                
        elif param.state['raspi_state'] == 'END':
            set_timer_task(1, False, False)#end meeting
            param.state['raspi_state'] = 'IDLE'
            fun_update_ui('set_to_idle')
            # 清空之前的按键事件缓存
            for key, value in param.button_click.items():
                param.button_click[key] = False
                
        elif param.state['raspi_state'] == 'RESET':
            fun_update_ui('set_to_ready')
            # 清空之前的按键事件缓存
            for key, value in param.button_click.items():
                param.button_click[key] = False
            param.state['raspi_state'] = 'READY'
            
        else:
            error.error['error_code'] = error.error_code_list['ERROR_CODE_STATE_UNKNOWN']
            pass
            

            



#ui init
root = tk.Tk()
root.config(width = 320, height = 240, bg='black')

## 顺序不能调整，因为有图层index的逻辑关系
photoimage_label_bootup_greeting = PhotoImage(file= param.pic_path['bootup_greeting'])
label_bootup_greeting =  Label(root, text="OK", image = photoimage_label_bootup_greeting, bg = 'black')

photoimage_label_wifi = PhotoImage(file= param.pic_path['wifi_off'])
label_wifi = Label(root, text="OK", image = photoimage_label_wifi)


photoimage_button_mute = PhotoImage(file= param.pic_path['button_mute'])
button_mute = Button(root, text="OK", command=lambda: button_click(button_id= 'mute'), image = photoimage_button_mute, bg='black')

photoimage_button_unmute = PhotoImage(file= param.pic_path['button_unmute'])
button_unmute = Button(root, text="OK", command=lambda: button_click(button_id= 'unmute'), image = photoimage_button_unmute, bg='black')



photoimage_label_muted = PhotoImage(file= param.pic_path['label_muted'])
label_muted = Label(root, text="OK", image = photoimage_label_muted)


photoimage_button_volume_down = PhotoImage(file= param.pic_path['volume_down_inactive'])
button_volume_down = Button(root, text="OK", command=lambda: button_click(button_id= 'volume_down'), image = photoimage_button_volume_down)

photoimage_button_volume_up = PhotoImage(file=param.pic_path['volume_up_inactive'])
button_volume_up = Button(root, text="OK", command=lambda: button_click(button_id= 'volume_up'), image = photoimage_button_volume_up)


photoimage_label_volume = PhotoImage(file=param.pic_path['volume_']+'5.png')
label_volume = Label(root, text="OK", image = photoimage_label_volume)


photoimage_button_pause = PhotoImage(file=param.pic_path['button_pause'])
button_pause = Button(root, text="OK", command=lambda: button_click(button_id= 'pause'), image = photoimage_button_pause)


photoimage_button_resume = PhotoImage(file=param.pic_path['button_resume'])
button_resume = Button(root, text="OK", command=lambda: button_click(button_id= 'resume'), image = photoimage_button_resume)


label_time = Label(root, text="00 : 00 : 00", font='Arial 9 bold', fg = 'white')


#photoimage_label_error = PhotoImage(file="icons/error_01.png")
#label_error = Label(root, text="OK", image = photoimage_label_error)
label_error = Label(root, text="01", font='Arial 10 bold', bg = 'red', fg = 'white')



photoimage_button_end = PhotoImage(file=param.pic_path['button_end_meeting'])
button_meeting_end = Button(root, text="OK", command=lambda: button_click(button_id= 'end_meeting'), image = photoimage_button_end)

photoimage_button_start = PhotoImage(file=param.pic_path['button_start_meeting'])
button_meeting_start = Button(root, text="OK", command=lambda: button_click(button_id= 'start_meeting'), image = photoimage_button_start)


##photoimage_label_loading_spinner_background = PhotoImage(file="icons/loading_spinner_background.png")
##label_loading_spinner_background = Label(root, text="OK", image = photoimage_label_loading_spinner_background)
##
##photoimage_label_loading_spinner = PhotoImage(file="icons/loading_spinner.png")
##label_loading_spinner = Label(root, text="OK", image = photoimage_label_loading_spinner)

canvas_meeting_start_loading= Canvas(root, width=120, height=120)
canvas_meeting_end_loading= Canvas(root, width=64, height=64)

pos = {
## 顺序为 width，height，x，y
id(label_wifi): [18, 18, 151, 5],
id(button_volume_down): [50, 50, 36, 96],
id(button_volume_up): [50, 50, 234, 96],
id(button_mute): [50, 50, 135, 24],
id(button_unmute): [50, 50, 135, 24],
id(label_muted): [64, 16, 128, 69],
id(button_meeting_start): [120, 120, 100, 60],
id(button_meeting_end): [64, 64, 128, 88],
id(button_pause): [50, 45, 135, 166],
id(button_resume): [50, 45, 135, 166],
id(label_volume): [200, 84, 60, 138],
id(label_error): [18, 18, 146, 222],
id(label_time): [128, 16, 130, 156],
id(label_bootup_greeting):[200, 84, 60, 78],
id(canvas_meeting_start_loading):[120, 120, 100, 60],
id(canvas_meeting_end_loading):[64, 64, 128, 88],
}

## list of show & hide

list_all_widgets = [root, label_wifi, button_mute, button_unmute, label_muted, button_pause, label_volume, button_meeting_end, button_volume_down, button_volume_up,  button_resume, button_meeting_start, label_error, label_time, canvas_meeting_start_loading, canvas_meeting_end_loading]

list_bootup_greeting_show = [label_bootup_greeting]
list_bootup_greeting_hide = [label_wifi, button_mute, button_unmute, label_muted, button_pause, label_volume, button_meeting_end, button_volume_down, button_volume_up,  button_resume, button_meeting_start, label_error, label_time, canvas_meeting_start_loading, canvas_meeting_end_loading]

list_meeting_start_show = [button_mute, button_meeting_end, button_pause, label_time]
list_meeting_start_hide = [canvas_meeting_start_loading, label_bootup_greeting, button_unmute,  label_muted, button_resume, button_meeting_start]

list_meeting_end_show = [button_meeting_start]
list_meeting_end_hide = [canvas_meeting_end_loading, button_unmute, label_muted, button_resume, button_mute, button_meeting_end, button_pause, label_time]

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

list_home_show = [label_wifi, button_volume_down, button_volume_up, button_meeting_start]

list_start_loading = [canvas_meeting_start_loading]
list_end_loading = [canvas_meeting_end_loading]

    

### change widget background color
change_all_widgets_bg('#000000')


# get current time
param.param3['old_time'] = datetime.datetime.now()
param.param3['new_time'] = param.param3['old_time']



platform_check.init(root)

# 透明loading控件
image_loading_spinner = Image.open(param.pic_path['loading_spinner'])
image_loading_spinner_background = Image.open(param.pic_path['loading_spinner_background'])
photoimage_loading_spinner = ImageTk.PhotoImage(image_loading_spinner)
photoimage_loading_spinner_background = ImageTk.PhotoImage(image_loading_spinner_background)
canvas_meeting_start_loading.create_image(60, 60, image = photoimage_button_start)
canvas_meeting_start_loading.create_image(60, 60, image = photoimage_loading_spinner_background)
canvas_meeting_start_loading.create_image(60, 60, image = photoimage_loading_spinner)

canvas_meeting_end_loading.create_image(32, 32, image = photoimage_button_end)
canvas_meeting_end_loading.create_image(32, 32, image = photoimage_loading_spinner_background)
canvas_meeting_end_loading.create_image(32, 32, image = photoimage_loading_spinner)



_thread.start_new_thread(fun_rotate_pic, ())
_thread.start_new_thread(thread_state_machine, ())

_thread.start_new_thread(thread_update_timeout, ())

_thread.start_new_thread(thread_timer_task, ())
_thread.start_new_thread(thread_UI_update, ())


set_timer_task(3, True, True) #thread_quit_check
set_timer_task(4, True, True) #loop send state 
set_timer_task(5, True, True) #raspi state watch dog

fun_update_ui('set_to_ready')



root.mainloop()







# class motion_image:
    # def __init__(self, width, height, image_list):
        # self.width = width
        # self.height = height
        # self.image_list = image_list
    # def image_init(self):
        # canvas_widget = Canvas(root, width = self.width, height = self.height)
        # for image_url in self.image_list:
            # image_widget = Image.open(image_url)
            # photoimage_widget = ImageTk.PhotoImage(image_widget)
            # canvas_widget.create_image(self.width/2, self.height/2, image=photoimage_widget)
        # canvas_widget.place(x = 0,y = 0)
    
    # def rotate(self):
        # while param.quit_msg['quit_flag'] == False:
            # time.sleep(0.05)
            # if param.ui_flag['loading_flag'] == True:
                # try:
                    # photoimage_widget.paste(image_widget.rotate(param.param3['angle']))
                    # param.param3['angle'] += -20
                    # aaa.delete()
                    # aaa = canvas_widget.create_image(self.width/2, self.height/2, image = photoimage_widget)
                    
                # except:
                    # pass
# #list_temp = [1,2,3]
# list_temp = [param.pic_path['button_start_meeting'], param.pic_path['loading_spinner_background'], param.pic_path['loading_spinner']]
# start_loading_gif = motion_image(120, 120, list_temp)
# start_loading_gif.image_init()

