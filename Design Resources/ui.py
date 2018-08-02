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
        show_widget_list(list_bootup_greeting_show)
        
    elif flag == 'set_to_idle':
        hide_widget_list(list_bootup_greeting_show)
        show_widget_list(list_home_show)
        
    elif flag == 'set_to_start_loading':
        show_widget_list(list_start_loading)
        param.ui_flag['loading_flag'] = True
        
    elif flag == 'set_to_started':
        fun_update_label_time()
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
        param.param1['volume_adjust_timeout'] = 2
        if param.param1['volume'] < 9:
            param.param1['volume'] += 1
            photo_path = param.pic_path['volume_'] + str(param.param1['volume']) + '.png'
            photoimage_label_volume.config(file = photo_path)
            
    elif flag == 'set_to_vol_down':
        #volume_adjust_show
        label_volume.place(x = pos[id(label_volume)][2], y = pos[id(label_volume)][3])
        photoimage_button_volume_down.config(file = param.pic_path['volume_down'])
        photoimage_button_volume_up.config(file = param.pic_path['volume_up'])
        param.param1['volume_adjust_timeout'] = 2
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
    
    else:
        pass
    
            

def show_widget_list(widget_list):
    for widget in widget_list:
        widget.place(x = pos[id(widget)][2], y = pos[id(widget)][3])


def hide_widget_list(widget_list):
    for widget in widget_list:
        widget.place_forget()

def fun_change_volume_icon():
    if param.param1['volume_adjust_timeout'] > 0:
        param.param1['volume_adjust_timeout'] -= 1
        if param.param1['volume_adjust_timeout'] == 0:
            try:
                #volume_adjust_hide
                label_volume.place_forget()
                photoimage_button_volume_down.config(file = param.param1['volume_down_inactive'])
                photoimage_button_volume_up.config(file = param.param1['volume_up_inactive'])    
            except:
                pass
                
def fun_thread_quit_check():
    # if ui quit, tell other threads to quit
    try:
        label_quit.cget('text')
    except:
        print('quit')
        param.quit_msg['quit_flag'] = True
        pass
                
def fun_update_label_time():
    ## label time
    if param.param3['meeting_status'] == 'PAUSED':
        param.param3['pause_time'] += 1#这个方案可能会导致多减1秒，待后续单独开启线程任务可以解决
    if param.param3['meeting_status'] == 'STARTED':
        param.param3['new_time'] = datetime.datetime.now()
        time_delta = param.param3['new_time'] - param.param3['old_time'] 
        m, s = divmod(time_delta.seconds - param.param3['pause_time'], 60)
        h, m = divmod(m, 60)
        param.param3['time_str'] = '{0:02d} : {1:02d} : {2:02d}'.format(h, m, s)
        try:
            label_time.config(text = param.param3['time_str'])
        except:
            pass          

    
            

def thread_update_ui():
    while param.quit_msg['quit_flag'] == False :
        time.sleep(1)# 1 second timer
        fun_thread_quit_check()
        fun_change_volume_icon()
        fun_update_label_time()
        # in mode ready: every second send ready to tx2
        if param.param3['meeting_status'] == 'READY':
            udp_client.send_msg('RASPI_IS_READY')



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


def thread_update_timeout():
    while param.quit_msg['quit_flag'] == False:
        time.sleep(1)
        for key, value in param.timeout.items():
            if value > 0:
                param.timeout[key] -= 1
        pass



