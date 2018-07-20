#!/usr/bin/python
#coding:utf-8


import tkinter as tk
from PIL import ImageTk, Image ## to use png format, import imageTK
from tkinter import Button, Frame, PhotoImage,Label
import platform
from socket import *
import _thread
import random
import time

## global variable
global_var = {'meeting_status':False, 'old_time':0, 'new_time':0, 'time_str':'00:00:00', 'send_flag':False, 'angle':0}
server = {'IP':'192.168.31.209', 'PORT':60000}
key_word = {'doa':'doa'}


def rotate_pic(angle):
    global_var['angle'] = angle
    photo_bg.paste(image_bg.rotate(global_var['angle']))
    label_bg.config(image = photo_bg) 
    label_time.text = str(angle)

def fun_udp_msg_send(udp_msg):
   my_udp_socket.sendall(udp_msg.encode())


def thread_udp_recv():
    while True:
        try:           
            recv_data = my_udp_socket.recv(1024)
            recv_str = recv_data.decode()
            print(recv_str)
            if recv_str.find(key_word['doa']) != -1:
                index_start = recv_str.find('doa=')+4
                aaa = recv_str[index_start:len(recv_str)]
                print (index_start, aaa)
                angle = int(aaa)
                try:
                    rotate_pic(angle)
                except:
                    pass            
        except:
            pass
    my_udp_socket.close()



def thread_random_rotate():
    while True:
        time.sleep(0.3)
        angle = random.randint(0,360)
        pass
        try:
            rotate_pic(angle)
        except:
            pass
        
   
   

def fun_meeting_control():
    global meeting_status # True is start, False is stop
    if global_var['meeting_status'] == False:
        global_var['meeting_status'] = True
        fun_udp_msg_send('start')
        ## enable timer
        #    global_var['old_time'] = datetime.datetime.now()
        #    msg_time_elapse.repeat(1000, fun_calculate_time_elapse)
        ## update UI
        photoimage_button.config(file='image_button_stop-1.png')
        #    global_var['time_str'] = '00:00:00'
        #    msg_time_elapse.value = global_var['time_str']
    else:
        fun_udp_msg_send('stop')
        ## disable timer
        #    msg_time_elapse.cancel(fun_calculate_time_elapse)
        ## update UI
        global_var['meeting_status'] = False
        photoimage_button.config(file='image_metal_button-1.png')



##class SimpleApp(object):
##    def __init__(self, master, filename, **kwargs):
##        self.master = master
##        self.filename = filename
##        self.canvas = tk.Canvas(master, width=160, height=160)
##        self.canvas.pack()
##        self.update = self.draw().__next__
##        master.after(20, self.update)
##
##
##
##    def draw(self):
##        image = Image.open(self.filename)
##        
##
##        angle = 0
##
##        while True:
##            tkimage = ImageTk.PhotoImage(image.rotate(angle))
##            canvas_obj = self.canvas.create_image(
##                80, 80, image=tkimage)
##            self.master.after_idle(self.update)
##            yield
##            self.canvas.delete(canvas_obj)
##            angle += 1
##            angle %= 360

## check system version
sysstr = platform.system()
if(sysstr =="Windows"):
    print ("Call Windows tasks")
elif(sysstr == "Linux"):
    print ("Call Linux tasks")
else:
    print ("Other System tasks")   

## init window
root = tk.Tk()
root.config(width = 320, height = 240)

## adapt to raspberry pi
if(sysstr == "Linux"):
    root.attributes("-fullscreen", True)
    root.config(cursor="none")
    server = {'IP':'10.0.5.1', 'PORT':9999}
	

label_time = Label(root)
label_time.place(x=0,y=0)


## clock background
image_bg = Image.open("clock.png")
photo_bg = ImageTk.PhotoImage(image_bg)
label_bg = Label(image = photo_bg)
label_bg.image = photo_bg # keep a reference!
label_bg.place(x=40,y=0)

#button
photoimage_button = PhotoImage(file="image_metal_button-1.png")
button_cmd = Button(root, text="OK", command=fun_meeting_control, image = photoimage_button)
button_cmd.place(x=110,y=70)
#button.config(image = 'image_metal_button.png')
button_cmd.config(width = 100, height = 100, borderwidth = 0, highlightthickness = 0)


## create UDP socket
my_udp_socket = socket(AF_INET,SOCK_DGRAM)
my_udp_socket.connect((server['IP'],server['PORT']))

## create UDP recv thread
_thread.start_new_thread(thread_udp_recv, ())
_thread.start_new_thread(thread_random_rotate, ())

root.mainloop()


