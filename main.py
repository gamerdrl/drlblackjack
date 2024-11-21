#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 11:29:52 2024

@author: fran
"""

from parameters import number_players, number_decks, stands_on_17, bet, game_rounds, debug
from blackjack_class import BlackJack

blackjack = BlackJack(number_players, number_decks, debug)

for ii in range(game_rounds):
    blackjack.game_initialization()
    
    # Player rounds
    for jj in range(number_players):
        if not blackjack.flag_blackjack[jj]:
            if debug: print("Player", jj+1, "starts the round")
            blackjack.player_round(jj, jj, flag_first_entrance = True)
        else:
            if debug: print("Player", jj+1, "has a blackjack")
        
    # Croupier round
    croupier_playing = any(value <= 21 for value in blackjack.players_count_soft[0:-1])
    if croupier_playing:
        blackjack.croupier_round(stands_on_17)
    else:
        "All players have passed 21 and croupier does not need to play"
    
    # Budget delivery
    blackjack.budget_delivery(bet)

    if debug: print(blackjack.players_count_hard)
    if debug: print(blackjack.players_budget)

if debug: print(blackjack.players_budget)