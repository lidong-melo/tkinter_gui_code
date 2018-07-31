import time
import param
import error
        

def thread_run():
    while param.quit_msg['quit_flag'] == False:
        time.sleep(1)
        param.param1['shake_timeout'] += 1
        if param.param1['shake_timeout'] > param.param2['SHAKE_TIMEOUT']:
            param.param1['shake_timeout'] = 0
            error.error['error_code'] = error.error_code_list['ERROR_CODE_SHAKE_TIMEOUT']
            error.error['error_flag'] = True
            param.msg_list_1.append([error.error['error_flag'], error.error['error_code']])
            print('timeout!')
            

        
        