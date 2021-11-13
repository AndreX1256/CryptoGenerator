# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 17:12:59 2021

@author: Andre
"""

from abc import ABC, abstractmethod


class Strategy(ABC):
    
    @abstractmethod
    def receive_action(self, input_data):
        pass
        
    @abstractmethod
    def update(self, wallet):
        pass
    
    @property
    def action_list(self):
        return self.__action_list
    
    @action_list.setter
    def action_list(self, value):
        self.__action_list = value