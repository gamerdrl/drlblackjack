#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 11:30:58 2024

@author: fran
"""

import numpy as np
import random

class BlackJack():
    def __init__(self, number_players, number_decks):
        self.number_players = number_players
        self.number_decks = number_decks
        
        self.cards_in_deck = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
                              5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8,
                              9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10,
                              10, 10, 10, 10, 10, 10, 10, 10] * self.number_decks
        
        # Players and croupier counts. croupier count is the last value of the array
        self.players_count = np.zeros(self.number_players + 1, dtype=int)
            
    
    def game_initialization(self):
        for ii in range(self.number_players + 1):  # Deal 1 card to each player and to croupier
            dealt_card = random.choice(self.cards_in_deck)  # Deal the card
            self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
            self.players_count[ii] = dealt_card  # Add the card to the count
            # This if is only for the print
            if ii < self.number_players:
                print("Player", ii+1, "gets a", dealt_card)
            else:
                print("Croupier gets a", dealt_card)
        
        # Deal the second card to each player
        for ii in range(self.number_players):  # Croupier does not receive card now
            dealt_card = random.choice(self.cards_in_deck)  # Deal the card
            self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
            if dealt_card == self.players_count[ii]:
                flag_split = True  # TODO: improve this so we know which player has the split option
            self.players_count[ii] = self.players_count[ii] + dealt_card  # Add the card to the count
            print("Player", ii+1, "gets a", dealt_card, "and sums", self.players_count[ii])
    
    def player_round(self, player_id):
        playing = True  # FLag to tell when to stand
        # Possible actions:
        # 0: stand
        # 1: hit
        # 2: double (after double only 1 card is dealt)
        # 3: split
        # 4: protect (only available when croupier has an As and if rules allow it)
        while playing:
            self.get_possible_actions(self.players_count[player_id], self.players_count[-1])  # self.players_count[-1] is croupier count
            action = random.choice(self.possible_actions)
            # This if is only for the print
            if action == 0:
                action_string = "stands"
            elif action == 1:
                action_string = "hits a card"
            print("Player", player_id+1, action_string)
            
            if action == 0:
                playing = False  # End player round
            elif action == 1:  # Deal a card
                dealt_card = random.choice(self.cards_in_deck)  # Deal the card
                self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
                self.players_count[player_id] = self.players_count[player_id] + dealt_card  # Add the card to the count
                print("The card is a", dealt_card, "and count is", self.players_count[player_id])
                if self.players_count[player_id] > 21:
                    playing = False  # End player round
                    print("Player", player_id+1, "is over 21 and losses the round")
                elif self.players_count[player_id] == 21:
                    playing = False  # End player round
                    print("Player", player_id+1, "gets a 21 and stands")
                    
    def croupier_round(self, stands_on_17):
        if stands_on_17:
            croupier_stands = 17
        else:
            croupier_stands = 18
            
        while self.players_count[-1] < croupier_stands:  # self.players_count[-1] is croupier count
            # Deal a card for croupier
            dealt_card = random.choice(self.cards_in_deck)  # Deal the card
            self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
            self.players_count[-1] = self.players_count[-1] + dealt_card  # Add the card to the croupier count
            print("Croupier deals a", dealt_card, "and count is", self.players_count[-1])
            
        # This if is for the print
        if self.players_count[-1] > 21:
            print("Croupier passes 21 and player wins")
        else:
            print("Croupier stands with", self.players_count[-1])
        
        
        
        
    def get_possible_actions(self, player_count, croupier_count):  # TODO: develope this
        if player_count < 12:
            self.possible_actions = [1]
        else:
            self.possible_actions = [0, 1]
        
        