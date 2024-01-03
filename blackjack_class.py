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
        
        # Players budget
        self.players_budget = np.zeros(self.number_players, dtype=int)
        
        # Players and croupier counts. croupier count is the last value of the array
        self.players_count_hard  = np.zeros(self.number_players + 1, dtype=int)
        self.players_count_soft  = np.zeros(self.number_players + 1, dtype=int)
        self.players_final_count = np.zeros(self.number_players + 1, dtype=int)
        
        # Flag for soft counts
        self.flag_player_playing_soft = np.full(self.number_players + 1, False, dtype=bool)
        
        # Flag to indicate if players and croupier have a blackjack
        self.flag_blackjack = np.full(self.number_players + 1, False, dtype=bool)
        
        # Flag to indicate that split is available
        self.flag_split = np.full(self.number_players, False, dtype=bool)
            
    
    def game_initialization(self):
        # Shuffle the deck of cards every round
        self.cards_in_deck = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
                              5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8,
                              9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10,
                              10, 10, 10, 10, 10, 10, 10, 10] * self.number_decks
        for ii in range(self.number_players + 1):  # Deal 1 card to each player and to croupier
            dealt_card = random.choice(self.cards_in_deck)  # Deal the card
            self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
            if dealt_card > 1:
                self.players_count_hard[ii] = dealt_card  # Add the card to the count
                self.players_count_soft[ii] = dealt_card
            else:  # Player gets an As
                self.flag_player_playing_soft[ii] = True  # Activate soft count
                self.players_count_hard[ii] = dealt_card + 10  # Add the card to the count
                self.players_count_soft[ii] = dealt_card
            # This if is only for the print
            if ii < self.number_players:
                print("Player", ii+1, "gets a", dealt_card)
            else:
                print("Croupier gets a", dealt_card)
        
        # Deal the second card to each player
        for ii in range(self.number_players):  # Croupier does not receive card now
            dealt_card = random.choice(self.cards_in_deck)  # Deal the card
            self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
            if dealt_card == self.players_count_soft[ii]:
                self.flag_split = True
            if not self.flag_player_playing_soft[ii]:  # Player does not have an As
                if dealt_card > 1:
                    self.players_count_hard[ii] = self.players_count_hard[ii] + dealt_card  # Add the card to the count
                    self.players_count_soft[ii] = self.players_count_soft[ii] + dealt_card
                else:  # Player gets an As
                    self.flag_player_playing_soft[ii] = True  # Activate soft count
                    self.players_count_hard[ii] = self.players_count_hard[ii] + dealt_card + 10
                    self.players_count_soft[ii] = self.players_count_soft[ii] + dealt_card
            else:  # Player had an As
                self.players_count_hard[ii] = self.players_count_hard[ii] + dealt_card
                self.players_count_soft[ii] = self.players_count_soft[ii] + dealt_card
                
            print("Player", ii+1, "gets a", dealt_card, "and sums", self.players_count_hard[ii])
    
    def player_round(self, player_id):
        playing = True  # Flag to tell when to stand
        # Possible actions:
        # 0: stand
        # 1: hit
        # 2: double (after double only 1 card is dealt)
        # 3: split
        # 4: protect (only available when croupier has an As and if rules allow it)
        while playing:
            self.get_possible_actions(self.players_count_hard[player_id], self.players_count_hard[-1])  # self.players_count_hard[-1] is croupier count
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
                if not self.flag_player_playing_soft[player_id]:  # Player does not have an As
                    if dealt_card > 1:
                        self.players_count_hard[player_id] = self.players_count_hard[player_id] + dealt_card  # Add the card to the count
                        self.players_count_soft[player_id] = self.players_count_soft[player_id] + dealt_card
                    else:  # Player gets an As
                        self.flag_player_playing_soft[player_id] = True  # Activate soft count
                        self.players_count_hard[player_id] = self.players_count_hard[player_id] + dealt_card + 10
                        self.players_count_soft[player_id] = self.players_count_soft[player_id] + dealt_card
                else:  # Player had an As
                    self.players_count_hard[player_id] = self.players_count_hard[player_id] + dealt_card
                    self.players_count_soft[player_id] = self.players_count_soft[player_id] + dealt_card
                print("The card is a", dealt_card, "and count is", self.players_count_hard[player_id])
                if self.players_count_hard[player_id] > 21:
                    if not self.flag_player_playing_soft[player_id]:  # Player does not have an As
                        playing = False  # End player round
                        print("Player", player_id+1, "is over 21 and losses the round")
                    else:
                        if self.players_count_soft[player_id] > 21:
                            playing = False  # End player round
                            print("Player", player_id+1, "is over 21 and losses the round")
                        elif self.players_count_soft[player_id] == 21:
                            playing = False   # End player round
                            print("Player", player_id+1, "gets a 21 and stands")
                elif self.players_count_hard[player_id] == 21:
                    playing = False  # End player round
                    print("Player", player_id+1, "gets a 21 and stands")
                    
        if not self.flag_player_playing_soft[player_id]:  # Player does not have an As
            self.players_final_count[player_id] = self.players_count_hard[player_id]
        elif self.players_count_hard[player_id] <= 21:  # Player has an As but still ends with the hard count
            self.players_final_count[player_id] = self.players_count_hard[player_id]
        else:  # Player has an As and ends with the soft count
            self.players_final_count[player_id] = self.players_count_soft[player_id]
                    
    def croupier_round(self, stands_on_17):
        if stands_on_17:
            croupier_stands = 17
        else:
            croupier_stands = 18
            
        while self.players_count_hard[-1] < croupier_stands:  # self.players_count_hard[-1] is croupier count
            # Deal a card for croupier
            dealt_card = random.choice(self.cards_in_deck)  # Deal the card
            self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
            if not self.flag_player_playing_soft[-1]:  # Croupier does not have an As
                if dealt_card > 1:
                    self.players_count_hard[-1] = self.players_count_hard[-1] + dealt_card  # Add the card to the croupier count
                    self.players_count_soft[-1] = self.players_count_soft[-1] + dealt_card
                else:  # Croupier gets an As
                    self.flag_player_playing_soft[-1] = True  # Activate soft count
                    self.players_count_hard[-1] = self.players_count_hard[-1] + dealt_card + 10  # Add the card to the croupier count
                    self.players_count_soft[-1] = self.players_count_soft[-1] + dealt_card
            else:  # Croupier had an As
                self.players_count_hard[-1] = self.players_count_hard[-1] + dealt_card  # Add the card to the croupier count
                self.players_count_soft[-1] = self.players_count_soft[-1] + dealt_card
                    
            print("Croupier deals a", dealt_card, "and count is", self.players_count_hard[-1])
            
        if self.flag_player_playing_soft[-1]:  # Croupier has an As an has another chance with the soft count
            while self.flag_player_playing_soft[-1] < croupier_stands:  # self.players_count_hard[-1] is croupier count
                # Deal a card for croupier
                dealt_card = random.choice(self.cards_in_deck)  # Deal the card
                self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
                self.players_count_hard[-1] = self.players_count_hard[-1] + dealt_card  # Add the card to the croupier count
                self.players_count_soft[-1] = self.players_count_soft[-1] + dealt_card
                
                print("Croupier deals a", dealt_card, "and count is", self.players_count_soft[-1])
                
        if not self.flag_player_playing_soft[-1]:  # Croupier does not have an As
            self.players_final_count[-1] = self.players_count_hard[-1]
        elif self.players_count_hard[-1] <= 21:  # Croupier has an As but still ends with the hard count
            self.players_final_count[-1] = self.players_count_hard[-1]
        else:  # Croupier has an As and ends with the soft count
            self.players_final_count[-1] = self.players_count_soft[-1]
        
        # This if is for the print
        if self.players_final_count[-1] > 21:
            print("Croupier passes 21 and player wins")
        else:
            print("Croupier stands with", self.players_final_count[-1])
        
        
        
        
    def get_possible_actions(self, player_count, croupier_count):  # TODO: develope this
        if player_count < 12:
            self.possible_actions = [1]
        else:
            self.possible_actions = [0, 1]
    
    def budget_delivery(self, bet):
        croupier_count = self.players_final_count[-1]
        for ii in range(self.number_players):
            player_count = self.players_final_count[ii]
            if croupier_count > 21:  # Croupier has passes, which means that player wins
                self.players_budget[ii] = self.players_budget[ii] + bet
            else:  # Croupier has not passed
                if player_count > 21: # Player has passes, so player losses
                    self.players_budget[ii] = self.players_budget[ii] - bet
                elif player_count > croupier_count:  # Player is closer to 21, so player wins
                    self.players_budget[ii] = self.players_budget[ii] + bet
                elif player_count < croupier_count: # Croupier is closer to 21, so player losses
                    self.players_budget[ii] = self.players_budget[ii] - bet
                # else game is tied so no need to adjust budget
        
        