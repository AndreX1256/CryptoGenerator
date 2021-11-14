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

from CryptoGenerator.StrategyRandom import StrategyRandom
from CryptoGenerator.StrategyScripted import StrategyScripted
from CryptoGenerator.StategyDeepQLearning import StategyDeepQLearning

class CryptoGenerator: 


    def __init__(self, start_money):
        self.__start_money = start_money
        self.__strategy = StategyDeepQLearning()
       

    def calculate_current_outcome(self, market, trader, tax_authority, start_money):
        current_euros = trader.wallet().euros()
        current_bitcoins = trader.wallet().bitcoins()
        current_bitcoin_value = current_bitcoins * market.bitcoin_price()
        current_taxes_to_pay = tax_authority.calculate_taxes_to_pay(trader.tax_declaration())
        current_outcome = current_euros + current_bitcoin_value - current_taxes_to_pay - start_money
        print ("CryptoGenerator: current outcome is " + str(current_outcome) + "€")
        return current_outcome
        
    
    def run(self):
        print("Running Crypto Generator!")
        keep_running = True
        max_steps = 300
        max_episodes = 100

        for current_episode in range(max_episodes):
            print("--- next episode (" + str(current_episode) + ")---")
            current_step = 0
            
            trader = Trader(self.__start_money, self.__strategy)
            tax_authority = TaxAuthority(taxes_percentage = 45)
            stock_market = StockMarket(bitcoin_price = 35000, trading_fees = 1)
            market_updater = MarketUpdater(34000, 36000)
            history = History()
            
            while not trader.is_broke() and current_step < max_steps and keep_running:
                print("--- next step (" + str(current_step) + ")---")
                
                # do action
                state = InputData(history, trader.wallet(), stock_market.bitcoin_price())
                action = trader.do_action(stock_market, state)
                tax_authority.calculate_taxes_to_pay(trader.tax_declaration())
                
                # evaluate
                trader.show()
                outcome = self.calculate_current_outcome(stock_market, trader, tax_authority, self.__start_money)
                history.update(current_step+1, stock_market.bitcoin_price(), action, outcome)
                
                # update
                market_updater.update_market(stock_market)
                current_step += 1
                
                reward = self.calculate_current_outcome(stock_market, trader, tax_authority, self.__start_money)
                next_state = InputData(history, trader.wallet(), stock_market.bitcoin_price())
                self.__strategy = trader.strategy()
                self.__strategy.update(state.processed_data(), action, reward, next_state.processed_data())
                
            self.__strategy.train()
            
        history.visualize()
        


