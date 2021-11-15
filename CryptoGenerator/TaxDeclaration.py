# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 21:35:26 2021

@author: Andre
"""


from CryptoGenerator.StockMarket import TradeType

from CryptoGenerator.VerboseLevel import VerboseLevel

from enum import Enum
import numpy as np


class TaxType(Enum):
    FIFO = 1
    LIFO = 2
    

class TaxDeclaration:
    
    
    def __init__(self, tax_type, verbose):
        self.__tax_type = tax_type
        self.__purchases = []
        self.__profit_to_declare = 0
        self.__verbose = verbose
        

    def add_trade(self, trade):
        if trade.trade_type() is TradeType.PURCHASE:
            self.__purchases.append(trade)
        if trade.trade_type() is TradeType.SALE:
            self.update_profit(trade)
                
            
    def purchases(self):
        return self.__purchases


    def update_profit(self, sale):
        if (sale.trade_type() is not TradeType.SALE): return
        current_profit = sale.bitcoins() * sale.bitcoin_price()

        while sale.bitcoins() > np.finfo(float).eps:

            if self.__tax_type is TaxType.FIFO: purchase = self.__purchases[0]
            if self.__tax_type is TaxType.LIFO: purchase = self.__purchases[len(self.__purchases)-1]
            
            if purchase.bitcoins() > sale.bitcoins():
                current_profit -= sale.bitcoins() * purchase.bitcoin_price()
                purchase.set_bitcoins(purchase.bitcoins() - sale.bitcoins())
                sale.set_bitcoins(0)
                
            if purchase.bitcoins() <= sale.bitcoins():
                current_profit -= purchase.bitcoins() * purchase.bitcoin_price()
                #sale.set_bitcoins(0)
                sale.set_bitcoins(sale.bitcoins() - purchase.bitcoins())
                #purchase.set_bitcoins(0)
                if len(self.__purchases) <= 1: self.__purchases = []
                elif self.__tax_type is TaxType.FIFO: self.__purchases = self.__purchases[1:]
                elif self.__tax_type is TaxType.LIFO: self.__purchases = self.__purchases[:len(self.__purchases)-2]
        
        self.__profit_to_declare += current_profit
        if self.__verbose <= VerboseLevel.DEBUG: print("TaxDeclaration: profit to declare: " + str(self.__profit_to_declare) + "€")
            
            

    def clear_profit(self):
        self.__profit_to_declare = 0
        
        
    def profit_to_declare(self):
        return self.__profit_to_declare