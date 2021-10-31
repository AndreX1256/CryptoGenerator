# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 16:44:50 2021

@author: Andre
"""

from CryptoGenerator.Trader import Trader
from CryptoGenerator.TaxAuthority import TaxAuthority
from CryptoGenerator.StockMarket import StockMarket

class CryptoGenerator: 


    def __init__(self, start_money):
        self.__trader = Trader(start_money)
        self.__tax_authority = TaxAuthority(taxes_percentage = 25, total_taxes_paid_by_trader = 0)
        self.__stock_market = StockMarket(bitcoin_price = 35000, trading_fees = 1)
        
    
    def run(self):
        print("Running Crypto Generator!")
        self.__trader.do_action(self.__stock_market)
        self.__tax_authority.tax_declaration(self.__trader)
        self.__trader.do_action(self.__stock_market)
        self.__tax_authority.tax_declaration(self.__trader)
        self.__trader.show()
        


