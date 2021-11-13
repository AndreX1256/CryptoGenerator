# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 16:37:31 2021

@author: Andre
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:28:51 2021

@author: Andre
"""


import numpy as np

from CryptoGenerator.Action import Action
from CryptoGenerator.Action import ActionType

from CryptoGenerator.Strategy import Strategy


class StrategyScripted(Strategy):
    
    
    def __init__(self):
        self.create_strategy()
        self.__buy_threshold = 34250
        self.__sell_threshold = 35750
    
    
    def receive_action(self, input_data):
        if input_data.get_bitcoin_price() < self.__buy_threshold and input_data.get_wallet().euros() > 10.0:
            return Action(ActionType.BUYALL)
        if input_data.get_bitcoin_price() > self.__sell_threshold and input_data.get_wallet().bitcoins() * input_data.get_bitcoin_price() > 10.0:
            return Action(ActionType.SELLALL)
        else:
            return Action(ActionType.HOLD)
            
    
    def update(self, wallet):
        pass
    
    
    def create_strategy(self):
        self.__action_list = np.empty(5, dtype=Action)
        self.__action_list[0] = Action(ActionType.BUY, 100)
        self.__action_list[1] = Action(ActionType.BUYALL)
        self.__action_list[2] = Action(ActionType.HOLD)
        self.__action_list[3] = Action(ActionType.SELL, 100)
        self.__action_list[4] = Action(ActionType.SELLALL)
        
        