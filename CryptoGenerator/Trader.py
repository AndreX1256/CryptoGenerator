# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:41:03 2021

@author: Andre
"""


from CryptoGenerator.Wallet import Wallet
from CryptoGenerator.Strategy import Strategy


class Trader:
    
    
    def __init__(self, start_money):
        self.__wallet = Wallet(start_money,0)
        self.__strategy = Strategy()
        
        
    def do_action(self, stock_market):
        action = self.__strategy.receive_action(stock_market, self.__wallet)
        if (action > 0):
            self.buy(stock_market, action)
        elif (action < 0):
            self.sell(stock_market, self.__wallet.get_bitcoins())
        self.__strategy.update(self.__wallet)
        
        
    def buy(self, stock_market, euros):
        if (euros > self.__wallet.get_euros()): euros = self.__wallet.get_euros()
        if (euros <= 0): return False
        return stock_market.buyBitcoins(self.__wallet, euros)
        
    
    def sell(self, stock_market, bitcoins):
        if (bitcoins > self.__wallet.get_bitcoins()): bitcoins = self.__wallet.get_bitcoins()
        if (bitcoins <= 0): return False
        return stock_market.sellBitcoins(self.__wallet, bitcoins)
    
    
    def pay_taxes(self, euros):
        print("Trader: paying taxes: " + str(euros) + "€")
        self.__wallet.remove_euros(euros)
        
        
    def return_taxes(self, euros):
        print("Trader: return taxes: " + str(euros) + "€")
        self.__wallet.insert_euros(euros)
        
        
    def get_financial_profit(self):
        return self.__wallet.get_financial_profit()


    def show(self):
        print("Trader: financial profit is: " + str(self.get_financial_profit()) + "€")
        self.__wallet.show()