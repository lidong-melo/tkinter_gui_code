from socket import *
import _thread
import param
import json
import platform



# def fun_send_msg(udp_msg):
   # my_udp_socket.sendall(udp_msg.encode())





   
def send_msg(udp_msg):
    json_string = json.dumps(udp_msg)
    my_udp_socket.sendall(json_string.encode())

   
def thread_udp_recv():
    while param.quit_msg['quit_flag'] == False:
        try:
            recv_data = my_udp_socket.recv(1024)
            recv_str = recv_data.decode()
            print('str:',recv_str)
            recv_msg_dict = json.loads(recv_str)
            print('dict:',recv_msg_dict)
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
            print('udp parse fail')
    my_udp_socket.close()

def parse_udp_msg(msg):
    print('parse -->')
    # 按照状态机接收解析消息，如果不对应则抛弃。
    # 方法1：在字典中找列表中的值
    # for key in param.msg_list_for_state_machine[param.param3['meeting_status']]:
        # print('123',key)
        # if msg.get(key):
            # param.msg_from_tx2[key] = msg[key]
    
    # 方法2：在列表中找字典中的key
    for key in msg:
        if param.msg_list_for_state_machine[param.param3['meeting_status']].count(key) != 0:
            param.msg_from_tx2[key] = msg[key]
    print('<-- parse')
    

if(platform.system() == "Linux"):
    server = {'IP':'10.0.5.1', 'PORT':9999}
else:
    server = {'IP':gethostbyname(gethostname()), 'PORT':60000}
    

    
## create UDP socket
my_udp_socket = socket(AF_INET,SOCK_DGRAM)
my_udp_socket.connect((server['IP'],server['PORT']))
print('connect to', server)
_thread.start_new_thread(thread_udp_recv, ())   