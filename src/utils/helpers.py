# -*- encoding: UTF-8 -*-
import math
class Helpers():
    @staticmethod
    def GetArrayRadians(arrayAngles):
       arrayRadians = []
       for angle in arrayAngles:
           arrayRadians.append(math.radians(angle))

       return  arrayRadians
        
