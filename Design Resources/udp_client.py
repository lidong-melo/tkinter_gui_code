from socket import *
import _thread
import param
import json

server = {'IP':'10.0.5.1', 'PORT':9999}

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
            print(recv_str)            
            recv_param.param1 = json.loads(recv_str)
            print (recv_param.param1)
            if recv_param.param1['msg_type'] == 't2r' :
                print (recv_param.param1['doa_angle'])
                global_var['angle'] = recv_param.param1['doa_angle']
                fun_rotate_pic(global_var['angle'])
            elif recv_param.param1['msg_type'] == 'r2t':
                print (recv_param.param1['status'])
                global_var['meeting_status'] = recv_param.param1['status']
            else:
                print('wrong param.param1')
        except:
            pass
    my_udp_socket.close()
    
## create UDP socket
my_udp_socket = socket(AF_INET,SOCK_DGRAM)
my_udp_socket.connect((server['IP'],server['PORT'])) 

_thread.start_new_thread(thread_udp_recv, ())   