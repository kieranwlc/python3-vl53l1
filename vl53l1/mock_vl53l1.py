from time import time
from .vl53l1 import ToFSensor

class MockToFSensor(ToFSensor):
    def __init__(self):
        self.distance = 200
        self.direction = 1
        self.speed = 30
        self.last_time = time() 

    def init_tof(self) -> int:
        return 0

    def start_tof(self) -> int:
        return 0

    def stop_tof(self) -> int:
        return 0
    
    def set_roi(self, width: int, height: int):
        pass

    def get_distance(self) -> int:
        # Calculate the time elapsed since the last measurement
        current_time = time()
        elapsed_time = current_time - self.last_time
        self.last_time = current_time

        # Update the distance based on elapsed time and direction
        self.distance += self.direction * self.speed * elapsed_time

        # Reverse direction if the limits are reached
        if self.distance >= 250:
            self.distance = 250
            self.direction = -1
        elif self.distance <= 20:
            self.distance = 20
            self.direction = 1

        return round(self.distance)

    def set_offset(self, offset):
        pass

    def set_xtalk(self, offset):
        pass

