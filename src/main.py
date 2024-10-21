# -*- encoding: UTF-8 -*- 

import yaml

from communication.naoCommunication import NaoCommunication 
from movements.NaoMovements import NaoMovements

def main():
        with open('src/configs/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            ip = config['robot']['ip']
            port = config['robot']['port']
            openAiKey = config['robot']['openAiKey']
            context = config['robot']['context']
        
        #naoMovements = NaoMovements(ip, port)
        #naoMovements.Balance()
        naoCommunication  = NaoCommunication(ip, port, openAiKey,context)
        naoCommunication.Start("presentate")

        
    

if __name__ == "__main__":
    main()