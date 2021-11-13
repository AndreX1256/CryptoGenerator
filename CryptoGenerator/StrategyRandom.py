# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:28:51 2021

@author: Andre
"""


import numpy as np

from CryptoGenerator.Action import Action
from CryptoGenerator.Action import ActionType

from CryptoGenerator.Strategy import Strategy


class StrategyRandom(Strategy):
    
    
    def __init__(self):
        self.create_strategy()
    
    
    def receive_action(self, input_data):
        return np.random.choice(self.__action_list, 1)[0]
    
    
    def update(self, wallet):
        pass
    
    
    def create_strategy(self):
        self.__action_list = np.empty(5, dtype=Action)
        self.__action_list[0] = Action(ActionType.BUY, 100)
        self.__action_list[1] = Action(ActionType.BUYALL)
        self.__action_list[2] = Action(ActionType.HOLD)
        self.__action_list[3] = Action(ActionType.SELL, 100)
        self.__action_list[4] = Action(ActionType.SELLALL)
        