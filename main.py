#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 11:29:52 2024

@author: fran
"""

from parameters import number_players, number_decks, stands_on_17, bet, game_rounds
from blackjack_class import BlackJack

blackjack = BlackJack(number_players, number_decks)

for ii in range(game_rounds):
    blackjack.game_initialization()
    
    # Player rounds
    for jj in range(number_players):
        print("Player", jj+1, "starts the round")
        blackjack.player_round(jj)
        
    # Croupier round
    croupier_playing = any(value <= 21 for value in blackjack.players_count[0:-1])
    if croupier_playing:
        blackjack.croupier_round(stands_on_17)
    else:
        "All players have passed 21 and croupier does not need to play"
    
    # Budget delivery
    blackjack.budget_delivery(bet)

    print(blackjack.players_count)

print(blackjack.players_budget)