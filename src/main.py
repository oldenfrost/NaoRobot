# -*- encoding: UTF-8 -*- 

import yaml

from communication.naoCommunication import NaoCommunication 
from movements.NaoMovements import NaoMovements
from utils.helpers import Helpers

def main():

        config=Helpers.GetConfig()
        naoCommunication  = NaoCommunication(config[0], config[1], config[2],config[3])
        naoCommunication.Start("presentate")

if __name__ == "__main__":
    main()