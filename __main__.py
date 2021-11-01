# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 17:59:03 2021

@author: Andre
"""


from CryptoGenerator.CryptoGenerator import CryptoGenerator


def main():
    start_money = 10000
    crypto_generator = CryptoGenerator(start_money)
    crypto_generator.run()


if __name__ == "__main__":
    main()

