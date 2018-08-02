error = {'error_code': 0, 'error_flag': False}


error_code_list = {
'ERROR_CODE_READY_TIMEOUT':1,
'ERROR_CODE_SHAKE_TIMEOUT':2,
'ERROR_CODE_START_MEETING_TIMEOUT':3,
'ERROR_CODE_END_MEETIG_TIMEOUT':4,
'ERROR_CODE_PAUSE_TIMEOUT':5,
'ERROR_CODE_RESUME_TIMEOUT':6,
'ERROR_CODE_MUTE_TIMEOUT':7,
'ERROR_CODE_UNMUTE_TIMEOUT':8,
'ERROR_CODE_VOL_UP_TIMEOUT':9,
'ERROR_CODE_VOL_DOWN_TIMEOUT':10,
'ERROR_CODE_INIT_ERROR':11,
'ERROR_CODE_READY_ERROR':12,
'ERROR_CODE_IDLE_ERROR':13,
'ERROR_CODE_NETWORK_ERROR':14,
'ERROR_CODE_AUDIO_IN_ERROR':15,
'ERROR_CODE_AUDIO_OUT_ERROR':16,
'ERROR_CODE_TX2_ERROR':51,
'ERROR_CODE_STATE_UNKNOWN': 99
}


def error_handler(error_code):
    error['error_code'] = error_code
    print(error_code)
    
    
    