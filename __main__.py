# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 17:59:03 2021

@author: Andre
"""


from CryptoGenerator.CryptoGenerator import CryptoGenerator
from CryptoGenerator.VerboseLevel import VerboseLevel


def main():
    start_money = 1000
    verbose = VerboseLevel.INFO
    crypto_generator = CryptoGenerator(start_money, verbose)
    crypto_generator.run()


if __name__ == "__main__":
    main()

