# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:28:51 2021

@author: Andre
"""

#import random
import numpy as np


from CryptoGenerator.Action import Action
from CryptoGenerator.Action import ActionType
#from CryptoGenerator.InputData import InputData

class Strategy:
    
    
    def __init__(self):
        self.create_strategy()
    
    
    def receive_action(self, input_data):
        data = input_data.processed_data()
        return np.random.choice(self.__action_list, 1)[0]
    
    
    def update(self, wallet):
        pass
    
    
    def get_action_list(self):
        return __action_list
    
    
    def create_strategy(self):
        self.__action_list = np.empty(3, dtype=Action)
        self.__action_list[0] = Action(ActionType.BUY, 100)
        self.__action_list[0] = Action(ActionType.BUYALL)
        self.__action_list[1] = Action(ActionType.HOLD)
        self.__action_list[2] = Action(ActionType.SELL, 100)
        self.__action_list[2] = Action(ActionType.SELLALL)
        
        