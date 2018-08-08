

msg_from_raspi = {
'RASPI_IS_READY':False, #0
'MEETING_IS_STARTING':False, #1
'MEETING_IS_ENDING':False, #2
'MEETING_IS_PAUSING':False, #3
'MEETING_IS_RESUMING':False, #4
'ERROR_CODE':0, #5
'VOLUME_IS_UP':-1, #6
'VOLUME_IS_DOWN':-1, #7
'MUTE':False, #8
'UNMUTE':False, #9
'RASPI_IS_IDLE':False, #10
'RESET_MEETING':False,

}

# msg_to_raspi = {
# 'SYSTEM_IS_READY':False, #0
# 'MEETING_IS_RECORDING':False, #1
# 'MEETING_IS_PAUSED':False, #2
# 'TX2_END_MEETING':False, #3
# 'MEETING_IS_END':False, #4
# 'ERROR_CODE':0, #5
# 'VOLUME_IS_UP':0, #6
# 'VOLUME_IS_DOWN':0 #7
# }
msg_to_raspi = [
{"SYSTEM_IS_READY": True}, #0
{"MEETING_IS_RECORDING": True}, #1
{'MEETING_IS_PAUSED':True}, #2
{"TX2_END_MEETING":True}, #3
{"MEETING_IS_END":True}, #4
{'ERROR_CODE':0}, #5
{'VOLUME_IS_UP':-1}, #6
{'VOLUME_IS_DOWN':-1}, #7
{'WIFI_RSSI':0}, #8
{'MUTE':True}, #9
{'UNMUTE':True}, #10
]

param1 = {'no_face_15min':False, 'volume':5, 'mute':False}

#根据不同状态机，响应不同消息
msg_list_for_state_machine={
'READY':['RASPI_IS_READY','ERROR_CODE'],
'IDLE':['MEETING_IS_STARTING','ERROR_CODE','VOLUME_IS_UP','VOLUME_IS_DOWN'],
'RECORDING':['MEETING_IS_PAUSING','MEETING_IS_ENDING','ERROR_CODE','VOLUME_IS_UP','VOLUME_IS_DOWN','MUTE','UNMUTE'],
'PAUSED':['MEETING_IS_RESUMING','MEETING_IS_ENDING','ERROR_CODE','VOLUME_IS_UP','VOLUME_IS_DOWN','MUTE','UNMUTE']
#'END_LOADING':['MEETING_IS_END','ERROR_CODE']# 15min noface, tx2 end meeting 
}

