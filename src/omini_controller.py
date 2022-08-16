from system import Camera
from convertor import VRC_UAVCam_Client
import filters as f
import scope
import time


""" 可调整的变量
"""
SYSTEM_EVALUATION_CYCLE_TIME = 0.02  # The loop time of the whole system, do not change it unless you know what you are doing. It will also effect the sample speed of the system, which will make the camera move faster or slower.
RECORD_VOLUME = 10000
RECORDING = False

""" 录制
"""
class RecordTape:
    volume = RECORD_VOLUME

    def __init__(self):
        self.rec_point = []

    def init_tape(self):
        self.rec_point = []

    def add_rec_point(self, pos, rot, t_diff):
        if len(self.rec_point) < self.volume:
            self.rec_point.append((pos, rot, t_diff))

    def replay(self, client: VRC_UAVCam_Client):
        for i in range(len(self.rec_point)):
            pos, rot, t_diff = self.rec_point[i]
            client.sync_state(pos, rot)
            time.sleep(t_diff+5 / 1000)


def start_record():
    global RECORDING
    global tape
    RECORDING = True
    tape.init_tape()
    print("start recording")


def stop_record():
    global RECORDING
    RECORDING = False
    print("stop recording")

def toggle_record():
    global RECORDING
    if RECORDING:
        stop_record()
    else:
        start_record()


def replay_record():
    global tape
    tape.replay(vrc_client)
    print("replay finished")


""" 获取实例 (一般不用动)
"""
vrc_client = VRC_UAVCam_Client()  # get vrc osc client instance
cam = Camera()  # get camera instance that controls the camera movement and features
cam.stop_evaluate()  # stop the camera object evaluation first
tape = RecordTape()


""" 按钮配置区域
you can diy your own button config here. Attach filter or camera movement mode to the button.
I list all Button event so it's easier to copy and paste, only tested in Windows with my
3dconnecxion basic wireless model.
1. "none"                         - no button pressed
2. "left_button_click"            - only left button clicked
3. "right_button_click"           - only right button clicked
4. "left_button_hold"             - only left button held
5. "right_button_hold"            - only right button held
6. "left_button_double_click"     - only left button double clicked
7. "right_button_double_click"    - only right button double clicked
8. "all_button_click"             - all buttons clicked at the same time
9. "all_button_hold"              - all buttons held at the same time
10."all_button_double_click"      - all buttons double clicked at the same time
11."push_double"                  - push the middle wheel double times
"""

# ——————默认状态配置——————
cam.mode_fpv("none")  # 在默认情况下相机运动为FPV模式
cam.add_pre_pos_filter_list("none", [f.amp_0_01])  # 控制默认状态下相机移动速度
cam.add_pre_rot_filter_list("none", [f.amp_0_05])  # 控制默认状态下相机旋转速度

# ——————左键单击配置——————
cam.register_toggle("left_button_click")  # 注册左键点击为开关
cam.mode_drone("left_button_click")  # 注册左键点击为航拍模式

# ——————左键双击配置——————
cam.add_func_list(
    "left_button_double_click",
    [
        vrc_client.vrcl_toggle_af,
        vrc_client.vrcl_toggle_avatar_focus,
    ],  # 双击左键切换对焦模式
)

# ——————左键长按配置——————
cam.add_pre_pos_filter_list("left_button_hold", [f.zero])  # 长按左键时停止相机移动
cam.add_pre_rot_filter_list("left_button_hold", [f.zero])  # 长按左键时停止相机旋转

# ——————右键单击配置——————
cam.register_toggle("right_button_click")
cam.add_pre_pos_filter_list("right_button_click", [f.amp_10])

# ——————右键双击配置——————
cam.add_func_list("right_button_double_click", [vrc_client.uav_toggle_follow])

# ——————右键长按配置——————
cam.mode_slide("right_button_hold")

# ——————左右同时单击配置——————
cam.register_toggle("all_button_click")
cam.mode_cruise("all_button_click")
# cam.add_func_list("all_button_click", [toggle_record])

# ——————左右同时双击配置——————
# cam.add_func_list("all_button_double_click", [replay_record])

# ——————左右同时长按配置——————
cam.add_func_list(
    "all_button_hold", [cam.toggle_evaluate, vrc_client.toggle_start_stop]
)

# ——————旋钮双击配置——————
cam.add_after_pos_filter_list("push_double", [f.zero])
cam.add_after_rot_filter_list("push_double", [f.zero])


""" 数据处理区域
数据处理区域会启动一个Loop, 每一个周期计算并且更新一次按钮事件/相机位移.
"""


def constrain(x: float, min_value: float = 0, max_value: float = 1) -> float:
    """constrant the given value to be between min_value and max_value

    To convert a value to be between two numbers, cause the VRChat OSC offense raise error when
    the wrong value is given (expecially float number). If a float number should be between 0 and 1,
    it's better to use constrain(x, 0.001, 0.999) to make sure it won't be 0 or 1.

    Args:
        x: the value to be constrained
        min_value: the minimum value, default is 0
        max_value: the maximum value, default is 1

    Returns:
        the constrained value, if x smaller than min_value, return min_value, if x larger than max_value, return max_value
    """
    return max(min_value, min(max_value, x))


# 开始循环
while True:
    # 将左键按住设定为一个参数调整层, 按住左键时不再更新相机位移, 而是获取旋钮数据作为调整参数
    if cam.get_event_state("left_button_hold"):
        cam.start_variable_tunner()  # 调整层开始标志
        cam.update()  # 更新相机数据, 注意在start_variable_tunner()函数之后相机的姿态不再更新
        vrc_client.VRCLZoomRadial += cam.raw.y * 5e-3  # 获取旋钮原始y数据更新焦距
        vrc_client.VRCLZoomRadial = constrain(vrc_client.VRCLZoomRadial, 0.001, 0.999)
        vrc_client.sync_zoom()  # 上传焦距参数
        vrc_client.VRCLFocusRadial += cam.raw.yaw * 5e-3  # 获取旋钮原始yaw数据更新对焦距离
        vrc_client.VRCLFocusRadial = constrain(vrc_client.VRCLFocusRadial, 0.001, 0.999)
        vrc_client.sync_focus()  # 上传对焦距离参数
        vrc_client.VRCLApertureRadial += cam.raw.x * 5e-3  # 获取旋钮原始x数据更新光圈
        vrc_client.VRCLApertureRadial = constrain(
            vrc_client.VRCLApertureRadial, 0.001, 0.999
        )
        vrc_client.sync_aperture()  # 上传光圈参数
        if cam.raw.z < -0.9:
            vrc_client.vrcl_toggle_portrait()  # 按旋钮, 切换竖屏模式
            time.sleep(0.3)
        elif cam.raw.z > 0.9:
            vrc_client.vrcl_toggle_focus_peak()  # 拉旋钮, 开关对焦峰值线
            time.sleep(0.1)
        cam.stop_variable_tunner()  # 调整层结束标志

    # 正常状态
    else:
        cam.update()  # 更新相机数据
        vrc_client.sync_state(cam.pos, cam.rot)  # 上传相机位姿
        if RECORDING:
            tape.add_rec_point(cam.pos, cam.rot, cam.t_diff)

    # scope.debug_in_vofa(cam) # 取消注释将同时发送数据包到VOFA进行调试
    time.sleep(SYSTEM_EVALUATION_CYCLE_TIME)