def thread_state_machine():
    while param.quit_msg['quit_flag'] == False:
        time.sleep(0.02)
        
        if param.tx2_ack['ERROR_CODE'] != 0:# tx2 报错
            param.tx2_ack['ERROR_CODE'] = 0
            error.error_handler('ERROR_CODE_TX2_ERROR')
        
        #button
        if param.button_click['volume_down'] == True:#vol- button click
            param.button_click['volume_down'] = False
            fun_update_ui('set_to_vol_down')

        if param.button_click['volume_up'] == True:#vol+ button click
            param.button_click['volume_up'] = False
            fun_update_ui('set_to_vol_up')
            
        if param.button_click['mute'] == True:#vol+ button click
            param.button_click['mute'] = False
            fun_update_ui('set_to_mute')
            udp_client.send_msg(param.msg)
        
        if param.button_click['unmute'] == True:#vol+ button click
            param.button_click['unmute'] = False
            fun_update_ui('set_to_unmute')
            udp_client.send_msg(param.msg)
        
        
        #ready
        if param.param3['meeting_status'] == 'READY':
            if param.timeout['bootup_greeting_timeout'] == 0:
                error.error_handler('ERROR_CODE_READY_TIMEOUT')# timeout, report error
                
                ## just for debug #调试用，后续删掉
                param.param3['meeting_status'] = 'IDLE'
                fun_update_ui('set_to_idle')

            elif param.tx2_ack['SYSTEM_IS_READY'] == True:#recv msg from tx2
                param.tx2_ack['SYSTEM_IS_READY'] = False
                param.param3['meeting_status'] = 'IDLE'
                fun_update_ui('set_to_idle')

                
        #idle
        elif param.param3['meeting_status'] == 'IDLE':
            # 按键启动会议
            if param.button_click['start_meeting'] == True:#start button click
                param.button_click['start_meeting'] = False
                #param.timeout['START_LOADING'] = 3
                param.param3['meeting_status'] = 'START_LOADING'
                udp_client.send_msg(param.msg)
                fun_update_ui('set_to_start_loading')

        #start loading
        elif param.param3['meeting_status'] == 'START_LOADING':
            if param.timeout['START_LOADING'] == 0:
                error.error_handler('ERROR_CODE_START_MEETING_TIMEOUT')# timeout, report error
                
                ##--> just for debug #调试用，后续删掉
                param.param3['meeting_status'] = 'STARTED'
                param.param3['old_time'] = datetime.datetime.now()
                param.param3['new_time'] = param.param3['old_time']
                param.param3['pause_time'] = 0
                param.param3['time_str'] = '00 : 00 : 00'
                fun_update_ui('set_to_started')
                ##<--
            elif param.tx2_ack['MEETING_IS_STARTED'] == True:#recv msg from tx2
                param.tx2_ack['MEETING_IS_STARTED'] = False
                param.param3['meeting_status'] = 'STARTED'
                fun_update_ui('set_to_started')
                ## initial time
                param.param3['old_time'] = datetime.datetime.now()
                param.param3['new_time'] = param.param3['old_time']
                param.param3['pause_time'] = 0
                param.param3['time_str'] = '00 : 00 : 00'

        #started        
        elif param.param3['meeting_status'] == 'STARTED':
            if param.tx2_ack['TX2_END_MEETING'] == True:# 15m no-face detect tx2 end meeting
                param.tx2_ack['TX2_END_MEETING'] = False
                #param.timeout['END_LOADING'] = 3
                param.param3['meeting_status'] = 'END_LOADING'
                udp_client.send_msg(param.msg)
                fun_update_ui('set_to_end_loading')
                
            if param.button_click['end_meeting'] == True:#end button click
                param.button_click['end_meeting'] = False
                #param.timeout['END_LOADING'] = 3
                param.param3['meeting_status'] = 'END_LOADING'
                udp_client.send_msg(param.msg)
                fun_update_ui('set_to_end_loading')
            
            if param.button_click['pause'] == True:#pause button click
                param.button_click['pause'] = False
                udp_client.send_msg(param.msg)
                param.param3['meeting_status'] = 'PAUSED'
                fun_update_ui('set_to_pause')
            
        #paused
        elif param.param3['meeting_status'] == 'PAUSED':
            if param.tx2_ack['TX2_END_MEETING'] == True:# 15m no-face detect tx2 end meeting
                param.tx2_ack['TX2_END_MEETING'] = False
                #param.timeout['END_LOADING'] = 3
                param.param3['meeting_status'] = 'END_LOADING'
                udp_client.send_msg(param.msg)
                fun_update_ui('set_to_end_loading')
                
            if param.button_click['end_meeting'] == True:#end button click
                param.button_click['end_meeting'] = False
                #param.timeout['END_LOADING'] = 3
                param.param3['meeting_status'] = 'END_LOADING'
                udp_client.send_msg(param.msg)
                fun_update_ui('set_to_end_loading')

            if param.button_click['resume'] == True:#resume button click
                param.button_click['resume'] = False
                param.param3['meeting_status'] = 'STARTED'
                udp_client.send_msg(param.msg)
                fun_update_ui('set_to_resume')      
        
        #end loading
        elif param.param3['meeting_status'] == 'END_LOADING':
            if param.timeout['END_LOADING'] == 0:
                error.error_handler('ERROR_CODE_END_MEETING_TIMEOUT')# timeout, report error
                
                ##--> just for debug #调试用，后续删掉
                param.param3['meeting_status'] = 'END'
                fun_update_ui('set_to_end')
                ##<--
            elif param.tx2_ack['MEETING_IS_END'] == True:#recv msg from tx2
                param.tx2_ack['MEETING_IS_END'] = False
                param.param3['meeting_status'] = 'END'
                fun_update_ui('set_to_end')
                
        elif param.param3['meeting_status'] == 'END':
            param.param3['meeting_status'] = 'IDLE'
            fun_update_ui('set_to_idle')
            # 清空之前的按键事件缓存
            for key, value in param.button_click.items():
                param.button_click[key] = False
        
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

