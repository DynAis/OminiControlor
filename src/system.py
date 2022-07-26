import scope
import process as l2
import numpy as np
import filters as f


class Camera(l2.Process):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return super().__str__()

    # 注册开关机开关
    def register_start_stop_toggle(self, bind_key_name: str = "none"):
        self.add_func_list(bind_key_name, [self.toggle_evaluate])

    # 注册回中按钮
    def register_reset_button(self, bind_key_name: str = "none"):
        self.add_after_pos_filter_list(bind_key_name, [f.zero])
        self.add_after_rot_filter_list(bind_key_name, [f.zero])

    # FPV模式:无限制
    def mode_fpv(self, bind_key_name: str = "none"):
        self.add_pre_pos_filter_list(bind_key_name, [])
        self.add_pre_rot_filter_list(bind_key_name, [])

    # 无人机模式:锁定z轴旋转
    def mode_drone(self, bind_key_name: str = "none"):
        # self.add_pre_pos_filter_list(bind_key_name, [f.unchange])
        # self.add_pre_rot_filter_list(bind_key_name, [f.z_zero])
        self.add_after_rot_filter_list(bind_key_name, [f.z_zero])

    # 三脚架模式:固定在当前位置, 并且锁定z轴旋转
    def mode_tripod(self, bind_key_name: str = "none"):
        self.add_after_pos_filter_list(bind_key_name, [f.unchange])
        self.add_after_rot_filter_list(bind_key_name, [f.z_zero])

    # 定速巡航模式:保持进入状态时的速度不变
    def mode_cruise(self, bind_key_name: str = "none"):
        self.add_pre_pos_filter_list(bind_key_name, [f.unchange])
        self.add_pre_rot_filter_list(bind_key_name, [f.unchange])

    # 滑轨模式:固定在当前高度平面, 并且锁定z轴旋转
    def mode_slide(self, bind_key_name: str = "none"):
        self.add_after_pos_filter_list(bind_key_name, [f.z_unchange])
        self.add_after_rot_filter_list(bind_key_name, [f.z_zero])

    def update(self):
        super().update_raw_data()
        super().update()
