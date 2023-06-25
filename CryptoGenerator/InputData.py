# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 18:53:12 2021

@author: Andre
"""


class InputData:
    
#    def __init__(self, history, wallet, bitcoin_price, current_buy_in_price, current_buy_in_amount, bitcoin_trend):
#        self.__history = history
#        self.__bitcoin_price = bitcoin_price
#        self.__wallet = wallet
#        self.__current_buy_in_price = current_buy_in_price
#        self.__current_buy_in_amount = current_buy_in_amount
#        self.__bitcoin_trend = bitcoin_trend
        
    def __init__(self, wallet, bitcoin_price, current_buy_in_price, bitcoin_trend):
        self.__bitcoin_price = bitcoin_price
        self.__wallet = wallet
        self.__current_buy_in_price = current_buy_in_price
        self.__bitcoin_trend = bitcoin_trend
    
    def get_bitcoin_price(self):
        return self.__bitcoin_price
    
    
    def get_wallet(self):
        return self.__wallet
    
        
    def processed_data(self):
        data = []
        
        start_money = 1000
        
        # market_bitcoin_trend = 0
        # if (len(h) == 1):
        #     if (self.__bitcoin_price - h[0]) > 0:
        #         market_bitcoin_trend = 1
        #     if (self.__bitcoin_price - h[0]) < 0: 
        #         market_bitcoin_trend = -1
        #    market_bitcoin_normalized = (self.__bitcoin_price - h[0]) / 100
        #else:
        #    market_bitcoin_normalized = 0
            
        market_bitcoin_normalized = (self.__bitcoin_price - 35000) / (36000 - 35000)
        wallet_bitcoin = self.__wallet.bitcoins() * 35000
        wallet_euro = self.__wallet.euros()
        current_buy_in_price_normalized = (self.__current_buy_in_price - 35000) / (36000 - 35000)
        #current_buy_in_amount_normalized = self.__current_buy_in_amount * 35000 / start_money

        
        #wallet_bitcoin_normalized = (wallet_bitcoin / (wallet_bitcoin + wallet_euro)) * 2 - 1

        wallet_bitcoin_normalized = wallet_bitcoin / start_money
        #wallet_euro_normalized = (wallet_euro / (wallet_bitcoin + wallet_euro)) * 2 - 1
        wallet_euro_normalized = wallet_euro / start_money
        #data.append(self.__bitcoin_price - self.__history.get_bitcoin_price()[-1])
        
        wallet_norm = wallet_euro_normalized - wallet_bitcoin_normalized
        
        data.append(market_bitcoin_normalized)
        data.append(self.__bitcoin_trend)
        data.append(wallet_bitcoin_normalized)
        data.append(wallet_euro_normalized)
        #data.append(wallet_norm)
        #data.append(current_buy_in_price_normalized)
        #data.append(current_buy_in_amount_normalized)
        
        return data