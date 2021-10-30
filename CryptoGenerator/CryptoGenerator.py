# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 16:44:50 2021

@author: Andre
"""

from CryptoGenerator.Wallet import Wallet

class CryptoGenerator: 


    def __init__(self):
        self.__wallet = Wallet(0,0)
    
    def run(self):
        print("running Crypto Generator")

