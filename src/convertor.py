import time
from pythonosc import udp_client
import numpy as np


class VRC_UAVCam_Client:
    def __init__(self, ip: str = "127.0.0.1", port: int = 9000):
        self.positions = np.zeros(3)
        self.rotation = np.zeros(3)
        self.ENABLE = False
        self.FOLLOW = False
        self.AF = True
        # vrc lens parameters
        self.VRCLZoomRadial = 0.3
        self.VRCLExposureRadial = 0.5
        self.VRCLApertureRadial = 0.17
        self.VRCLFocusRadial = 0.5
        self.osc_client = udp_client.SimpleUDPClient(ip, port)
        self.uav_stop()
        self.uav_disable_follow()
        self.sync_zoom()
        self.sync_exposure()
        self.sync_aperture()
        self.sync_focus()

    def __output_space_conversion(self, pos: np.ndarray, rot: np.ndarray):
        # change to left hand coordinate system
        self.positions[0] = -pos[0]
        self.positions[1] = pos[1]
        self.positions[2] = pos[2]
        self.positions = (self.positions + 100) / 200

        self.rotation[0] = rot[0]
        self.rotation[1] = 2 * np.pi - rot[1]
        self.rotation[2] = 2 * np.pi - rot[2]
        for i in range(3):
            if 0 <= self.rotation[i] <= np.pi:
                self.rotation[i] = (self.rotation[i] + np.pi) / (2 * np.pi)
            else:
                self.rotation[i] = (self.rotation[i] - np.pi) / (2 * np.pi)

        # self.rotation = np.mod(self.rotation, 1)

    def is_enabled(self):
        return self.ENABLE

    def vrcl_feature(self, feature_number: int):
        # is integer assert
        assert isinstance(feature_number, int)
        self.osc_client.send_message(
            "/avatar/parameters/VRCLFeatureToggle", feature_number
        )
        time.sleep(0.1)
        self.osc_client.send_message("/avatar/parameters/VRCLFeatureToggle", 0)
        print("feature:", feature_number)

    def vrcl_start(self):
        self.vrcl_feature(254)
        print("vrcl: enable camera")

    def vrcl_stop(self):
        self.osc_client.send_message("/avatar/parameters/VRCLFeatureToggle", 254)
        time.sleep(0.5)
        self.osc_client.send_message("/avatar/parameters/VRCLFeatureToggle", 0)
        print("vrcl: disable camera")

    def vrcl_toggle_hud(self):
        self.vrcl_feature(226)
        print("vrcl: toggled hud")

    def vrcl_toggle_af(self):
        self.AF = not self.AF
        if self.AF:
            self.osc_client.send_message("/avatar/parameters/VRCLFocusRadial", False)
        else:
            self.sync_focus()
        print("vrcl: toggled af")

    def vrcl_toggle_avatar_focus(self):
        self.vrcl_feature(13)
        print("vrcl: toggled avatar focus")

    def vrcl_toggle_focus_peak(self):
        self.vrcl_feature(1)
        self.vrcl_feature(51)
        print("vrcl: toggled focus peak")

    def vrcl_toggle_portrait(self):
        self.vrcl_feature(222)
        print("vrcl: toggled portrait")

    def vrcl_toggle_vr_mount(self):
        self.vrcl_feature(223)
        print("vrcl: toggled vr mount")

    def toggle_start_stop(self):
        enable = not self.ENABLE
        if enable:
            self.uav_start()
            self.vrcl_start()
        else:
            self.sync_state(np.zeros(3), np.zeros(3))
            self.uav_stop()
            self.vrcl_stop()
        self.ENABLE = enable
        time.sleep(0.5)

    def uav_start(self):
        self.osc_client.send_message("/avatar/parameters/UAV_Bool", True)
        self.ENABLE = True

    def uav_stop(self):
        self.osc_client.send_message("/avatar/parameters/UAV_Bool", False)
        self.ENABLE = False

    def uav_toggle_follow(self):
        b = not self.FOLLOW
        self.osc_client.send_message("/avatar/parameters/UAV_Follow", b)
        self.FOLLOW = b

    def uav_enable_follow(self):
        self.osc_client.send_message("/avatar/parameters/UAV_Follow", True)
        self.FOLLOW = True

    def uav_disable_follow(self):
        self.osc_client.send_message("/avatar/parameters/UAV_Follow", False)
        self.FOLLOW = False

    def sync_state(self, pos: np.ndarray, rot: np.ndarray):
        self.__output_space_conversion(pos, rot)
        self.osc_client.send_message("/avatar/parameters/UAV_PX", self.positions[0])
        self.osc_client.send_message("/avatar/parameters/UAV_PY", self.positions[1])
        self.osc_client.send_message("/avatar/parameters/UAV_PZ", self.positions[2])
        self.osc_client.send_message("/avatar/parameters/UAV_RX", self.rotation[0])
        self.osc_client.send_message("/avatar/parameters/UAV_RY", self.rotation[1])
        self.osc_client.send_message("/avatar/parameters/UAV_RZ", self.rotation[2])
        # debug
        # print(self.positions, self.rotation)

    def sync_zoom(self):
        self.osc_client.send_message(
            "/avatar/parameters/VRCLZoomRadial", self.VRCLZoomRadial
        )
        print("zoom:", self.VRCLZoomRadial)

    def sync_exposure(self):
        self.osc_client.send_message(
            "/avatar/parameters/VRCLExposureRadial", self.VRCLExposureRadial
        )
        print("exposure:", self.VRCLExposureRadial)

    def sync_aperture(self):
        self.osc_client.send_message(
            "/avatar/parameters/VRCLApertureRadial", self.VRCLApertureRadial
        )
        print("aperture:", self.VRCLApertureRadial)

    def sync_focus(self):
        if self.AF:
            return
        self.osc_client.send_message(
            "/avatar/parameters/VRCLFocusRadial", self.VRCLFocusRadial
        )
        print("focus:", self.VRCLFocusRadial)
