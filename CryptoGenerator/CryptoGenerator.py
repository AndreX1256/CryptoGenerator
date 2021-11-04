# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 16:44:50 2021

@author: Andre
"""

from CryptoGenerator.Trader import Trader
from CryptoGenerator.TaxAuthority import TaxAuthority
from CryptoGenerator.StockMarket import StockMarket
from CryptoGenerator.StockMarket import MarketUpdater


class CryptoGenerator: 


    def __init__(self, start_money):
        self.__trader = Trader(start_money)
        self.__tax_authority = TaxAuthority(taxes_percentage = 45)
        self.__stock_market = StockMarket(bitcoin_price = 35000, trading_fees = 1)
    
    
    def buy_sell_taxes(self):
        self.__trader.buy(self.__stock_market, 1500)
        self.__trader.show()
        self.__stock_market.update(36000)
        self.__trader.sell(self.__stock_market, 0.1004)
        self.__trader.show()
        self.__tax_authority.calculate_taxes_to_pay(self.__trader.tax_declaration())
        
    def calculate_current_outcome(self, market, trader, tax_authority):
        current_euros = trader.wallet().euros()
        current_bitcoins = trader.wallet().bitcoins()
        current_bitcoin_value = current_bitcoins * market.bitcoin_price()
        current_taxes_to_pay = tax_authority.calculate_taxes_to_pay(trader.tax_declaration())
        current_outcome = current_euros + current_bitcoin_value - current_taxes_to_pay
        print ("CryptoGenerator: current outcome is " + str(current_outcome))
        return current_outcome
        
    
    def run(self):
        print("Running Crypto Generator!")
        keep_running = True
        max_steps = 10000
        current_step = 0
        market_updater = MarketUpdater(-100, 100)
        while not self.__trader.is_broke() and current_step < max_steps and keep_running:
            print("--- next step (" + str(current_step) + ")---")
            self.__trader.do_action(self.__stock_market)
            self.__tax_authority.calculate_taxes_to_pay(self.__trader.tax_declaration())
            self.__trader.show()
            self.calculate_current_outcome(self.__stock_market, self.__trader, self.__tax_authority)
            
            market_updater.update_market(self.__stock_market)
            current_step += 1
        


