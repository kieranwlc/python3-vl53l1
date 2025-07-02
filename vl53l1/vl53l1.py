import ctypes
from ctypes import CDLL
import os

import logging
logger = logging.getLogger(__name__)

class VL53L1X_Result(ctypes.Structure):
    _fields_ = [
        ("status", ctypes.c_uint8),
        ("distance", ctypes.c_uint16),
        ("ambient", ctypes.c_uint16),
        ("signal", ctypes.c_uint16),
        ("numSPADS", ctypes.c_uint16),
    ]

    def __repr__(self):
        return f"Result(Status = {self.status}, dist = {self.distance}, Ambient = {self.ambient}, Signal = {self.signal}, #ofSpads = {self.numSPADS} )"  

class ToFSensor:
    def __init__(self):
        self._lib = CDLL(os.path.dirname(os.path.realpath(__file__)) + "/STSW-IMG013_v1.1.1/user_lib/libtof.so")

        self._lib.init_tof.argtypes = [ctypes.c_int]
        self._lib.init_tof.restype = ctypes.c_int

        self._lib.start_tof.restype = ctypes.c_int
        self._lib.stop_tof.restype = ctypes.c_int
        self._lib.get_distance.restype = ctypes.c_int

        # [dev , *offset]
        self._lib.VL53L1X_GetOffset.argtypes = [ctypes.c_uint16, ctypes.POINTER(ctypes.c_int16)]
        self._lib.VL53L1X_GetOffset.restype = ctypes.c_int8

        self._lib.VL53L1X_SetOffset.argtypes = [ctypes.c_uint16, ctypes.c_int16]
        self._lib.VL53L1X_SetOffset.restype = ctypes.c_int8

        # [dev, target, *offset]
        self._lib.VL53L1X_CalibrateOffset.argtypes = [ctypes.c_uint16, ctypes.c_uint16, ctypes.POINTER(ctypes.c_int16)]
        self._lib.VL53L1X_CalibrateOffset.restype = ctypes.c_int8

        # [dev , *offset]
        self._lib.VL53L1X_GetXtalk.argtypes = [ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint16)]
        self._lib.VL53L1X_GetXtalk.restype = ctypes.c_int8

        self._lib.VL53L1X_SetXtalk.argtypes = [ctypes.c_uint16, ctypes.c_uint16]
        self._lib.VL53L1X_SetXtalk.restype = ctypes.c_int8

        # [dev, target, *offset]
        self._lib.VL53L1X_CalibrateXtalk.argtypes = [ctypes.c_uint16, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint16)]
        self._lib.VL53L1X_CalibrateXtalk.restype = ctypes.c_int8
        
    def set_roi(self, width: int, height: int):
        """
        Sets the ROI (Region of Interest) size for the sensor.
        :param width: Width of the ROI (4 to 16)
        :param height: Height of the ROI (4 to 16)
        """
        if width < 4 or width > 16 or height < 4 or height > 16:
            raise ValueError("ROI width and height must be between 4 and 16.")

        # Dev number isn't used so we use zero
        ret = self._lib.VL53L1X_SetROI(0, width, height)
        if ret:
            raise Exception("Setting ROI failed")
        print(f"ROI set to width: {width}, height: {height}")

    def get_roi(self):
        """
        Retrieves the current ROI settings.
        :return: Tuple (width, height) of the current ROI.
        """
        width = ctypes.c_uint8(0)
        height = ctypes.c_uint8(0)
        ret = self._lib.VL53L1X_GetROI(0, ctypes.byref(width), ctypes.byref(height))
        if ret:
            raise Exception("Getting ROI failed")
        return width.value, height.value

    def init_tof(self) -> int:
        """ 
        returns 0 on success
        """
        return self._lib.init_tof(3)

    def  start_tof(self) -> int:
        """"
        start a ToF measurement cycle
 
        return 0 on success
        """
        return self._lib.start_tof()

    def stop_tof(self) -> int:
        """
        return 0 on success
        """
        return self._lib.stop_tof()

    def get_distance(self) -> int:
        result = self._lib.get_distance()
        return result 
    
    def get_offset(self) -> int:
        """
        returns current offset in mm
        """
        # initialize with arbitrary value
        value = ctypes.c_int16(42)
        ptr = ctypes.pointer(value)

        # Dev number isn't used so we use zero
        ret = self._lib.VL53L1X_GetOffset(0, ptr)
        if ret:
            raise Exception("Error in get offset")

        return ptr[0]


    def set_offset(self, offset: int):
        """
        offset in mm
        """
        # Dev number isn't used so we use zero
        ret = self._lib.VL53L1X_SetOffset(0, offset)
        if ret: 
            raise Exception("Setting offset failed")
    
    def calibrate_offset(self, target_distance: int) -> int:
        """
        target_distance in mm

        returns offset in mm
        """
        # initialize with arbitrary value
        value = ctypes.c_int16(42)
        ptr = ctypes.pointer(value)

        # Dev number isn't used so we use zero
        ret = self._lib.VL53L1X_CalibrateOffset(0, target_distance, ptr)
        if ret:
            raise Exception("Error in calibrating offset")

        return ptr[0]

    def get_xtalk(self) -> int:
        """
        returns current xtalk in counts per second
        """
        # initialize with arbitrary value
        value = ctypes.c_uint16(42)
        ptr = ctypes.pointer(value)

        # Dev number isn't used so we use zero
        ret = self._lib.VL53L1X_GetXtalk(0, ptr)
        if ret:
            raise Exception("Error in get xtalk")

        return ptr[0]


    def set_xtalk(self, offset: int):
        """
        offset in counts per second
        """
        # Dev number isn't used so we use zero
        ret = self._lib.VL53L1X_SetXtalk(0, offset)
        if ret: 
            raise Exception("Setting xtalk failed")
    
    def calibrate_xtalk(self, target_distance: int) -> int:
        """
        target_distance in mm

        returns offset in mm
        """
        # initialize with arbitrary value
        value = ctypes.c_uint16(42)
        ptr = ctypes.pointer(value)

        # Dev number isn't used so we use zero
        ret = self._lib.VL53L1X_CalibrateXtalk(0, target_distance, ptr)
        if ret:
            raise Exception("Error in calibrating offset")

        return ptr[0]
