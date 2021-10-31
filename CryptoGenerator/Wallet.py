# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 17:28:03 2021

@author: Andre
"""


class Wallet: 


    def __init__(self, euros, bitcoins):
        self.__euros = euros
        self.__bitcoins = bitcoins
        self.__financial_profit = 0
        self.__invested_money = 0
        
    
    def buyBitcoins(self, bitcoins, euros):
        if (euros > self.__euros): return False
        print("Wallet: buying bitcoins: removing " + str(euros) + "€, adding " + str(bitcoins) + "BTC")
        self.__euros -= euros
        self.__bitcoins += bitcoins
        
        return True
        
    
    def sellBitcoins(self, bitcoins, euros):
        if (bitcoins > self.__bitcoins): return False
        print("Wallet: selling bitcoins: removing " + str(bitcoins) + "BTC, adding " + str(euros) + "€")
        self.__euros += euros
        self.__bitcoins -= bitcoins
        self.__invested_money -= euros
        self.__financial_profit = self.__invested_money
        return True
    
    
    def insert_euros(self, euros):
        print("Wallet: insert " + str(euros) + "€")
        self.__euros -= euros
        
        
    def remove_euros(self, euros):
        print("Wallet: remove " + str(euros) + "€")
        self.__euros -= euros
        
        
    def get_euros(self):
        return self.__euros
    
    
    def get_bitcoins(self):
        return self.__bitcoins
    
    
    def get_financial_profit(self):
        return self.__financial_profit
    
    
    def show(self):
        print ( "Wallet is: euros: " + str(self.__euros) + ", bitcoins: " + str(self.__bitcoins))