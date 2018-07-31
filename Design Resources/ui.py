#!/usr/bin/python
#coding:utf-8

import tkinter as tk
from PIL import ImageTk, Image ## to use png format, import imageTK
from tkinter import Button, PhotoImage, Label
import param
import _thread
import time
import datetime


def fun_meeting_start():
    show_widget_list(list_meeting_start_show)
    hide_widget_list(list_meeting_start_hide)
    param.param3['meeting_status'] = 'STARTED'
    
    ## initial time
    param.param3['old_time'] = datetime.datetime.now()
    param.param3['new_time'] = param.param3['old_time']
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
    photoimage_button_volume_down.config(file = 'icons/volume_down.png')
    photoimage_button_volume_up.config(file = 'icons/volume_up.png')
    param.param1['volume_adjust_timeout'] = 2
    if param.param1['volume'] < 9:
        param.param1['volume'] += 1
        photo_path = 'icons/volume_' + str(param.param1['volume']) + '.png'
        photoimage_label_volume.config(file=photo_path)
    pass


def fun_volume_down():
    #volume_adjust_show
    label_volume.place(x = pos[id(label_volume)][2], y = pos[id(label_volume)][3])
    photoimage_button_volume_down.config(file = 'icons/volume_down.png')
    photoimage_button_volume_up.config(file = 'icons/volume_up.png')
    param.param1['volume_adjust_timeout'] = 2
    if param.param1['volume'] > 0 :
        param.param1['volume'] -= 1
        photo_path = 'icons/volume_' + str(param.param1['volume']) + '.png'
        photoimage_label_volume.config(file=photo_path)
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
    show_label_error(1231)
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


def thread_update_ui():
    while 1 :
        time.sleep(1)# 1 second timer
        ## volume adjust hide
        if param.param1['volume_adjust_timeout'] > 0:
            param.param1['volume_adjust_timeout'] -= 1
            if param.param1['volume_adjust_timeout'] == 0:
                try:
                    #volume_adjust_hide
                    label_volume.place_forget()
                    photoimage_button_volume_down.config(file = 'icons/volume_down_inactive.png')
                    photoimage_button_volume_up.config(file = 'icons/volume_up_inactive.png')    
                except:
                    break # 从这里退出线程，否则线程永远关不掉

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
                break # 从这里退出线程，否则线程永远关不掉


def show_label_error(error_code):
    label_error.config(text = error_code)
    label_error.place(x = pos[id(label_error)][2], y = pos[id(label_error)][3])



#ui init
root = tk.Tk()
root.config(width = 320, height = 240, bg='black')

## 顺序不能调整，因为有图层index的逻辑关系
photoimage_label_wifi = PhotoImage(file="icons/wifi_off.png")
label_wifi = Label(root, text="OK", image = photoimage_label_wifi)
#label_wifi.config(activebackground=label_wifi.cget('background'))
#label_wifi.place(x=pos_label_wifi[2], y=pos_label_wifi[3])
#label_wifi.config(width = pos_label_wifi[0], height = pos_label_wifi[1])



photoimage_button_mute = PhotoImage(file="icons/button_mute.png")
button_mute = Button(root, text="OK", command=fun_mute, image = photoimage_button_mute, bg='black')

photoimage_button_unmute = PhotoImage(file="icons/button_unmute.png")
button_unmute = Button(root, text="OK", command=fun_unmute, image = photoimage_button_unmute, bg='black')



photoimage_label_muted = PhotoImage(file="icons/label_muted.png")
label_muted = Label(root, text="OK", image = photoimage_label_muted)


photoimage_button_volume_down = PhotoImage(file="icons/volume_down_inactive.png")
button_volume_down = Button(root, text="OK", command=fun_volume_down, image = photoimage_button_volume_down)

photoimage_button_volume_up = PhotoImage(file="icons/volume_up_inactive.png")
button_volume_up = Button(root, text="OK", command=fun_volume_up, image = photoimage_button_volume_up)


photoimage_label_volume = PhotoImage(file="icons/volume_0.png")
label_volume = Label(root, text="OK", image = photoimage_label_volume)


photoimage_button_pause = PhotoImage(file="icons/button_pause.png")
button_pause = Button(root, text="OK", command=fun_pause, image = photoimage_button_pause)


photoimage_button_resume = PhotoImage(file="icons/button_resume.png")
button_resume = Button(root, text="OK", command=fun_resume, image = photoimage_button_resume)


label_time = Label(root, text="00 : 00 : 00", font='Arial 9 bold', fg = 'white')


#photoimage_label_error = PhotoImage(file="icons/error_01.png")
#label_error = Label(root, text="OK", image = photoimage_label_error)
label_error = Label(root, text="01", font='Arial 10 bold', fg = 'red')



photoimage_button_end = PhotoImage(file="icons/button_end_meeting.png")
button_meeting_end = Button(root, text="OK", command=fun_meeting_end, image = photoimage_button_end)

photoimage_button_start = PhotoImage(file="icons/button_start_meeting.png")
button_meeting_start = Button(root, text="OK", command=fun_meeting_start, image = photoimage_button_start)



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
id(label_error): [18, 18, 146, 222],#id(label_error): [18, 18, 151, 222],
id(label_time): [128, 16, 130, 156]
}

## list of show & hide

list_all_widgets = [root, label_wifi, button_mute, button_unmute, label_muted, button_pause, label_volume, button_meeting_end, button_volume_down, button_volume_up,  button_resume, button_meeting_start, label_error, label_time]

list_meeting_start_show = [button_mute, button_meeting_end, button_pause, label_time]
list_meeting_start_hide = [button_unmute,  label_muted, button_resume, button_meeting_start]

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

list_home = [label_wifi, button_volume_down, button_volume_up, button_meeting_start]



# widget place
for widget in list_home:
    widget.place(x = pos[id(widget)][2], y = pos[id(widget)][3])
    widget.config(width = pos[id(widget)][0], height = pos[id(widget)][1])

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




root.mainloop()






