# Description: 提供了一些Wrapper函数，用于调试
# Date: 2022-07-01
# Auther: DynAis
# ChangeLog: 

import time
import socket

# count time
def count_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("Time: %.2f" % (end - start))
    return wrapper

# log
def log(func):
    def wrapper(*args, **kwargs):
        print("Call: %s" % func.__name__)
        return func(*args, **kwargs)
    return wrapper

# output data to vofa as debuger
def debug_state(state):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 1347 # vofa local port
    # convert vec3 to csv string
    MESSAGE = ",".join(map(str, (state.t,\
                                 state.x,\
                                 state.y,\
                                 state.z,\
                                 state.pitch,\
                                 state.roll,\
                                 state.yaw,\
                                 state.buttons[0],\
                                 state.buttons[1])))
    MESSAGE = MESSAGE + "\n"
    print("Debug Message: %s" % MESSAGE)
    
    sock = socket.socket(socket.AF_INET,    # Internet
                          socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
