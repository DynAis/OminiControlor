import spacenavigator
import time

def connect_device(device_number=0):
  device = spacenavigator.open(device_number)
  if device:
    return device
  else:
    raise Exception("Device not found")

# use after connect_device()
def get_state():
  state = spacenavigator.read()
  return state

def read_position(state):
  return (state.x, state.y, state.z)

def read_rotation(state):
  return (state.pitch, state.roll, state.yaw)

def read_buttons(state):
  return (state.buttons)

def read_time(state):
  return (state.t)

if __name__ == "__main__":
  device = connect_device()
  while True:
    state = get_state()
    print(state)
    time.sleep(0.1)