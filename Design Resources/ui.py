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




def fun_meeting_ready():
    show_widget_list(list_bootup_greeting_show)
    pass

    
def fun_meeting_idle():
    hide_widget_list(list_bootup_greeting_show)
    show_widget_list(list_home_show)



def fun_meeting_start_loading():
    param.param3['meeting_status'] = 'START_LOADING'
    param.timeout['START_LOADING'] = 3
    show_widget_list(list_start_loading)
    udp_client.send_msg(param.msg)
    param.ui_flag['loading_flag'] = True
    pass
    

def fun_meeting_start():
    show_widget_list(list_meeting_start_show)
    hide_widget_list(list_meeting_start_hide)
    param.param3['meeting_status'] = 'STARTED'
    ## initial time
    param.param3['old_time'] = datetime.datetime.now()
    param.param3['new_time'] = param.param3['old_time']
    param.ui_flag['loading_flag'] = False
    pass


def fun_meeting_end():
    fun_resume()
    show_widget_list(list_meeting_end_show)
    hide_widget_list(list_meeting_end_hide)
    param.param3['time_str'] = '00 : 00 : 00'
    param.param3['meeting_status'] = 'END'
    pass


def fun_volume_up():
    #volume_adjust_show
    label_volume.place(x = pos[id(label_volume)][2], y = pos[id(label_volume)][3])
    photoimage_button_volume_down.config(file = param.pic_path['volume_down'])
    photoimage_button_volume_up.config(file = param.pic_path['volume_up'])
    param.param1['volume_adjust_timeout'] = 2
    if param.param1['volume'] < 9:
        param.param1['volume'] += 1
        photo_path = param.pic_path['volume_'] + str(param.param1['volume']) + '.png'
        photoimage_label_volume.config(file = photo_path)
    pass


def fun_volume_down():
    #volume_adjust_show
    label_volume.place(x = pos[id(label_volume)][2], y = pos[id(label_volume)][3])
    photoimage_button_volume_down.config(file = param.pic_path['volume_down'])
    photoimage_button_volume_up.config(file = param.pic_path['volume_up'])
    param.param1['volume_adjust_timeout'] = 2
    if param.param1['volume'] > 0 :
        param.param1['volume'] -= 1
        photo_path = param.pic_path['volume_'] + str(param.param1['volume']) + '.png'
        photoimage_label_volume.config(file = photo_path)
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
    param.param3['meeting_status'] = 'PAUSED'
    for widget in list_all_widgets:
        widget.config(bg = '#541F1F')
        try:
            widget.config(activebackground=widget.cget('background'))
        except:
            pass


def fun_resume():
    show_widget_list(list_resume_show)
    hide_widget_list(list_resume_hide)
    param.param3['meeting_status'] = 'STARTED'
    ##show_label_error(1231)
    for widget in list_all_widgets:
        widget.config(bg = '#000000')
        try:
            widget.config(activebackground=widget.cget('background'))
        except:
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
                print('rotate')
                pass


def thread_update_timeout():
    while param.quit_msg['quit_flag'] == False:
        time.sleep(1)
        for key, value in param.timeout.items():
            if value > 0:
                param.timeout[key] -= 1
        print('timeout',param.timeout)
        pass



def thread_state_machine():
    while param.quit_msg['quit_flag'] == False:
        time.sleep(0.1)
        if param.param3['meeting_status'] == 'READY':
            if param.timeout['bootup_greeting_timeout'] == 0:
                error.error['error_code'] = error.error_code_list['ERROR_CODE_READY_TIMEOUT']
                param.param3['meeting_status'] = 'IDLE'
                fun_meeting_idle()
                pass
            elif param.msg_list_1[0] == 'SYSTEM_READY':
                param.param3['meeting_status'] = 'IDLE'
                fun_meeting_idle()
                pass
        elif param.param3['meeting_status'] == 'IDLE':
            
            pass
        elif param.param3['meeting_status'] == 'START_LOADING':
            if param.timeout['START_LOADING'] == 0:
                param.param3['meeting_status'] = 'STARTED'            
                fun_meeting_start()
            pass
        elif param.param3['meeting_status'] == 'STARTED':
            pass
        elif param.param3['meeting_status'] == 'END_LOADING':
            pass
        elif param.param3['meeting_status'] == 'END':
            pass
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
button_mute = Button(root, text="OK", command=fun_mute, image = photoimage_button_mute, bg='black')

