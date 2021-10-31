# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:30:54 2021

@author: Andre
"""


from CryptoGenerator.Trader import Trader


class TaxAuthority: 


    def __init__(self, taxes_percentage, total_taxes_paid_by_trader):
        self.__taxes_percentage = taxes_percentage
        self.__total_taxes_paid_by_trader = total_taxes_paid_by_trader

        
        
    def tax_declaration(self, trader):
        financial_profit_of_trader = trader.get_financial_profit()
        total_taxes_to_pay = financial_profit_of_trader * self.__taxes_percentage / 100
        taxes = total_taxes_to_pay - self.__total_taxes_paid_by_trader
        if (taxes > 0):
            print("Tax Authority: requesting taxes from trader")
            trader.pay_taxes(taxes)
        elif (taxes < 0):
            print("Tax Authority: returning taxes from trader")
            trader.return_taxes(abs(taxes))
        else:
            print("Tax Authority: no taxes to pay")
        self.__total_taxes_paid_by_trader += taxes
        
        
