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

# constrant number between 0 and 1
def constrain(x, min_value=0, max_value=1):
    return max(min_value, min(max_value, x))


vrc_client = VRC_UAVCam_Client()
cam = Camera()
cam.stop_evaluate()  # stop camera first

# config buttons
cam.mode_fpv("none")
cam.add_pre_pos_filter_list("none", [f.amp_0_2])
cam.add_pre_rot_filter_list("none", [f.amp_0_2])

# 添加按钮函数和滤镜
# 左键单击 - 开关z轴旋转
cam.register_toggle("left_button_click")
cam.mode_drone("left_button_click")

# 左键双击 - 开关AF
cam.add_func_list(
    "left_button_double_click",
    [vrc_client.vrcl_toggle_af, vrc_client.vrcl_toggle_avatar_focus],
)

# 左键长按 - 相机设置调节
cam.add_pre_pos_filter_list("left_button_hold", [f.zero])
cam.add_pre_rot_filter_list("left_button_hold", [f.zero])

# 右键单击 - 开关补光 (待实现)
cam.register_toggle("right_button_click")
cam.add_pre_rot_filter_list("right_button_click", [f.amp_0_1])

# 右键双击 - 开关跟随
cam.add_func_list("right_button_double_click", [vrc_client.uav_toggle_follow])

# 右键长按 - 调节光照设置 - 旋转:颜色 - 前后:强度 (待实现)
cam.mode_tripod("right_button_hold")

# 全部键单击 - 定速巡航
cam.register_toggle("all_button_click")
cam.mode_cruise("all_button_click")

# 全部建双击 - 开关机
cam.add_func_list(
    "all_button_double_click", [cam.toggle_evaluate, vrc_client.toggle_start_stop]
)

# 全部键长按

# Push双击 - 回中
cam.add_after_pos_filter_list("push_double", [f.zero])
cam.add_after_rot_filter_list("push_double", [f.zero])

while True:
    # as variable controler
    # 左键hold, 前后:zoom, 旋转:对焦

    if cam.get_event_state("left_button_hold"):
        cam.start_variable_tunner()
        cam.update()
        vrc_client.VRCLZoomRadial += cam.raw.y * 5e-3
        vrc_client.VRCLZoomRadial = constrain(vrc_client.VRCLZoomRadial, 0.001, 0.999)
        vrc_client.sync_zoom()
        vrc_client.VRCLFocusRadial += cam.raw.yaw * 5e-3
        vrc_client.VRCLFocusRadial = constrain(vrc_client.VRCLFocusRadial, 0.001, 0.999)
        vrc_client.sync_focus()
        vrc_client.VRCLApertureRadial += cam.raw.x * 5e-3
        vrc_client.VRCLApertureRadial = constrain(
            vrc_client.VRCLApertureRadial, 0.001, 0.999
        )
        vrc_client.sync_aperture()
        if cam.raw.z < -0.9:
            vrc_client.vrcl_toggle_portrait()
            time.sleep(0.3)
        elif cam.raw.z > 0.9:
            vrc_client.vrcl_toggle_focus_peak()
            time.sleep(0.1)
        # vrc_client.sync_state(cam.pos, cam.rot)
        cam.stop_variable_tunner()

    # as position controler
    else:
        cam.update()
        vrc_client.sync_state(cam.pos, cam.rot)

    # scope.debug_in_vofa(cam)
    time.sleep(0.02)
