# -*- coding: utf-8 -*-
import threading
from naoqi import *
import almath
import time

from utils.helpers import Helpers

class NaoMovements:
    
    def __init__(self, ip, port):
        try:
            self.motionProxy = ALProxy("ALMotion", ip, port)
        except Exception as e:
            print("no se pudo crear el",e)
        try:
                self.postureProxy = ALProxy("ALRobotPosture", ip, port)

        except Exception as e:
            print("no se pudocrear el",e)

        self.names=self.GetNames()
        self.stopEvent = threading.Event()
        try:
            self.postureProxy.goToPosture("Stand", 0.5)
        except Exception as e:
            print("el error es el siguiente",e)
        self.StiffnessOn()  

# definir las partes  del cuerpo
    def GetNames(self):
            return [
            "HeadYaw", "HeadPitch",
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
            "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
            "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"
        ]
#animacion para las posiciones 
    def StartPosing(self):
        while self.stopEvent.is_set():
            self.LowFrontDoubleBiceps()
            self.HighFrontDoubleBiceps()
            self.SideChest()

        self.StiffnessOn()  
        self.postureProxy.goToPosture("Stand", 1)
        
#funciones sobre las posiciones iniciales  
    def LowFrontDoubleBiceps(self):

        angles = [
            0.0,-6.4, 
            63.0, 16.7, -12.4, -63.2, 0.3, 0.25, 
            63.0, -16.7, 12.4, 63.2, 0.3, 0.25, 
            -14.7, 0.1, -25.3, 40.1, -19.7, -0.4, 
            -14.7, -0.1, -25.3, 40.1, -19.7, 0.4      
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(self.names, angles, times, True)

    def HighFrontDoubleBiceps(self):
        angles = [
             0.0,-9.7, 
            -38.3, 61.5, -46.8, -85.1, -77.1, 0.01,
            -38.3, -61.5, 46.8, 85.1, 77.1, 0.01,
            -14.7, 0.1, -25.3, 40.1, -19.7, -0.4, 
            -14.7, -0.1, -25.3, 40.1, -19.7, 0.4
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)

        self.motionProxy.angleInterpolation(self.names, angles, times, True)

    def SideChest(self):
        angles = [
            -32.3, -12.7, 
            -4.1, 62.9, -69.1, -88.3, -75.3, 0.0,  
            -26.2, -53.1, 81.1, 20.6, -36.7, 0.99, 
            -14.7, 0.1, -25.3, 40.1, -19.7, -0.4, 
            -14.7, -0.1, -25.3, 40.1, -19.7, 0.4
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(self.names, angles, times, True)


# define la rigidez del cuerpo 
    def StiffnessOn(self):
        self.motionProxy.stiffnessInterpolation("Body", 1.0, 1.0)

    def StiffnessOff(self):
        self.motionProxy.stiffnessInterpolation("Body", 0.0, 1.0)



#animacion de las sentadillas
    def SquatsUp(self):
    
        angles = [
            0.0, -9.3, 
            12.8, 0.1, 68.5, 24.9, -66.9, 1.0,
            12.8, 0.1, -68.5, -25.2, 67.1, 1.0,
            -10.0, -6.5, 7.0,-4.8, 4.5, 5.8,
            -10.0, 6.5, 7.0,-4.8, 4.5, -6.1
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)

        self.motionProxy.angleInterpolation(self.names, angles, times, True)

    def SquatsDown(self):
        angles = [
            0.0, -9.3, 
            12.8, 0.1, 68.5, 24.9, -66.9, 1.0,
            12.8, 0.0, -68.5, -25.2, 67.1, 1.0,
            -10.0, -6.3, -66.5,84.4, -21.3, 6.3,
            -10.0, 6.3, -66.5,84.4, -21.3, -6.3
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)

        self.motionProxy.angleInterpolation(self.names, angles, times, True)

#animacion de las sentadillas
    def SitUp(self):
        angles = [
             0.0,-9.7, 
            59.6, -7.8, -67.0, -85.5, 16.5, 0.01,
            59.6, 7.8, 67.0, 85.5, -16.5, 0.01,
            -6.0, 3.2, -88.0, 77.2, 52.9, 0.4,
            -5.7, -3.2, -88.0, 76.9, 53.4, 0.2
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)

        self.motionProxy.angleInterpolation(self.names, angles, times, True)
    
    def SitDonw(self):
        angles = [
             0.0,-9.7, 
            59.6, -7.8, -67.0, -85.5, 16.5, 0.01,
            59.6, 7.8, 67.0, 85.5, -16.5, 0.01,
            -0.6, 6.7, -34.1, 77.2, 47.3, 0.7,
            -0.6, -6.7, -34.6, 77.0, 47.5, -0.1
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)

        self.motionProxy.angleInterpolation(self.names, angles, times, True) 

#animacion de las largatijas
    def PushUp(self):
        angles = [
             0.0,-9.7, 
            19.6, 19.1, -3.5, -18.4, -0.2, 0.01,
            19.6, -19.1, 3.5, 18.4, 0.2, 0.01,
            5.2, 1.1, -13.5, 4.7, -60.6, 4.3,
            5.2, -1.1, -13.5, 4.7, -60.6, -3.7,
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)

        self.motionProxy.angleInterpolation(self.names, angles, times, True)

    def PushDonw(self):
        angles = [
             0.0,-9.7, 
            19.6, 60.1, -2.0, -59.5, -0.2, 0.01,
            19.6, -60.1, 2.0, 59.5, 0.2, 0.01,
            5.2, 1.1, -13.5, 4.7, -60.6, 4.3,
            5.2, -1.1, -13.5, 4.7, -60.6, -3.7,
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)

        self.motionProxy.angleInterpolation(self.names, angles, times, True)


    def StartPositionExercise(self,position):
        self.StiffnessOff() 
        self.postureProxy.goToPosture(position, 1)
        if position=='Crouch':
            self.StartPositionPushUp()

#funcion para ubicar la posicion inicial  
    def StartPositionPushUp(self):
        self.Position_1()
        self.Position_2()
        self.Position_3()
   
    def EndPositionPushUp(self,position):
        self.Position_2()
        self.Position_1()
        self.postureProxy.goToPosture(position, 1)


#funciones que realizan los movimientes respectivos para ubicar el robot en posicion de largatija
    def Position_1(self):
        angles = [
        -0.5, 5.7, 
        31.3, 8.1, -26.3, -9.5, 32.0, 0.01,  
        31.3, -8.1, 26.3, 9.5, -32.0, 0.01,
        -3.9, -7.2, -87.5, 120.8, -67.1, 4.0, 
        -3.9, 7.8, -84.8, 121.0, -67.5,-3.4, 
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)
    
        self.motionProxy.angleInterpolation(self.names, angles, times, True)
    
    def Position_2(self):
        angles = [
        -0.5, 5.7,
        15.6, 7.9, -26.3, -10.1, 31.5, 0.00,  
        15.6, -8.1, 26.3, 10.1, -31.5, 0.00, 
        5.1, -5.1,-85.6, 76.6, -67.6, 4.3,  
        5.1, -0.7, -84.3, 75.5, -67.6, -4.1,
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(self.names, angles, times, True)

    def Position_3(self):
        angles = [
        -0.5, 5.7, 
        15.6, 7.9, -26.3, -10.1, 31.5, 0.00, 
        15.6, -8.1, 26.3, 10.1, -31.5, 0.00,  
        2.9, 0.4,-40.0, 21.0, -58.7, 4.1, 
        5.5, -6.5, -39.5, 20.8, -58.5, -3.4, 
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(self.names, angles, times, True)
    
    def Balance(self):
        self.StiffnessOn()
        self.postureProxy.goToPosture("StandInit", 0.5)
        space      = motion.FRAME_WORLD
        axisMask   = almath.AXIS_MASK_ALL   # full control
        isAbsolute = False
        effector   = "Torso"
        path       = [0.0, 0.07, -0.03, 0.0, 0.0, 0.0]
        times       = 2.0                    # seconds
        self.motionProxy.positionInterpolation(effector, space, path,
                                axisMask, times, isAbsolute)


        names = [
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand",
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll",
        ]
        angles = [
        25.6, -6.5, 43.5, 88.3, 20.2, 1.0, 
        25.6, 6.5, -43.5, -88.3, -20.2, 1.0,  
        -0.3, -16.1, -78.7, 10.7, 14.3, 16.2, 
        ]
        angles = Helpers.GetArrayRadians(angles)
        times = 1.0 
        self.motionProxy.angleInterpolation(names, angles, times, True)
        time.sleep(2)
        angles = [
        25.6, -6.5, 43.5, 88.3, 20.2, 1.0, 
        25.6, 6.5, -43.5, -88.3, -20.2, 1.0,  
        -0.2, -17.9, -37.4, 59.2, -28.3, 18.0, 
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)
        self.postureProxy.goToPosture("Stand", 0.5)







    

        


        

         
        
