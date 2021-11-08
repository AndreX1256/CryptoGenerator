# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:28:51 2021

@author: Andre
"""


from CryptoGenerator.StockMarket import StockMarket
from CryptoGenerator.Wallet import Wallet
import random
from enum import Enum
import numpy as np


class ActionType(Enum):
    HOLD = 1
    BUY = 2
    SELL = 3
    BUYALL = 4
    SELLALL = 5


class Action:
    
    def __init__(self, action_type, amount=0.0):
        self.__action_type = action_type
        self.__amount = amount
        
    def get_action_type(self):
        return self.__action_type
    
    def get_amount(self):
        return self.__amount
    


class Strategy:
    
    
    def __init__(self):
        self.create_strategy()
    
    
    def receive_action(self, stock_market, wallet):
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
        
        