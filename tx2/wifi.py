import subprocess
import re

#proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
#sudo iw dev wlan0 scan | grep -E 'on wlan0|signal:|SSID:' > ~/lidong/rssi.txt

def get_rssi():
    try:
        proc = subprocess.Popen(["sudo", "iw", "wlan0", "scan"], stdout=subprocess.PIPE, universal_newlines=True)
        out, err = proc.communicate()
        
        index1 = out.find('associated')
        index2 = out.find('signal', index1)
        index3 = out.find('\n', index2)
        out_line = out[index2:index3]
        if out_line:
            ret = re.search('\d+', out[index2:index3]).group()
            #print("~~~~~~~~~~~~~~~~~~~~~",ret)
            return ret
        else:
            #print('no connection')
            return 'ERROR'
    except:
        print('wifi scan too fast')
    
    
    

    
    
    
    
    