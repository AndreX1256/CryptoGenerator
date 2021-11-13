# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 18:53:12 2021

@author: Andre
"""


class InputData:
    
    def __init__(self, history, wallet, bitcoin_price):
        self.__history = history
        self.__bitcoin_price = bitcoin_price
        self.__wallet = wallet
        
        
    def get_bitcoin_price(self):
        return self.__bitcoin_price
    
    
    def get_wallet(self):
        return self.__wallet
    
        
    def processed_data(self):
        data = []
        
        #data.append(self.__bitcoin_price - self.__history.get_bitcoin_price()[-1])
        data.append(self.__bitcoin_price)
        data.append(self.__wallet.bitcoins())
        data.append(self.__wallet.euros())
        
        return data