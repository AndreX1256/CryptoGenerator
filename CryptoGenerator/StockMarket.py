# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:20:15 2021

@author: Andre
"""


from CryptoGenerator.Wallet import Wallet
import copy
from enum import Enum


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


class StockMarket: 


    def __init__(self, bitcoin_price, trading_fees):
        self.__bitcoin_price = bitcoin_price
        self.__trading_fees = trading_fees
        
        
    def update(self, bitcoin_price):
        self.__bitcoin_price = bitcoin_price
    
    
    def buy_bitcoins(self, wallet, euros):
        if (euros <= self.__trading_fees): return Trade(TradeType.DENIED, 0, 0)
        if (euros > wallet.euros()): return Trade(TradeType.DENIED, 0, 0)
        print("StockMarket: buying bitcoins")
        bitcoins = (euros - self.__trading_fees) / self.__bitcoin_price
        wallet.remove_euros(euros)
        wallet.insert_bitcoins(bitcoins)
        return Trade(TradeType.PURCHASE, bitcoins, copy.copy(self.__bitcoin_price))
        
        
    def sell_bitcoins(self, wallet, bitcoins):
        if (bitcoins > wallet.bitcoins()): return Trade(TradeType.DENIED, 0, 0)
        print("StockMarket: selling bitcoins")
        euros = (bitcoins * self.__bitcoin_price) - self.__trading_fees
        wallet.remove_bitcoins(bitcoins)
        wallet.insert_euros(euros)
        return Trade(TradeType.SALE, bitcoins, copy.copy(self.__bitcoin_price))
        
        
    def bitcoin_price(self):
        return self.__bitcoin_price
    
    
    def print_stock_market(self):
        print ( "StockMarket: bitcoin price is " + str(self.__bitcoin_price) + "€")