photoimage_button_unmute = PhotoImage(file= param.pic_path['button_unmute'])
button_unmute = Button(root, text="OK", command=fun_unmute, image = photoimage_button_unmute, bg='black')



photoimage_label_muted = PhotoImage(file= param.pic_path['label_muted'])
label_muted = Label(root, text="OK", image = photoimage_label_muted)


photoimage_button_volume_down = PhotoImage(file= param.pic_path['volume_down_inactive'])
button_volume_down = Button(root, text="OK", command=fun_volume_down, image = photoimage_button_volume_down)

photoimage_button_volume_up = PhotoImage(file=param.pic_path['volume_up_inactive'])
button_volume_up = Button(root, text="OK", command=fun_volume_up, image = photoimage_button_volume_up)


photoimage_label_volume = PhotoImage(file=param.pic_path['volume_']+'0.png')
label_volume = Label(root, text="OK", image = photoimage_label_volume)


photoimage_button_pause = PhotoImage(file=param.pic_path['button_pause'])
button_pause = Button(root, text="OK", command=fun_pause, image = photoimage_button_pause)


photoimage_button_resume = PhotoImage(file=param.pic_path['button_resume'])
button_resume = Button(root, text="OK", command=fun_resume, image = photoimage_button_resume)


label_time = Label(root, text="00 : 00 : 00", font='Arial 9 bold', fg = 'white')


#photoimage_label_error = PhotoImage(file="icons/error_01.png")
#label_error = Label(root, text="OK", image = photoimage_label_error)
label_error = Label(root, text="01", font='Arial 10 bold', fg = 'red')



photoimage_button_end = PhotoImage(file=param.pic_path['button_end_meeting'])
button_meeting_end = Button(root, text="OK", command=fun_meeting_end, image = photoimage_button_end)

photoimage_button_start = PhotoImage(file=param.pic_path['button_start_meeting'])
button_meeting_start = Button(root, text="OK", command=fun_meeting_start_loading, image = photoimage_button_start)


##photoimage_label_loading_spinner_background = PhotoImage(file="icons/loading_spinner_background.png")
##label_loading_spinner_background = Label(root, text="OK", image = photoimage_label_loading_spinner_background)
##
##photoimage_label_loading_spinner = PhotoImage(file="icons/loading_spinner.png")
##label_loading_spinner = Label(root, text="OK", image = photoimage_label_loading_spinner)

canvas_meeting_start_loading= Canvas(root, width=120, height=120, borderwidth = 0, highlightthickness = 0, bg='black')
canvas_meeting_end_loading= Canvas(root, width=64, height=64, borderwidth = 0, highlightthickness = 0, bg='black')

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
list_meeting_end_hide = [button_unmute, label_muted, button_resume, button_mute, button_meeting_end, button_pause, label_time]

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

# widget place

    

### widget place


### change all widgets bg & activebg
for widget in list_all_widgets:
    widget.config(bg = 'black', borderwidth = 0, highlightthickness = 0)
    try:
        widget.config(activebackground=widget.cget('background'))
    except:
        pass


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
#canvas_meeting_start_loading.place(x = 100, y = 60)

_thread.start_new_thread(fun_rotate_pic, ())
_thread.start_new_thread(thread_state_machine, ())

_thread.start_new_thread(thread_update_timeout, ())


fun_meeting_ready()


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
