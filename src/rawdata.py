import spacenavigator
import time
import scope
import numpy as np


class State:

    def __init__(self, device_number: int=0):
        self.DEVICE_NUMBER = device_number
        device = spacenavigator.open(self.DEVICE_NUMBER)
        if device:
            print("3dconnexion device opened successfully")
        else:
            raise Exception("3dconnexion device not found")
        self.pos_diff = np.array([0, 0, 0])
        self.rot_diff = np.array([0, 0, 0])
        self.pre_pos_diff = np.array([0, 0, 0])
        self.pre_rot_diff = np.array([0, 0, 0])
        self.t = 0
        self.l_button_pressed = 0
        self.r_button_pressed = 0
        self.raw = None

    def __str__(self) -> str:
        return "t: {}, pos_diff: {}, rot_diff: {}, l_button_pressed: {}, r_button_pressed: {}".format(
            self.t,
            self.pos_diff,
            self.rot_diff,
            self.l_button_pressed,
            self.r_button_pressed,
        )

    def update_raw_data(self):
        """ read raw data from 3dconnexion device
        """
        self.raw = spacenavigator.read()

    def update(self):
        """ use raw data to update state
        """
        self.t = time.perf_counter()
        self.pre_pos_diff = self.pos_diff
        self.pre_rot_diff = self.rot_diff
        self.pos_diff = np.array([-self.raw.x, self.raw.z, self.raw.y])
        self.rot_diff = np.array([self.raw.pitch, -self.raw.yaw, self.raw.roll])
        self.l_button_pressed = self.raw.buttons[0]
        self.r_button_pressed = self.raw.buttons[1]


@scope.send_to_vofa
def debug_l0(state: State):
    MESSAGE = ",".join(
        map(
            str,
            (
                state.t,
                state.pos_diff[0],
                state.pos_diff[1],
                state.pos_diff[2],
                state.rot_diff[0],
                state.rot_diff[1],
                state.rot_diff[2],
                state.l_button_pressed,
                state.r_button_pressed,
            ),
        )
    )
    MESSAGE = MESSAGE + "\n"
    return MESSAGE


if __name__ == "__main__":
    state = State()
    while True:
        state.update_raw_data()
        state.update()
        print(state)
        debug_l0(state)
        time.sleep(0.01)
