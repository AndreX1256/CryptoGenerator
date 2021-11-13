# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 21:41:19 2021

@author: Andre
"""

import matplotlib.pyplot as plt
import numpy as np

from CryptoGenerator.Action import ActionType


class History:
    
    def __init__(self):
        self.__date = []
        self.__bitcoin_price = []
        self.__action = []
        self.__outcome = []
        
    def update(self, date, bitcoin_price, action, outcome):
        self.__date.append(date)
        self.__bitcoin_price.append(bitcoin_price)
        self.__action.append(action)
        self.__outcome.append(outcome)
        
    def get_bitcoin_price(self):
        return self.__bitcoin_price

        
    def visualize(self):        
        x_buy = []
        y_buy = []
        x_sell = []
        y_sell = []
        
        for i in range(len(self.__date)):
            if self.__action[i].get_action_type() is ActionType.BUY or self.__action[i].get_action_type() is ActionType.BUYALL:
                x_buy.append(i)
                y_buy.append(self.__bitcoin_price[i])
            if self.__action[i].get_action_type() is ActionType.SELL or self.__action[i].get_action_type() is ActionType.SELLALL:
                x_sell.append(i)
                y_sell.append(self.__bitcoin_price[i])
                
        s_buy = np.ones(len(x_buy)) * 50
        s_sell = np.ones(len(x_sell)) * 50
        
        plt.subplot(2, 1, 1)
        plt.scatter(x_buy, y_buy, s_buy, c="g", alpha=0.5, marker="^",  label="buy")
        plt.scatter(x_sell, y_sell, s_sell, c="r", alpha=0.5, marker="v",  label="sell")

        plt.plot(self.__bitcoin_price)
        plt.xlabel('date')
        plt.ylabel('bitcoin price')
        plt.legend(loc='upper left')
        
        plt.subplot(2, 1, 2)
        plt.plot(self.__outcome)
        plt.xlabel('date')
        plt.ylabel('outcome')
        
        plt.show()
        