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
            self.postureProxy = ALProxy("ALRobotPosture", ip, port)

        except Exception as e:
            print("no se pudo crear el",str(e))

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
        self.postureProxy.goToPosture("Stand", 1)
        while self.stopEvent.is_set():
            self.LowFrontDoubleBiceps()
            self.HighFrontDoubleBiceps()
            self.SideChest()
     
#funciones sobre las posiciones iniciales  
    def LowFrontDoubleBiceps(self):
        time.sleep(2)
        angles = [
            0.0,-6.4, 
            63.0, 16.7, -12.4, -63.2, 0.3, 0.25, 
            63.0, -16.7, 12.4, 63.2, 0.3, 0.25, 
            -9.7, 6.6, 7.2, -5.1, 4.9, -6.1, 
            -9.7, -6.6, 7.2, -5.1, 4.9, 6.1      
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(self.names, angles, times, True)

    def HighFrontDoubleBiceps(self):
        time.sleep(2)
        angles = [
             0.0,-9.7, 
            -38.3, 61.5, -46.8, -85.1, -77.1, 0.01,
            -38.3, -61.5, 46.8, 85.1, 77.1, 0.01,
            -9.7, 6.6, 7.2, -5.1, 4.9, -6.1, 
            -9.7, -6.6, 7.2, -5.1, 4.9, 6.1    
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)

        self.motionProxy.angleInterpolation(self.names, angles, times, True)

    def SideChest(self):
        time.sleep(2)
        angles = [
            -32.3, -12.7, 
            -4.1, 62.9, -69.1, -88.3, -75.3, 0.0,  
            -26.2, -53.1, 81.1, 20.6, -36.7, 0.99, 
            -9.7, 6.6, 7.2, -5.1, 4.9, -6.1, 
            -9.7, -6.6, 7.2, -5.1, 4.9, 6.1    
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
        names = [
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"
        ]
        angles = [
            -0.7, -23.4, 6.9, 28.8, 81.1, 0.0,
            -0.6, 23.4, -12.1, -28.8, -81.1, 0.0
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)

        self.motionProxy.angleInterpolation(names, angles, times, True)


    def PushDonw(self):
        names = [
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"
        ]
        angles = [
            -0.7, -75.5, 6.6, 87.1, 81.1, 0.0,
            -0.6, 75.6, -5.7, -87.0, -81.1, 0.0
        ]
        times = 2.0
        angles = Helpers.GetArrayRadians(angles)

        self.motionProxy.angleInterpolation(names, angles, times, True)


    def StartPositionSquad(self):
        self.StiffnessOn()
        self.postureProxy.goToPosture("StandZero", 0.8)

    def StartPositionCrunch(self):
        self.StiffnessOn()
        self.postureProxy.goToPosture("Sit", 0.8)
        self.AnimationCrunch()

    def SetPosition(self,position):
        self.StiffnessOn()
        self.postureProxy.goToPosture(position, 0.8)

#funcion para ubicar la posicion inicial  
    def StartPositionPushUp(self):
        self.StiffnessOn()
        self.postureProxy.goToPosture("LyingBelly", 0.8)
        self.AnimationPushUp()




#funciones que realizan los movimientes respectivos para ubicar el robot en posicion de largatija
    def AnimationPushUp(self):
        names = [
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"
        ]
        times = 2.0
        angles = [
        -56.2, -15.9, 10.6, 63.2, 90.5, 0.0,
        -55.3, 15.9, -10.1, -62.4, -90.8, 0.0    
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        -55.9, -17.9, 10.5, 71.3,94.7, 0.0,
        -54.8, 17.9, -10.2, -71.3,-94.7, 0.0  
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        -42.9, -17.2, 6.0, 81.4,94.7, 0.0,
        -42.9, 19.2, -5.9, -79.5,-94.7, 0.0   
        ]

        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)


        angles = [
        -36.5, -17.2, 6.0, 81.4,94.7, 0.0,
        -36.4, 19.2, -5.9, -79.5,-94.7, 0.0   
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)


        angles = [
        -0.5, -17.2, 6.3, 87.2,94.7, 0.0,
        -0.5, 18.6, -5.7, -87.1,-94.7, 0.0   
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        -0.5, -17.2, 6.3, 87.2,94.7, 0.0,
        -0.5, 18.6, -5.7, -87.1,-94.7, 0.0   
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        -0.5, -17.2, 6.3, 87.2,94.7, 0.0,
        -0.5, 64.6, -5.7, -87.1,-94.7, 0.0   
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        -0.5, -64.6, 6.3, 87.2,94.7, 0.0,
        -0.5, 64.6, -5.7, -87.1,-94.7, 0.0   
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        -0.5, -75.9, 6.3, 87.2,94.7, 0.0,
        -0.5, 75.7, -5.7, -87.1,-94.7, 0.0   
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        names = [
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll",
        "HeadYaw", "HeadPitch"
        ]
        angles = [
        -1.4, 10.3, 6.1, -5.1,52.0, 9.7,   
        -1.4, -10.3, 6.1, -5.1,52.0, 9.7,
        -4.6, -7.5
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)
        names = [
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"
        ]
        angles = [
        -1.4, 10.3, 6.1, -5.1,7.2, 9.7,   
        -1.4, -10.3, 6.1, -5.1,7.2, 9.7
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)


    
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
    
    def AnimationCrunch(self):
        times = 1.0 
        names = [
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"
        ]
        angles = [
        50.3, -20.6, 29.6, 2.4, -1.7, 0.0, 
        46.3, 18.2, -26.0, -2.2, 1.9, 0.0,  
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        93.7, -19.8, 29.1, 2.4, 16.0, 0.0, 
        94.4, 17.9, -25.4, -2.2, -16.0, 0.0,  
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        106.8, -18.1, 69.7, 2.4, 16.0, 0.0, 
        107.0, 15.8, -69.7, -2.2, -16.0, 0.0,  
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)


        names = [
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"
        ]
        angles = [
        -21.8, 14.0,-88.0, 80.5, 48.7, -0.9, 
        -21.8, -14.0,-88.0, 80.5, 48.7, 1.5   
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        -12.4, 17.3,-88.0, 80.5, 47.9, -0.9, 
        -12.7, -7.3,-88.0, 80.5, 48.7, 1.5   
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        names = [
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand",
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"
        ]
        angles = [
        119.5,-18.6,69.7, 2.1, 15.6, 0.00, 
        119.5,16.2,-69.6, -2.6, -15.6, 0.00,  
        -1.1, 0.9,-87.9, 80.0, 47.9, -0.9, 
        -1.1, -0.9,-88.0, 80.5, 48.7, 1.5   
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        119.5,-25.3,77.2, 2.1, 12.0, 0.00, 
        119.5,25.3,-77.2, -2.6, -12.0, 0.00,  
        -1.5, 1.1,-87.9, 85.0, 48.5, -0.9, 
        -1.5, -1.4,-87.9, 85.0, 48.5, 1.5, 
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)
  
        angles = [
        119.5,-44.3,79.3, 2.1, -15.6, 0.00, 
        119.5,44.3,-79.3, -2.1, 15.6, 0.00,  
        -1.5, 1.1,-87.9, 93.7, 48.5, -0.9, 
        -1.5, -1.4,-87.9, 93.7, 48.5, 1.5, 
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        angles = [
        119.5,-66.0,79.3, 2.1, -15.6, 0.00, 
        119.5,66.0,-79.3, -2.6, 15.6, 0.00,  
        -1.5, 1.1,-87.9, 109.9, 48.5, -0.9, 
        -1.5, -1.4,-87.9, 109.9, 48.5, 1.5, 
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)
        angles = [
        119.5,-75.5,79.3, 30.6, 28.0, 0.00, 
        119.5,66.0,-79.3, -30.4, -28.0, 0.00,  
        -1.5, 1.1,-87.9, 121.0, 48.5, -0.9, 
        -1.5, -1.4,-87.9, 121.0, 48.5, 1.5, 
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)

        names = [
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"
        ]
        angles = [
        71.6, -53.5,78.8, 30.6, 27.8, 0.0, 
        72.0, 53.8,-78.8, 30.1, -27.8, 0.0, 
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)
        angles = [
        71.6, -16.1,78.8, 30.6, 27.8, 0.0, 
        72.0, 16.1,-78.8, 30.1, -27.8, 0.0, 
        ]
        angles = Helpers.GetArrayRadians(angles)
        self.motionProxy.angleInterpolation(names, angles, times, True)



    







    

        


        

         
        
