# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:41:03 2021

@author: Andre
"""


from CryptoGenerator.Wallet import Wallet

from CryptoGenerator.Action import ActionType
from CryptoGenerator.Action import Action

from CryptoGenerator.StockMarket import TradeType
from CryptoGenerator.TaxDeclaration import TaxDeclaration
from CryptoGenerator.TaxDeclaration import TaxType

from CryptoGenerator.VerboseLevel import VerboseLevel


class Trader:
    
    
    def __init__(self, start_money, strategy, verbose):
        self.__wallet = Wallet(start_money, 0, verbose)
        self.__verbose = verbose
        self.__strategy = strategy
        self.__tax_declaration = TaxDeclaration(TaxType.FIFO, verbose)
        self.__buy_once = False
        
        
    def do_action(self, stock_market, input_data):
        action = self.__strategy.receive_action(input_data)
        
        if self.__buy_once:
            self.__buy_once = False
            action = Action(ActionType.BUYALL)
        
        if action.get_action_type() is ActionType.BUYALL and self.__wallet.euros() <= 0: action = Action(ActionType.HOLD)
        if action.get_action_type() is ActionType.SELLALL and self.__wallet.bitcoins() <= 0: action = Action(ActionType.HOLD)



        if action.get_action_type() is ActionType.BUY:
            if self.__verbose <= VerboseLevel.DEBUG: print("Trader choose to buy for " + str(action.get_amount()) + "€")
            self.buy(stock_market, action.get_amount())
        if action.get_action_type() is ActionType.BUYALL:
            if self.__verbose <= VerboseLevel.DEBUG: print("Trader choose to buy all")
            self.buy(stock_market, self.__wallet.euros())
        if action.get_action_type() is ActionType.SELL:
            if self.__verbose <= VerboseLevel.DEBUG: print("Trader choose to sell for " + str(action.get_amount()) + "€")
            self.sell(stock_market, action.get_amount() / stock_market.bitcoin_price())
        if action.get_action_type() is ActionType.SELLALL:
            if self.__verbose <= VerboseLevel.DEBUG: print("Trader choose to sell all")
            self.sell(stock_market, self.__wallet.bitcoins())
        if action.get_action_type() is ActionType.HOLD:
            if self.__verbose <= VerboseLevel.DEBUG: print("Trader choose to hold")
            self.hold()

        return action
        
        
    def buy(self, stock_market, euros):
        #if (self.__wallet.euros() <= 0): self.__wallet.remove_euros(10)
        if (euros > self.__wallet.euros()): euros = self.__wallet.euros()
        if (euros <= 0): return
        purchase = stock_market.buy_bitcoins(self.__wallet, euros)
        if self.__verbose <= VerboseLevel.DEBUG: purchase.print_trade()
        if purchase.trade_type() is not TradeType.DENIED:
            self.__tax_declaration.add_trade(purchase)
           
        
    
    def sell(self, stock_market, bitcoins):
        #if (self.__wallet.bitcoins() <= 0): self.__wallet.remove_euros(10)
        if (bitcoins > self.__wallet.bitcoins()): bitcoins = self.__wallet.bitcoins()
        if (bitcoins <= 0): return
        sale = stock_market.sell_bitcoins(self.__wallet, bitcoins)
        if self.__verbose <= VerboseLevel.DEBUG: sale.print_trade()
        if sale.trade_type() is not TradeType.DENIED:
            self.__tax_declaration.add_trade(sale)


    def hold(self):
        pass
    
    
    def pay_taxes(self, euros):
        if self.__verbose <= VerboseLevel.DEBUG: print("Trader: paying taxes: " + str(euros) + "€")
        self.__wallet.remove_euros(euros)
        
        
    def receive_tax_refund(self, euros):
        if self.__verbose <= VerboseLevel.DEBUG: print("Trader: receiving tax refund: " + str(euros) + "€")
        self.__wallet.insert_euros(euros)
        

    def wallet(self):
        return self.__wallet
    
    
    def strategy(self):
        return self.__strategy


    def is_broke(self):
        if self.__wallet.euros() <= 0 and self.__wallet.bitcoins() <= 0:
            if self.__verbose <= VerboseLevel.DEBUG: print("Trader: is broke")
            return True
        else:
            return False
    
    
    def tax_declaration(self):
        return self.__tax_declaration


    def show(self):
        #print("Trader: financial profit is: " + str(self.get_financial_profit()) + "€")
        self.__wallet.show()