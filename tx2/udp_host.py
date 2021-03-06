#coding:utf-8
import platform
from socket import *
import _thread
import json
import param_host
import msg_list
import time

def tx2_udp_send(msg_dict):
    json_string = json.dumps(msg_dict)
    address_tuple = tuple(param_host.address_list)
    #print('ip address:',param_host.address_list)
    try:
        s.sendto(json_string.encode(), address_tuple)
        #print(address_tuple)
        print('send', address_tuple, json_string)
    except:
        print(address_tuple)
        print('disconnect')  
        
def thread_udp_recv():
    while param_host.flag['thread_quit'] == False:
        try:
            recv_data,address_recv = s.recvfrom(1024)
            
            # update client ip -->
            param_host.address_list.clear()
            address_list_temp = list(address_recv)
            param_host.address_list.append(address_list_temp[0])
            param_host.address_list.append(address_list_temp[1])
            print('recv',param_host.address_list,recv_data)
            # <-- update client ip
            
            # parse recv msg
            recv_str = recv_data.decode()
            recv_msg_dict = json.loads(recv_str)
            parse_udp_msg(recv_msg_dict)
            recv_msg_dict.clear()
        except:
            pass
    my_udp_socket.close()


def parse_udp_msg(msg):
    # 方法2：在列表中找字典中的key
    for key in msg:
        if msg_list.msg_list_filter[param_host.state['tx2_state']].count(key) != 0:
            msg_list.msg_from_raspi[key] = msg[key]
            #print(msg_list.msg_from_raspi[key])
            
    
#udp inits
if platform.node().find('virtual') != -1:
    server = {'IP':'192.168.28.130', 'PORT':60000}
else:
    server = {'IP':'10.0.5.1', 'PORT':9999}
print(server)
    
    
#udp init
while 1:
    try:
        s = socket(AF_INET,SOCK_DGRAM)  
        s.bind((server['IP'], server['PORT']))
        break
    except:
        time.sleep(1)
        print('wait_for_pppd_service!!!!!!')
_thread.start_new_thread(thread_udp_recv, ())    
