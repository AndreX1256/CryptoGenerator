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
from CryptoGenerator.Action import ActionType

#from CryptoGenerator.StrategyRandom import StrategyRandom
#from CryptoGenerator.StrategyScripted import StrategyScripted
from CryptoGenerator.StategyDeepQLearning import StategyDeepQLearning

from CryptoGenerator.VerboseLevel import VerboseLevel

import time
import matplotlib.pyplot as plt
import copy

class CryptoGenerator: 


    def __init__(self, start_money, load_existing_network, verbose):
        self.__start_money = start_money
        self.__verbose = verbose
        
        self.__strategy = StategyDeepQLearning(verbose)
        if load_existing_network is not None: self.__strategy.load_network(path='data/trained_networks/', name=load_existing_network)
        
        # ToDo: put this history in extra class (training history)
        self.__reward_per_episode = []
       

    def calculate_current_outcome(self, market, trader, tax_authority, start_money):
        current_euros = trader.wallet().euros()
        current_bitcoins = trader.wallet().bitcoins()
        #current_bitcoin_value = 0
        #if current_bitcoins > 0:
        current_bitcoin_value = current_bitcoins * market.bitcoin_price()
        current_taxes_to_pay = 0#tax_authority.calculate_taxes_to_pay(trader.tax_declaration())
        current_outcome = current_euros + current_bitcoin_value - current_taxes_to_pay - start_money
        if self.__verbose <= VerboseLevel.DEBUG: print ("CryptoGenerator: current outcome is " + str(current_outcome) + "€")
        return current_outcome
        
    
    def run(self):
        print("--- Running Crypto Generator ---")
        keep_running = True
        max_steps = 500
        max_episodes = 5000

        for current_episode in range(max_episodes):
            time_start_episode = time.time()    
    
            if self.__verbose <= VerboseLevel.INFO: print("--- next episode (" + str(current_episode) + ")---")
            current_step = 0
            
            total_reward = 0
            last_outcome = 0
            last_bitcoin_price = 0
            
            trader = Trader(self.__start_money, self.__strategy, self.__verbose)
            tax_authority = TaxAuthority(taxes_percentage = 45, verbose = self.__verbose)
            stock_market = StockMarket(bitcoin_price = 35000, trading_fees = 0, verbose = self.__verbose)
            market_updater = MarketUpdater(34000, 36000)
            history = History()
            
            current_buy_in_price = 0
            
            while not trader.is_broke() and current_step < max_steps and keep_running:
                if self.__verbose <= VerboseLevel.DEBUG: print("--- next step (" + str(current_step) + ")---")
                
                market_bitcoin_trend = 0
                if stock_market.bitcoin_price() > last_bitcoin_price:
                    market_bitcoin_trend = 1
                if stock_market.bitcoin_price() < last_bitcoin_price:
                    market_bitcoin_trend = -1
                    
                # do action
                state = InputData(copy.copy(history), trader.wallet(), stock_market.bitcoin_price(), current_buy_in_price, market_bitcoin_trend)
                action = trader.do_action(stock_market, state)
                tax_authority.calculate_taxes_to_pay(trader.tax_declaration())
                
          
                
                # evaluate
                if self.__verbose <= VerboseLevel.DEBUG: trader.show()
                outcome = self.calculate_current_outcome(stock_market, trader, tax_authority, self.__start_money)
                history.update(current_step+1, stock_market.bitcoin_price(), action, outcome)
                
                # update
                last_bitcoin_price = stock_market.bitcoin_price()
                market_updater.update_market(stock_market)
                
                market_bitcoin_trend = 0
                if stock_market.bitcoin_price() > last_bitcoin_price:
                    market_bitcoin_trend = 1
                if stock_market.bitcoin_price() < last_bitcoin_price:
                    market_bitcoin_trend = -1
                
                # reward
                
                reward = 0 #self.calculate_current_outcome(stock_market, trader, tax_authority, self.__start_money) - outcome
                
                if action.get_action_type() is ActionType.SELLALL:
                    reward = stock_market.bitcoin_price() - current_buy_in_price
                 #   current_outcome = outcome - last_outcome
                  #  if outcome > last_outcome: reward = 1
                   # if outcome < last_outcome: reward = -1
                    #last_outcome = outcome
                #if reward > 0: reward = 1
                #if reward <= 0: reward = -1
                    #last_outcome = outcome
                #if action.get_action_type() is ActionType.BUYALL:
                    #last_outcome = outcome
                #reward = (outcome / last_outcome)
                
                
                #reward = outcome
                #start_budget = trader.wallet().euros() - current_outcome
                
                    #if reward > 0: reward = 1
                    #if reward < 0: reward = -1
                    
                total_reward += reward
                
                if action.get_action_type() is ActionType.SELLALL:
                    current_buy_in_price = 0
                if action.get_action_type() is ActionType.BUYALL:
                    current_buy_in_price = stock_market.bitcoin_price() 
                
                # get next state
                next_state = InputData(copy.copy(history), trader.wallet(), stock_market.bitcoin_price(), current_buy_in_price, market_bitcoin_trend)
                self.__strategy = trader.strategy()
                
                # feed experience replay
                if current_step > 0: self.__strategy.update(state.processed_data(), action, reward, next_state.processed_data())
                
                current_step += 1
            
            # train and update network
            time_start_train = time.time()  
            self.__strategy.train()
            time_end_train = time.time()
            self.__strategy.epsilon(1 - (current_episode / max_episodes))
            #self.__strategy.epsilon(1 - ((current_episode % (max_episodes/3)) / (max_episodes/3)))
            self.__strategy.update_target_weights()
            
            # update training history
            self.__reward_per_episode.append(total_reward)
            
            time_end_episode = time.time()
            if self.__verbose <= VerboseLevel.INFO: print ("execution time for training is: " + str((time_end_train - time_start_train) * 1000) + " ms")
            if self.__verbose <= VerboseLevel.INFO: print ("execution time for episode is: " + str((time_end_episode - time_start_episode) * 1000) + " ms")
            
        
        print("--- End Crypto Generator ---")
        
        self.__strategy.save_network(path='data/trained_networks/')
        history.visualize()
        
        
        plt.subplot(3, 1, 3)
        plt.plot(self.__reward_per_episode)
        plt.xlabel('episode')
        plt.ylabel('reward')
        plt.show()
        


