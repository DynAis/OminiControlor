from multiprocessing.dummy import Process
import scope
import event as l1
import filters as f
import time
import numpy as np
from scipy.spatial.transform import Rotation as R


class Process(l1.Event):
    def __init__(self, device_number: int=0):
        super().__init__(device_number)
        self.STOP_EVALUATE_FLAG = False
        self.AS_VARIABLE_TUNNER = False
        # self.CRUISE_COUNTROL = False
        # self.cruise_pos_diff = np.array([0, 0, 0])
        # self.cruise_rot_diff = np.array([0, 0, 0])
        # self.variable_list = []
        self.pre_pos = np.array([0, 0, 0])
        self.pre_rot = np.array([0, 0, 0])
        self.pos = np.array([0, 0, 0])  # in meter
        self.rot = np.array([0, 0, 0])  # in rad
        # filter list that storage filter function handle
        self.pre_pos_filter_list = []
        self.pre_rot_filter_list = []
        self.after_pos_filter_list = []
        self.after_rot_filter_list = []
        self.button_func_list = []
        for i in range(len(self.event_dict)):
            self.pre_pos_filter_list.append([])
            self.pre_rot_filter_list.append([])
            self.after_pos_filter_list.append([])
            self.after_rot_filter_list.append([])
            self.button_func_list.append([])

    def __str__(self) -> str:
        return super().__str__()

    def stop_evaluate(self):
        self.STOP_EVALUATE_FLAG = True

    def start_evaluate(self):
        self.STOP_EVALUATE_FLAG = False

    def toggle_evaluate(self):
        self.STOP_EVALUATE_FLAG = not self.STOP_EVALUATE_FLAG
        if self.STOP_EVALUATE_FLAG:
            self.stop_evaluate()
        else:
            self.start_evaluate()

    def start_variable_tunner(self):
        self.AS_VARIABLE_TUNNER = True

    def stop_variable_tunner(self):
        self.AS_VARIABLE_TUNNER = False

    # def start_cruise_control(self):
    #     self.CRUISE_COUNTROL = True
    #     self.cruise_pos_diff = self.pos_diff
    #     self.cruise_rot_diff = self.rot_diff

    # def stop_cruise_control(self):
    #     self.CRUISE_COUNTROL = False

    # def toggle_cruise_control(self):
    #     self.CRUISE_COUNTROL = not self.CRUISE_COUNTROL
    #     if self.CRUISE_COUNTROL:
    #         self.cruise_pos_diff = np.array([-self.raw.x, self.raw.z, self.raw.y])
    #         self.cruise_rot_diff = np.array([self.raw.pitch, -self.raw.yaw, self.raw.roll])

    def __update_position(self):
        # rotation_matrix = R.from_euler("xyz", self.rot).as_matrix()
        # # calculate rotated position, change pos to another base vector space.
        # pos = np.matmul(self.pos, rotation_matrix)
        # # calculate position
        # pos = pos + self.pos_diff
        # # return to original base vector space
        # pos = np.matmul(pos, np.linalg.inv(rotation_matrix))
        # self.pos = pos

        # storage pre_pos
        self.pre_pos = self.pos
        # calculate rotation matrix
        rotation_matrix = R.from_euler("xyz", self.rot).as_matrix()
        # 对位移误差进行左乘旋转矩阵,得到当前旋转下的位移在原空间中的数值
        pos_diff = np.transpose(np.matmul(rotation_matrix, np.transpose(self.pos_diff)))
        self.pos = self.pos + pos_diff

    # TODO: 待修改
    def __update_rotation(self):
        # storage pre_rot
        self.pre_rot = self.rot
        # rot alone y-x-z
        self.rot = self.rot + self.rot_diff
        # rot = np.matmul(R.from_euler('xyz', rot).as_matrix(), R.from_euler('xyz', kp_rot *diff_rot).as_matrix())
        # rot = R.from_matrix(rot).as_euler('xyz')
        # get dicimal part
        self.rot = np.mod(self.rot, 2 * np.pi)
        # self.rot[2] = 0

        # rot = R.from_euler('xyz', self.rot)
        # rot_diff_x = R.from_euler('xyz', (self.rot_diff[0],0,0))
        # rot_diff_y = R.from_euler('xyz', (0,self.rot_diff[1],0))
        # rot_diff_z = R.from_euler('xyz', (0,0,self.rot_diff[2]))
        # # 对原有旋转矩阵左乘, 施加一个新的旋转
        # rot = rot_diff_z * rot_diff_y * rot_diff_x * rot
        # self.rot = np.mod(self.rot, 2 * np.pi)
        # self.rot = rot.as_euler('xyz')

    def add_pre_pos_filter_list(self, event_name: str = "none", func_list: list = []):
        event_number = self.event_dict[event_name]
        if len(func_list) > 0:
            for func in func_list:
                self.pre_pos_filter_list[event_number].append(func)
        else:
            print("add_pre_pos_filter: func_list is empty")

    def add_pre_rot_filter_list(self, event_name: str = "none", func_list: list = []):
        event_number = self.event_dict[event_name]
        if len(func_list) > 0:
            for func in func_list:
                self.pre_rot_filter_list[event_number].append(func)
        else:
            print("add_pre_rot_filter: func_list is empty")

    def add_after_pos_filter_list(self, event_name: str = "none", func_list: list = []):
        event_number = self.event_dict[event_name]
        if len(func_list) > 0:
            for func in func_list:
                self.after_pos_filter_list[event_number].append(func)
        else:
            print("add_after_pos_filter: func_list is empty")

    def add_after_rot_filter_list(self, event_name: str = "none", func_list: list = []):
        event_number = self.event_dict[event_name]
        if len(func_list) > 0:
            for func in func_list:
                self.after_rot_filter_list[event_number].append(func)
        else:
            print("add_after_rot_filter: func_list is empty")

    def add_func_list(self, event_name: str = "none", func_list: list = []):
        event_number = self.event_dict[event_name]
        if len(func_list) > 0:
            for func in func_list:
                self.button_func_list[event_number].append(func)
        else:
            print("add_func: func_list is empty")

    # the most importent function
    def update(self):
        super().update()
        state_list = self.get_active_event_state_list()

        # Process function ataccording to event state
        for state in state_list:
            if len(self.button_func_list[state]) > 0:
                try:
                    for func in self.button_func_list[state]:
                        func()
                except Exception as e:
                    print("update: button_func_list error: {}".format(e))

        # if flag is True, stop process
        if self.STOP_EVALUATE_FLAG:
            return

        # Process pre filter
        for state in state_list:
            # pre filter list not empty
            if len(self.pre_pos_filter_list[state]) > 0:
                try:
                    for func in self.pre_pos_filter_list[state]:
                        self.pos_diff = func(self.pre_pos_diff, self.pos_diff)
                except Exception as e:
                    print("update: pos_filter_list error: {}".format(e))
            if len(self.pre_rot_filter_list[state]) > 0:
                try:
                    for func in self.pre_rot_filter_list[state]:
                        self.rot_diff = func(self.pre_rot_diff, self.rot_diff)
                except Exception as e:
                    print("update: rot_filter_list error: {}".format(e))

        if not self.AS_VARIABLE_TUNNER:
            # update position
            self.__update_position()
            # update rotation
            self.__update_rotation()

        # Process after filter
        for state in state_list:
            # after filter list not empty
            if len(self.after_pos_filter_list[state]) > 0:
                try:
                    for func in self.after_pos_filter_list[state]:
                        self.pos = func(self.pre_pos, self.pos)
                except Exception as e:
                    print("update: after_pos_filter_list error: {}".format(e))
            if len(self.after_rot_filter_list[state]) > 0:
                try:
                    for func in self.after_rot_filter_list[state]:
                        self.rot = func(self.pre_rot, self.rot)
                except Exception as e:
                    print("update: after_rot_filter_list error: {}".format(e))


