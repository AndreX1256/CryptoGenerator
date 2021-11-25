# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 16:44:50 2021

@author: Andre
"""

from CryptoGenerator.Trader import Trader
from CryptoGenerator.TaxAuthority import TaxAuthority
from CryptoGenerator.StockMarket import StockMarket
from CryptoGenerator.StockMarket import MarketUpdater
from CryptoGenerator.History import History
from CryptoGenerator.InputData import InputData

#from CryptoGenerator.StrategyRandom import StrategyRandom
#from CryptoGenerator.StrategyScripted import StrategyScripted
from CryptoGenerator.StategyDeepQLearning import StategyDeepQLearning

from CryptoGenerator.VerboseLevel import VerboseLevel

import time
import matplotlib.pyplot as plt


class CryptoGenerator: 


    def __init__(self, start_money, verbose):
        self.__start_money = start_money
        self.__verbose = verbose
        self.__strategy = StategyDeepQLearning()
        # ToDo: put this history in extra class (training history)
        self.__reward_per_episode = []
       

    def calculate_current_outcome(self, market, trader, tax_authority, start_money):
        current_euros = trader.wallet().euros()
        current_bitcoins = trader.wallet().bitcoins()
        current_bitcoin_value = current_bitcoins * market.bitcoin_price()
        current_taxes_to_pay = tax_authority.calculate_taxes_to_pay(trader.tax_declaration())
        current_outcome = current_euros + current_bitcoin_value - current_taxes_to_pay - start_money
        if self.__verbose <= VerboseLevel.DEBUG: print ("CryptoGenerator: current outcome is " + str(current_outcome) + "€")
        return current_outcome
        
    
    def run(self):
        print("--- Running Crypto Generator ---")
        keep_running = True
        max_steps = 300
        max_episodes = 3

        for current_episode in range(max_episodes):
            time_start_episode = time.time()    
    
            if self.__verbose <= VerboseLevel.INFO: print("--- next episode (" + str(current_episode) + ")---")
            current_step = 0
            
            trader = Trader(self.__start_money, self.__strategy, self.__verbose)
            tax_authority = TaxAuthority(taxes_percentage = 45, verbose = self.__verbose)
            stock_market = StockMarket(bitcoin_price = 35000, trading_fees = 1, verbose = self.__verbose)
            market_updater = MarketUpdater(34000, 36000)
            history = History()
            
            while not trader.is_broke() and current_step < max_steps and keep_running:
                if self.__verbose <= VerboseLevel.DEBUG: print("--- next step (" + str(current_step) + ")---")
                
                # do action
                state = InputData(history, trader.wallet(), stock_market.bitcoin_price())
                action = trader.do_action(stock_market, state)
                tax_authority.calculate_taxes_to_pay(trader.tax_declaration())
                
                # evaluate
                if self.__verbose <= VerboseLevel.DEBUG: trader.show()
                outcome = self.calculate_current_outcome(stock_market, trader, tax_authority, self.__start_money)
                history.update(current_step+1, stock_market.bitcoin_price(), action, outcome)
                
                # update
                market_updater.update_market(stock_market)
                current_step += 1
                
                reward = self.calculate_current_outcome(stock_market, trader, tax_authority, self.__start_money) / 100
                next_state = InputData(history, trader.wallet(), stock_market.bitcoin_price())
                self.__strategy = trader.strategy()
                self.__strategy.update(state.processed_data(), action, reward, next_state.processed_data())
            
            # train and update network
            time_start_train = time.time()  
            self.__strategy.train()
            time_end_train = time.time()
            self.__strategy.epsilon(1 - (current_episode / max_episodes))
            self.__strategy.update_target_weights()
            
            # update training history
            self.__reward_per_episode.append(reward)
            
            time_end_episode = time.time()
            if self.__verbose <= VerboseLevel.INFO: print ("execution time for training is: " + str((time_end_train - time_start_train) * 1000) + " ms")
            if self.__verbose <= VerboseLevel.INFO: print ("execution time for episode is: " + str((time_end_episode - time_start_episode) * 1000) + " ms")
            
        
        print("--- End Crypto Generator ---")
        
        history.visualize()
        
        
        plt.subplot(3, 1, 3)
        plt.plot(self.__reward_per_episode)
        plt.xlabel('episode')
        plt.ylabel('reward')
        plt.show()
        


