import platform
import sys

if(platform.system() == "Linux"):
    pic_dir = 'icons/'
else:
    pic_dir = str(sys.path[0] + "\\icons\\")
    print(pic_dir)
    #pic_dir = 'C:/Users/Lidong/Dropbox (Melo)/Dropbox/Melo/GitHub/raspi_python_code/Design Resources/icons/'

    
    
param1 = {'volume':5, 'volume_adjust_timeout':0, 'shake_timeout':0}
param2 = {'SHAKE_TIMEOUT': 3}
param3 = {'meeting_status':'READY', 'old_time':0, 'new_time':0, 'pause_time':0, 'time_str':'00:00:00', 'angle':0}

ui_flag = {'loading_flag':False}

msg = {'msg_type':'r2t','status':False, 'volumn':0}

#msg_list_1 = ['ERROR CODE is 33','SYSTEM IS READY', 'MEETING IS START', 'TX2 END MEETING', 'MEETING IS END']


tx2_ack = {
'SYSTEM_IS_READY':False,
'MEETING_IS_STARTED':False,
'MEETING_IS_PAUSED':False,
'MEETING_IS_RESUME':False,
'TX2_END_MEETING':False,
'MEETING_IS_END':False,
'ERROR_CODE':0
}


raspi_ack = {
'MEETING_IS_STARTING':False,
'MEETING_IS_ENDING':False,
'MEETING_IS_PAUSING':False,
'MEETING_IS_RESUMING':False,
'ERROR_CODE':0
}


timeout = {'bootup_greeting_timeout':-1, 'meeting_ready_timeout': -1, 'START_LOADING': -1, 'END_LOADING': -1}

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
