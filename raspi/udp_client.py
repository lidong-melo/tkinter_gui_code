from socket import *
import _thread
import param
import json
import platform
import msg_list
import time


# def fun_send_msg(udp_msg):
   # my_udp_socket.sendall(udp_msg.encode())





   
def send_msg(udp_msg):
    try:
        json_string = json.dumps(udp_msg)
        my_udp_socket.sendall(json_string.encode())
    except:
        print('send msg error. connection disappear when send msg')
    #print('send_msg->', udp_msg)

   
def thread_udp_recv():
    while param.quit_msg['quit_flag'] == False:
        try:
            recv_data = my_udp_socket.recv(1024)
            recv_str = recv_data.decode()
            #print('str:',recv_str)
            recv_msg_dict = json.loads(recv_str)
            print('recv:',recv_msg_dict)
            parse_udp_msg(recv_msg_dict)
            recv_msg_dict.clear()
            
            # if recv_param.param1['msg_type'] == 't2r' :
                # print (recv_param.param1['doa_angle'])
                # global_var['angle'] = recv_param.param1['doa_angle']
                # fun_rotate_pic(global_var['angle'])
            # elif recv_param.param1['msg_type'] == 'r2t':
                # print (recv_param.param1['status'])
                # global_var['meeting_status'] = recv_param.param1['status']
            # else:
                # print('wrong param.param1')
        except:
            pass
            #print('udp parse fail')
    my_udp_socket.close()

def parse_udp_msg(msg):
    #print('parse -->')
    # 按照状态机接收解析消息，如果不对应则抛弃。
    # 方法1：在字典中找列表中的值
    # for key in msg_list.msg_list_filter[param.state['raspi_state']]:
        # print('123',key)
        # if msg.get(key):
            # msg_list.msg_from_tx2[key] = msg[key]
    
    # 方法2：在列表中找字典中的key
    for key in msg:
        if msg_list.msg_list_filter[param.state['raspi_state']].count(key) != 0:
            msg_list.msg_from_tx2[key] = msg[key]
    #print('<-- parse')
    

if(platform.system() == "Linux"):
    server = {'IP':'10.0.5.1', 'PORT':9999}
else:
    #server = {'IP':gethostbyname(gethostname()), 'PORT':60000}
    server = {'IP':'192.168.28.130', 'PORT':60000}

    
## create UDP socket
while 1:
    try:
        my_udp_socket = socket(AF_INET,SOCK_DGRAM)
        my_udp_socket.connect((server['IP'],server['PORT']))
        break
    except:
        time.sleep(1)
        print('wait_for_pppd_service!!!!!!')
print('connect to', server)
_thread.start_new_thread(thread_udp_recv, ())   
