# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:28:51 2021

@author: Andre
"""


from CryptoGenerator.StockMarket import StockMarket
from CryptoGenerator.Wallet import Wallet
import random
from enum import Enum

class Strategy:
    
    
    def __init__(self):
        pass
    
    
    def receive_action(self, stock_market, wallet):
        return random.randint(-100, 100)
    
    
    def update(self, wallet):
        pass
        