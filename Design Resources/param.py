import platform

if(platform.system() == "Linux"):
    server = {'IP':'10.0.5.1', 'PORT':9999}
    pic_dir = 'icons/'
else:
    pic_dir = 'C:/Users/Lidong/Dropbox (Melo)/Dropbox/Melo/GitHub/raspi_python_code/Design Resources/icons/'

    
    
param1 = {'volume':5, 'volume_adjust_timeout':0, 'shake_timeout':0}
param2 = {'SHAKE_TIMEOUT': 3}
param3 = {'meeting_status':'READY', 'old_time':0, 'new_time':0, 'pause_time':0, 'time_str':'00:00:00', 'angle':0}

ui_flag = {'loading_flag':False}

msg = {'msg_type':'r2t','status':False, 'volumn':0}

msg_list_1 = ['SYSTEM_NOT_READY']

timeout = {'bootup_greeting_timeout':2, 'meeting_ready_timeout': 0}

quit_msg = {'quit_flag':False, 'quit_code': 0, 'quit_timeout': 0, 'quit_cmd':False}


button_click = {'start_meeting':False, 'end_meeting':False, 'mute':False, 'unmute':False, 'pause':False, 'resume':False, 'volume_up':False, 'volume_down':False}

pic_path = {
'bootup_greeting': pic_dir+'bootup_greeting.png',
'volume_down': pic_dir+'volume_down.png',
'volume_up': pic_dir+'volume_up.png',
'loading_spinner': pic_dir+'loading_spinner.png',
'loading_spinner_background': pic_dir+'loading_spinner_background.png',
'wifi_off': pic_dir+'wifi_off.png',
'button_mute': pic_dir+'button_mute.png',
'button_unmute': pic_dir+'button_unmute.png',
'button_pause': pic_dir+'button_pause.png',
'button_resume': pic_dir+'button_resume.png',
'button_start_meeting': pic_dir+'button_start_meeting.png',
'button_end_meeting': pic_dir+'button_end_meeting.png',
'label_muted': pic_dir+'label_muted.png',
'label_paused': pic_dir+'label_paused.png',
'volume_': pic_dir+'volume_',
'volume_down_inactive': pic_dir+'volume_down_inactive.png',
'volume_up_inactive': pic_dir+'volume_up_inactive.png'
}