label_quit = Label(root, text='hi')

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
id(button_pause): [50, 50, 135, 166],
id(button_resume): [50, 50, 135, 166],
id(label_volume): [200, 84, 60, 138],
id(label_error): [18, 18, 146, 222],
id(label_time): [128, 16, 130, 156],
id(label_bootup_greeting):[200, 84, 60, 78],
id(canvas_meeting_start_loading):[120, 120, 100, 60],
id(canvas_meeting_end_loading):[64, 64, 128, 88],
id(label_quit):[0,0,0,0]
}

## list of show & hide

list_all_widgets = [root, label_wifi, button_mute, button_unmute, label_muted, button_pause, label_volume, button_meeting_end, button_volume_down, button_volume_up,  button_resume, button_meeting_start, label_error, label_time, canvas_meeting_start_loading, canvas_meeting_end_loading]

list_bootup_greeting_show = [label_bootup_greeting]


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

    

### widget place
change_all_widgets_bg('#000000')




# get current time
param.param3['old_time'] = datetime.datetime.now()
param.param3['new_time'] = param.param3['old_time']


# get thread update ui
_thread.start_new_thread(thread_update_ui, ())


_thread.start_new_thread(shake_hand.thread_run, ())


platform_check.init(root)

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


fun_update_ui('set_to_ready')



root.mainloop()







##class class_loading_image():
##    def fun_rotate_pic():
##        while 1:
##            time.sleep(0.05)
##            try:
##                photoimage_loading_spinner.paste(image_loading_spinner.rotate(param.param3['angle']))
##                param.param3['angle'] += -20
##                aaa.delete()
##                aaa =canvas_meeting_start_loading.create_image(60, 60, image = photoimage_loading_spinner)
##                
##            except:
##                pass
##    canvas_meeting_start_loading= Canvas(root, width=120, height=120, borderwidth = 0, highlightthickness = 0, bg='black')
##    canvas_meeting_start_loading.create_image(60, 60, image = photoimage_button_start)
##    canvas_meeting_start_loading.create_image(60, 60, image = photoimage_loading_spinner_background)
##    canvas_meeting_start_loading.create_image(60, 60, image = photoimage_loading_spinner)
