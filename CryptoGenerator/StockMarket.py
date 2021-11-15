# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:20:15 2021

@author: Andre
"""


from CryptoGenerator.Wallet import Wallet

from CryptoGenerator.VerboseLevel import VerboseLevel

import copy
from enum import Enum
import random
import numpy as np


class TradeType(Enum):
    PURCHASE = 1
    SALE = 2
    DENIED = 3


class Trade:
    
    
    def __init__(self, trade_type, bitcoins, bitcoin_price):
        self.__trade_type = trade_type
        self.__bitcoins = bitcoins
        self.__bitcoin_price = bitcoin_price
        
    
    def bitcoins(self):
        return self.__bitcoins
    
    def set_bitcoins(self, bitcoins):
        self.__bitcoins = bitcoins
    
        
    def bitcoin_price(self):
        return self.__bitcoin_price
    
    
    def trade_type(self):
        return self.__trade_type
    
    
    def print_trade(self):
        if (self.__trade_type is TradeType.PURCHASE): print ( "Trade Purchase: bought " + str(self.__bitcoins) + "BTC for " + str(self.__bitcoin_price) + "€ per BTC")
        if (self.__trade_type is TradeType.SALE): print ( "Trade Sale: sold " + str(self.__bitcoins) + "BTC for " + str(self.__bitcoin_price) + "€ per BTC")
        if (self.__trade_type is TradeType.DENIED): print ( "Trade: denied")


class MarketUpdater:
    
    def __init__(self, min_range, max_range):
        self.__do_random_relative = False
        self.__do_random_absolute = False
        self.__do_function_curve = True
        self.__do_real_market = False
        self.__range_min = min_range
        self.__range_max = max_range
        self.create_sin_function_curve()
    
    def update_absolute(self, market, value):
        market.update(value)
        
    def update_relative(self, market, value):
        old_price = market.bitcoin_price()
        market.update(old_price + value)
        
    def create_sin_function_curve(self):
        self.__step = 0
        self.__total_steps = 80
        self.__relative_prive_values = np.sin(np.linspace(0.0, 360.0, num=self.__total_steps+1) * np.pi / 180.0 ) * ((self.__range_max - self.__range_min) / 2.0) + ((self.__range_min + self.__range_max) / 2.0)
        self.__relative_prive_values = self.__relative_prive_values[1:]
        #print(self.__relative_prive_values)


    def update_market(self, market):
        if self.__do_random_relative:
            self.update_relative(market, random.randint(self.__range_min, self.__range_max))
        if self.__do_random_absolute:
            self.update_absolute(market, random.randint(self.__range_min, self.__range_max))
        if self.__do_function_curve:
            self.update_absolute(market, self.__relative_prive_values[self.__step])
            self.__step += 1
            self.__step %= self.__total_steps
        
    

class StockMarket: 


    def __init__(self, bitcoin_price, trading_fees, verbose):
        self.__bitcoin_price = bitcoin_price
        self.__trading_fees = trading_fees
        self.__verbose = verbose
        
        
    def update(self, bitcoin_price):
        self.__bitcoin_price = bitcoin_price
        if self.__verbose <= VerboseLevel.DEBUG: print("StockMarket: new bitcoin price is " + str(bitcoin_price)) 
    
    
    def buy_bitcoins(self, wallet, euros):
        if (euros <= self.__trading_fees): return Trade(TradeType.DENIED, 0, 0)
        if (euros > wallet.euros()): return Trade(TradeType.DENIED, 0, 0)
        if self.__verbose <= VerboseLevel.DEBUG: print("StockMarket: buying bitcoins")
        bitcoins = (euros - self.__trading_fees) / self.__bitcoin_price
        wallet.remove_euros(euros)
        wallet.insert_bitcoins(bitcoins)
        return Trade(TradeType.PURCHASE, bitcoins, copy.copy(self.__bitcoin_price))
        
        
    def sell_bitcoins(self, wallet, bitcoins):
        if (bitcoins > wallet.bitcoins()): return Trade(TradeType.DENIED, 0, 0)
        if self.__verbose <= VerboseLevel.DEBUG: print("StockMarket: selling bitcoins")
        euros = (bitcoins * self.__bitcoin_price) - self.__trading_fees
        wallet.remove_bitcoins(bitcoins)
        wallet.insert_euros(euros)
        return Trade(TradeType.SALE, bitcoins, copy.copy(self.__bitcoin_price))
        
        
    def bitcoin_price(self):
        return self.__bitcoin_price
    
    
    def print_stock_market(self):
        print ( "StockMarket: bitcoin price is " + str(self.__bitcoin_price) + "€")