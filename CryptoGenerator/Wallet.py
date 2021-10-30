# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 17:28:03 2021

@author: Andre
"""

class Wallet(object): 


    def __init__(self, euros, bitcoins):
        self.__euros = euros
        self.__bitcoins = bitcoins
        
    
    def buyBitcoin(self, euros, bitcoins):
        print("buying bitcoins")
        self.__euros -= euros
        self.__bitcoins += bitcoins
        
    def sellBitcoin(self, bitcoins, euros):
        print("selling bitcoins")
        self.__euros += euros
        self.__bitcoins -= bitcoins
        
    def get_euros(self):
        return self.__euros
    
    def get_bitcoins(self):
        return self.__bitcoins