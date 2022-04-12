# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 17:59:03 2021

@author: Andre
"""


from CryptoGenerator.CryptoGenerator import CryptoGenerator
from CryptoGenerator.VerboseLevel import VerboseLevel

import time

def main():
    time_start_total = time.time()

    start_money = 1000
    verbose = VerboseLevel.INFO
    load_existing_network = None#'network_weights_2021-12-01-14-36-47'
    crypto_generator = CryptoGenerator(start_money=start_money, load_existing_network=load_existing_network, verbose=verbose)
    crypto_generator.run()
    
    time_end_total = time.time()
    if verbose <= VerboseLevel.INFO: print ("execution time for total is: " + str((time_end_total - time_start_total) / 60) + " min")


if __name__ == "__main__":
    main()

