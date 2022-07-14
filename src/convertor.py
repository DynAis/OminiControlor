from pythonosc import udp_client
import numpy as np


class VRC_UAVCam_Client:
    def __init__(self, ip: str = "127.0.0.1", port: int = 9000):
        self.positions = np.zeros(3)
        self.rotation = np.zeros(3)
        self.drone = False
        self.follow = False
        self.fullscreen = False
        self.osc_client = udp_client.SimpleUDPClient(ip, port)
        self.disable_drone()
        self.disable_follow()
        self.disable_fullscreen()

    def __output_space_conversion(self, pos: np.ndarray, rot: np.ndarray):
        # change to left hand coordinate system
        self.positions[0] = -pos[0]
        self.positions[1] = pos[1]
        self.positions[2] = pos[2]
        self.positions = (self.positions + 1000) / 2000
        
        self.rotation[0] = rot[0]
        self.rotation[1] = 2*np.pi-rot[1]
        self.rotation[2] = 2*np.pi--rot[2]
        for i in range(3):
            if 0<=self.rotation[i]<=np.pi:
                self.rotation[i] = (self.rotation[i]+np.pi) / (2*np.pi)
            else:
                self.rotation[i] = (self.rotation[i]-np.pi) / (2*np.pi)
            
        # self.rotation = np.mod(self.rotation, 1)

    def is_enabled(self):
        return self.drone

    def toggle_drone(self):
        b = not self.drone
        self.osc_client.send_message("/avatar/parameters/UAV_Bool", b)
        self.drone = b
    
    def enable_drone(self):
        self.osc_client.send_message("/avatar/parameters/UAV_Bool", True)
        self.drone = True

    def disable_drone(self):
        self.osc_client.send_message("/avatar/parameters/UAV_Bool", False)
        self.drone = False

    def toggle_fullscreen(self):
        b = not self.fullscreen
        self.osc_client.send_message("/avatar/parameters/UAV_FullScreen", b)
        self.fullscreen = b

    def enable_fullscreen(self):
        self.osc_client.send_message("/avatar/parameters/UAV_FullScreen", True)
        self.fullscreen = True

    def disable_fullscreen(self):
        self.osc_client.send_message("/avatar/parameters/UAV_FullScreen", False)
        self.fullscreen = False

    def toggle_follow(self):
        b = not self.follow
        self.osc_client.send_message("/avatar/parameters/UAV_Follow", b)
        self.follow = b

    def enable_follow(self):
        self.osc_client.send_message("/avatar/parameters/UAV_Follow", True)
        self.follow = True

    def disable_follow(self):
        self.osc_client.send_message("/avatar/parameters/UAV_Follow", False)
        self.follow = False

    def sync(self, pos: np.ndarray, rot: np.ndarray):
        self.__output_space_conversion(pos, rot)
        self.osc_client.send_message("/avatar/parameters/UAV_PX", self.positions[0])
        self.osc_client.send_message("/avatar/parameters/UAV_PY", self.positions[1])
        self.osc_client.send_message("/avatar/parameters/UAV_PZ", self.positions[2])
        self.osc_client.send_message("/avatar/parameters/UAV_RX", self.rotation[0])
        self.osc_client.send_message("/avatar/parameters/UAV_RY", self.rotation[1])
        self.osc_client.send_message("/avatar/parameters/UAV_RZ", self.rotation[2])
        # debug
        print(self.positions, self.rotation)
