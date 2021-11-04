# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:41:03 2021

@author: Andre
"""


from CryptoGenerator.Wallet import Wallet
from CryptoGenerator.Strategy import Strategy
from CryptoGenerator.StockMarket import TradeType
from CryptoGenerator.TaxDeclaration import TaxDeclaration
from CryptoGenerator.TaxDeclaration import TaxType


class Trader:
    
    
    def __init__(self, start_money):
        self.__wallet = Wallet(start_money,0)
        self.__strategy = Strategy()
        self.__tax_declaration = TaxDeclaration(TaxType.FIFO)
        
        
    def do_action(self, stock_market):
        action = self.__strategy.receive_action(stock_market, self.__wallet)
        if (action > 0):
            self.buy(stock_market, action)
        elif (action < 0):
            self.sell(stock_market, self.__wallet.bitcoins())
        else:
            self.hold()
        self.__strategy.update(self.__wallet)
        
        
    def buy(self, stock_market, euros):
        if (euros > self.__wallet.euros()): euros = self.__wallet.euros()
        if (euros <= 0): return
        purchase = stock_market.buy_bitcoins(self.__wallet, euros)
        purchase.print_trade()
        if purchase.trade_type() is not TradeType.DENIED:
            self.__tax_declaration.add_trade(purchase)
        # print(len(self.__tax_declaration.purchases()))
        # print(self.__tax_declaration.purchases()[0].print_trade())
            
        
    
    def sell(self, stock_market, bitcoins):
        if (bitcoins > self.__wallet.bitcoins()): bitcoins = self.__wallet.bitcoins()
        if (bitcoins <= 0): return
        sale = stock_market.sell_bitcoins(self.__wallet, bitcoins)
        if sale.trade_type() is not TradeType.DENIED:
            sale.print_trade()
            self.__tax_declaration.add_trade(sale)


    def hold(self):
        pass
    
    
    def pay_taxes(self, euros):
        print("Trader: paying taxes: " + str(euros) + "€")
        self.__wallet.remove_euros(euros)
        
        
    def receive_tax_refund(self, euros):
        print("Trader: receiving tax refund: " + str(euros) + "€")
        self.__wallet.insert_euros(euros)
        

    def wallet(self):
        return self.__wallet

    def is_broke(self):
        if self.__wallet.euros() <= 0 and self.__wallet.bitcoins() <= 0:
            print("Trader: is broke")
            return True
        else:
            return False
    
    
    def tax_declaration(self):
        return self.__tax_declaration


    def show(self):
        #print("Trader: financial profit is: " + str(self.get_financial_profit()) + "€")
        self.__wallet.show()