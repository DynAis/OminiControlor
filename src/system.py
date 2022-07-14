import scope
import process as l2
import numpy as np

class Camera(l2.Preocess):
  def __init__(self):
    super().__init__()
    

  def __str__(self) -> str:
    return super().__str__()

  def update(self):
    super().update_raw_data()
    super().update()