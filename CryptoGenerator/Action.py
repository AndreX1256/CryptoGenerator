# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 19:02:07 2021

@author: Andre
"""


from enum import Enum


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
    