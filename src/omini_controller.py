from system import Camera
from convertor import VRC_UAVCam_Client
import filters as f
import scope
import time

""" Button event list:
"none"
"left_button_click"
"right_button_click"
"left_button_hold"
"right_button_hold"
"left_button_double_click"
"right_button_double_click"
"all_button_click"
"all_button_hold"
"all_button_double_click"
"push_double"
"""

# User defined functions


vrc_client = VRC_UAVCam_Client()
cam = Camera()
cam.stop() # stop camera first

# config buttons
cam.add_pre_pos_filter_list("none", [f.amp_0_2])
cam.add_pre_rot_filter_list("none", [f.amp_0_2])

# 左键单击
cam.register_toggle("left_button_click")
cam.add_pre_pos_filter_list("left_button_click", [f.amp_0_2])
cam.add_pre_rot_filter_list("left_button_click", [f.amp_0_2])

# 左键双击
cam.add_func_list("left_button_double_click", [vrc_client.toggle_fullscreen])

# 左键长按

# 右键单击

# 右键双击
cam.add_func_list("right_button_double_click", [vrc_client.toggle_follow])

# 右键长按

# 全部键单击
cam.add_after_pos_filter_list("all_button_click", [f.zero])
cam.add_after_rot_filter_list("all_button_click", [f.zero])

# 全部建双击

# 全部键长按
cam.add_after_pos_filter_list("all_button_hold", [f.amp_0_99])
cam.add_after_rot_filter_list("all_button_hold", [f.amp_0_99])

# Push双击
cam.add_func_list("push_double", [vrc_client.toggle_drone, cam.toggle_start_stop])

while True:
    cam.update()
    vrc_client.sync(cam.pos, cam.rot)
    scope.debug_in_vofa(cam)
    time.sleep(0.02)
