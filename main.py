#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 11:29:52 2024

@author: fran
"""

import numpy as np
from parameters import number_players, number_decks, stands_on_17
from blackjack_class import BlackJack

blackjack = BlackJack(number_players, number_decks)

blackjack.game_initialization()

# Player rounds
for ii in range(number_players):
    print("Player", ii+1, "starts the round")
    blackjack.player_round(ii)
    
# Croupier round
blackjack.croupier_round(stands_on_17)

print(blackjack.players_count)
print(blackjack.cards_in_deck)