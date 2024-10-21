# -*- encoding: UTF-8 -*-
import math
import yaml
class Helpers():
    @staticmethod
    def GetArrayRadians(arrayAngles):
       arrayRadians = []
       for angle in arrayAngles:
           arrayRadians.append(math.radians(angle))

       return  arrayRadians

    @staticmethod
    def GetConfig():
        info=[]
        try:
            with open('src/configs/config.yaml', 'r') as file:
                config = yaml.safe_load(file)
                info.append(config['robot']['ip'])
                info.append(config['robot']['port'])
                info.append(config['robot']['openAiKey'])
                info.append(config['robot']['context'])
            return  info   
        except Exception as e:
            print("hubo un problema a leer el.yaml"+" :"+e)
           
