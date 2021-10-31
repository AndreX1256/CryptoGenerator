# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 17:28:03 2021

@author: Andre
"""


class Wallet: 


    def __init__(self, euros, bitcoins):
        self.__euros = euros
        self.__bitcoins = bitcoins

    
    def insert_euros(self, euros):
        print("Wallet: insert " + str(euros) + "€")
        self.__euros += euros
        
        
    def remove_euros(self, euros):
        print("Wallet: remove " + str(euros) + "€")
        self.__euros -= euros
        
    
    def insert_bitcoins(self, bitcoins):
        print("Wallet: insert " + str(bitcoins) + "BTC")
        self.__bitcoins += bitcoins


    def remove_bitcoins(self, bitcoins):
        print("Wallet: remove " + str(bitcoins) + "BTC")
        self.__bitcoins -= bitcoins        
        
        
    def euros(self):
        #print("Wallet: " + str(self.__euros) + "€")
        return self.__euros
    
    
    def bitcoins(self):
        #print("Wallet: " + str(self.__bitcoins) + "BTC")
        return self.__bitcoins
        
    
    def show(self):
        print ( "Wallet is: euros: " + str(self.__euros) + "€, bitcoins: " + str(self.__bitcoins) + " BTC (" + str(round(self.__bitcoins * 100000000))  + " Satoshis)")