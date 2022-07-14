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


def send_to_vofa(func):
    def wrapper(*args, **kwargs):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 1347  # vofa local port
        MESSAGE = func(*args, **kwargs)
        # print("Debug Message: %s" % MESSAGE)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
        sock.sendto(MESSAGE.encode("utf-8"), (UDP_IP, UDP_PORT))

    return wrapper


@send_to_vofa
def debug_in_vofa(cam):
    # convert to csv string
    MESSAGE = ",".join(
        map(
            str,
            (
                cam.t,
                cam.pos[0],
                cam.pos[1],
                cam.pos[2],
                cam.rot[0],
                cam.rot[1],
                cam.rot[2],
                cam.l_button_pressed,
                cam.r_button_pressed,
                cam.event,
                cam.t_diff,
                cam.l_button.button_hold_time,
                cam.r_button.button_hold_time,
                cam.get_event_state("left_button_click"),
                cam.get_event_state("right_button_click"),
                cam.get_event_state("left_button_hold"),
                cam.get_event_state("right_button_hold"),
                cam.get_event_state("left_button_double_click"),
                cam.get_event_state("right_button_double_click"),
                cam.get_event_state("all_button_click"),
                cam.get_event_state("all_button_hold"),
                cam.get_event_state("all_button_double_click"),
                cam.get_event_state("push_double"),
            ),
        )
    )
    MESSAGE = MESSAGE + "\n"
    return MESSAGE