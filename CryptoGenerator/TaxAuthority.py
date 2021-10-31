# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 02:30:54 2021

@author: Andre
"""

from CryptoGenerator.TaxDeclaration import TaxDeclaration
from CryptoGenerator.Trader import Trader

class TaxAuthority: 


    def __init__(self, taxes_percentage):
        self.__taxes_percentage = taxes_percentage

    
    def make_tax_declaration(self, trader):
        taxes = calculate_taxes_to_pay(trader.tax_declaration())
        trader.pay_taxes(taxes)
        trader.tax_declaration().clear_profit()


    def calculate_taxes_to_pay(self, tax_declaration):
        taxes = tax_declaration.profit_to_declare() * self.__taxes_percentage / 100
        if (taxes < 0): taxes = 0
        print("TaxAuthority: taxes to pay: " + str(taxes) + "€")
        return taxes
        

        
        
