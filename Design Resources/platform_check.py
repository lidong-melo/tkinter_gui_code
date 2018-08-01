import platform

def init(root):
    ## adapt to raspberry pi
    if(platform.system() == "Linux"):
        server = {'IP':'10.0.5.1', 'PORT':9999}
        root.attributes("-fullscreen", True)
        root.config(cursor="none")

        
