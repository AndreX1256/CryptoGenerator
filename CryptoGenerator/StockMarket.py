# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:20:15 2021

@author: Andre
"""


from CryptoGenerator.Wallet import Wallet


class StockMarket: 


    def __init__(self, bitcoin_price, trading_fees):
        self.__bitcoin_price = bitcoin_price
        self.__trading_fees = trading_fees
        
        
    def update(self, bitcoin_price):
        self.__bitcoin_price = bitcoin_price
    
    
    def buyBitcoins(self, wallet, euros):
        print("StockMarket: buying bitcoins")
        if (euros <= self.__trading_fees): return False
        bitcoins = (euros - self.__trading_fees) / self.__bitcoin_price
        return wallet.buyBitcoins(bitcoins, euros)
        

        
    def sellBitcoins(self, wallet, bitcoins):
        print("selling bitcoins")
        euros = (bitcoins * self.__bitcoin_price) - self.__trading_fees
        return wallet.sellBitcoins(bitcoins, euros)
        
        
    def get_bitcoin_price_euro(self):
        return self.__bitcoin_price
    
    
    def print_stock_market(self):
        print ( "StockMarket: bitcoin price is " + str(self.__bitcoin_price) + "€")