# output data to vofa as debuger
@scope.send_to_vofa
def debug_l2(filter: Process):
    # convert to csv string
    MESSAGE = ",".join(
        map(
            str,
            (
                filter.t,
                filter.pos_diff[0],
                filter.pos_diff[1],
                filter.pos_diff[2],
                filter.rot_diff[0],
                filter.rot_diff[1],
                filter.rot_diff[2],
                filter.l_button_pressed,
                filter.r_button_pressed,
                filter.event,
                filter.t_diff,
                filter.l_button.button_hold_time,
                filter.r_button.button_hold_time,
                filter.get_event_state("left_button_click"),
                filter.get_event_state("right_button_click"),
                filter.get_event_state("left_button_hold"),
                filter.get_event_state("right_button_hold"),
                filter.get_event_state("left_button_double_click"),
                filter.get_event_state("right_button_double_click"),
                filter.get_event_state("all_button_click"),
                filter.get_event_state("all_button_hold"),
                filter.get_event_state("all_button_double_click"),
                filter.get_event_state("push_double"),
            ),
        )
    )
    MESSAGE = MESSAGE + "\n"
    return MESSAGE


@scope.send_to_vofa
def debug_l2_final(filter: Process):
    # convert to csv string
    MESSAGE = ",".join(
        map(
            str,
            (
                filter.t,
                filter.pos[0],
                filter.pos[1],
                filter.pos[2],
                filter.rot[0],
                filter.rot[1],
                filter.rot[2],
                filter.l_button_pressed,
                filter.r_button_pressed,
                filter.event,
                filter.t_diff,
                filter.l_button.button_hold_time,
                filter.r_button.button_hold_time,
                filter.get_event_state("left_button_click"),
                filter.get_event_state("right_button_click"),
                filter.get_event_state("left_button_hold"),
                filter.get_event_state("right_button_hold"),
                filter.get_event_state("left_button_double_click"),
                filter.get_event_state("right_button_double_click"),
                filter.get_event_state("all_button_click"),
                filter.get_event_state("all_button_hold"),
                filter.get_event_state("all_button_double_click"),
                filter.get_event_state("push_double"),
            ),
        )
    )
    MESSAGE = MESSAGE + "\n"
    return MESSAGE


if __name__ == "__main__":
    filter = Process()
    # append filter function to filter list according to event
    filter.add_after_pos_filter_list("left_button_hold", [f.amp_0_8])
    filter.add_after_rot_filter_list("left_button_hold", [f.amp_0_8])

    filter.register_toggle("right_button_click")
    filter.add_pre_pos_filter_list("right_button_click", [f.exp])
    filter.add_pre_rot_filter_list("right_button_click", [f.exp])

    while True:
        filter.update_raw_data()
        filter.update()
        print(filter)
        debug_l2_final(filter)
        time.sleep(0.01)
