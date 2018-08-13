import platform
import sys

if(platform.system() == "Linux"):
    pic_dir = '/home/pi/share/raspi/icons/'
else:
    pic_dir = str(sys.path[0] + "\\icons\\")
    print(pic_dir)
    #pic_dir = 'C:/Users/Lidong/Dropbox (Melo)/Dropbox/Melo/GitHub/raspi_python_code/Design Resources/icons/'

    
    
param1 = {'volume':5, 'volume_adjust_timeout':0, 'shake_timeout':0, 'rssi':-1}
param2 = {'SHAKE_TIMEOUT': 3}
param3 = {'meeting_status':'READY', 'old_time':0, 'new_time':0, 'pause_time':0, 'time_str':'00:00:00', 'angle':0}

ui_flag = {'loading_flag':False}

#msg = {'msg_type':'r2t','status':False, 'volumn':0}

#msg_list_1 = ['ERROR CODE is 33','SYSTEM IS READY', 'MEETING IS START', 'TX2 END MEETING', 'MEETING IS END']

state = {'raspi_state':'READY', 'reset_raspi_state':False}
watch_dog = {'timeout':30, 'interval':30}



msg_to_tx2 = [
{'RASPI_IS_READY':True}, #0
{'MEETING_IS_STARTING':True}, #1
{'MEETING_IS_ENDING':True}, #2
{'MEETING_IS_PAUSING':True}, #3
{'MEETING_IS_RESUMING':True}, #4
{'ERROR_CODE':0}, #5
{'VOLUME_IS_UP':0}, #6
{'VOLUME_IS_DOWN':0}, #7
{'MUTE':True}, #8
{'UNMUTE':True}, #9
{'RESET_MEETING':False},#10
{'WIFI_RSSI':0},#11
]

msg_from_tx2 = {
'SYSTEM_IS_READY':False,
'MEETING_IS_RECORDING':False,
'MEETING_IS_PAUSED':False,
'MEETING_IS_RESUME':False,
'TX2_END_MEETING':False,
'MEETING_IS_END':False,
'ERROR_CODE':0,
'VOLUME_IS_UP':0,
'VOLUME_IS_DOWN':0,
'MUTE':False,
'UNMUTE':False, 
'RESET_MEETING':False,
'WIFI_RSSI':-1,
'tx2_state':'READY',
}

#根据不同状态机，响应不同消息
msg_list_for_state_machine={
'READY':['SYSTEM_IS_READY','ERROR_CODE','WIFI_RSSI','tx2_state',],
'IDLE':['ERROR_CODE','VOLUME_IS_UP','VOLUME_IS_DOWN','WIFI_RSSI','tx2_state',],
'START_LOADING':['MEETING_IS_RECORDING','ERROR_CODE','WIFI_RSSI','tx2_state',],
'RECORDING':['TX2_END_MEETING','ERROR_CODE','VOLUME_IS_UP','VOLUME_IS_DOWN','MUTE','UNMUTE','WIFI_RSSI','tx2_state',],
'PAUSED':['MEETING_IS_PAUSED','TX2_END_MEETING','MEETING_IS_END','ERROR_CODE','VOLUME_IS_UP','VOLUME_IS_DOWN','MUTE','UNMUTE','WIFI_RSSI','tx2_state',],
'END_LOADING':['MEETING_IS_END','ERROR_CODE','WIFI_RSSI','tx2_state',]
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
'volume_up_inactive': pic_dir+'volume_up_inactive.png',
'wifi_': pic_dir+'wifi_',
}
