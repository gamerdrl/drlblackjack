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
        self.players_budget = np.zeros(self.number_players)
            
    
    def game_initialization(self):
        # Shuffle the deck of cards every round
        self.cards_in_deck = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
                              5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8,
                              9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10,
                              10, 10, 10, 10, 10, 10, 10, 10] * self.number_decks
        
        # Players and croupier counts. croupier count is the last value of the array
        self.players_count_hard  = np.zeros(self.number_players + 1, dtype=int)
        self.players_count_soft  = np.zeros(self.number_players + 1, dtype=int)
        self.players_final_count = np.zeros(self.number_players + 1, dtype=int)
        
        # Flag for soft counts
        self.flag_player_playing_soft = np.full(self.number_players + 1, False, dtype=bool)
        
        # Flag to indicate if players and croupier have a blackjack
        self.flag_blackjack = np.full(self.number_players + 1, False, dtype=bool)
        
        # Flag to indicate if players has doubled
        self.flag_double = np.ones(self.number_players, dtype=int)
        
        # Flag to indicate that split is available
        self.flag_split = np.full(self.number_players, False, dtype=bool)
        # Counter of splits by player
        self.players_splits = np.zeros(self.number_players, dtype=int)
        
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
                self.flag_split[ii] = True
            if not self.flag_player_playing_soft[ii]:  # Player does not have an As
                if dealt_card > 1:
                    self.players_count_hard[ii] = self.players_count_hard[ii] + dealt_card  # Add the card to the count
                    self.players_count_soft[ii] = self.players_count_soft[ii] + dealt_card
                else:  # Player gets an As
                    self.flag_player_playing_soft[ii] = True  # Activate soft count
                    self.players_count_hard[ii] = self.players_count_hard[ii] + dealt_card + 10
                    self.players_count_soft[ii] = self.players_count_soft[ii] + dealt_card
                    if self.players_count_hard[ii] == 21:  # Player has a blackjack
                        self.flag_blackjack[ii] = True  # Player has a blackjack
            else:  # Player had an As
                self.players_count_hard[ii] = self.players_count_hard[ii] + dealt_card
                self.players_count_soft[ii] = self.players_count_soft[ii] + dealt_card
                if dealt_card == 10:
                    self.flag_blackjack[ii] = True  # Player has a blackjack
                
            print("Player", ii+1, "gets a", dealt_card, "and sums", self.players_count_hard[ii])
    
    
    def player_round(self, original_player, player_id, flag_first_entrance = False):
        # Original player is the player that is playing the round
        # player_id will refer the the position in the array vector.
        # original_player and player_id will differ when there are splits
        # flag_first_entrance is used to set the correct position of player_id in case previous player have splitted
        if flag_first_entrance:
            player_id = original_player + np.sum(self.players_splits[0:original_player])
        playing = True  # Flag to tell when to stand
        self.flag_first_action = True  # This flag is used to determine if player is on first action so he can use to double
        # Possible actions:
        # 0: stand
        # 1: hit
        # 2: double (after double only 1 card is dealt)
        # 3: split
        # 4: protect (only available when croupier has an As and if rules allow it)
        while playing:
            self.get_possible_actions(self.players_count_hard[player_id],self.flag_split[player_id],
                                      self.players_count_hard[-1])  # self.players_count_hard[-1] is croupier count
            action = random.choice(self.possible_actions)
            # This if is only for the print
            if action == 0:
                action_string = "stands"
            elif action == 1:
                action_string = "hits a card"
            elif action == 2:
                action_string = "doubles the bet"
            elif action == 3:
                action_string = "splits"
            elif action == 4:
                action_string = "protects"
            print("Player", player_id+1, action_string)
            if action == 2:  # Player doubles the bet
                action = 1       # Do as a normal hit
                playing = False  # and end the game
                self.flag_double[player_id] = 2
            
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
            elif action == 3:  # Player splits
                self.players_count_hard[player_id] /= 2  # Split the count
                self.players_count_soft[player_id] /= 2
                # Add one value to the count vectors. This added value will be the new count (from the split) for player_id
                self.players_count_hard = np.insert(self.players_count_hard, player_id+1, self.players_count_hard[player_id])
                self.players_count_soft = np.insert(self.players_count_soft, player_id+1, self.players_count_soft[player_id])
                self.players_final_count = np.insert(self.players_final_count, player_id+1, 0)
                # Add the value to the flags
                self.flag_player_playing_soft = np.insert(self.flag_player_playing_soft, player_id+1, self.flag_player_playing_soft[player_id])
                self.flag_blackjack = np.insert(self.flag_blackjack, player_id+1, False)
                self.flag_double = np.insert(self.flag_double, player_id+1, 1)
                self.flag_split = np.insert(self.flag_split, player_id+1, False)
                # Reset split flag of player_id to False
                self.flag_split[player_id] = False
                # Play the fisrt card splited
                dealt_card = random.choice(self.cards_in_deck)  # Deal the card
                self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
                if dealt_card == self.players_count_soft[player_id]:
                    self.flag_split[player_id] = True
                if not self.flag_player_playing_soft[player_id]:  # Player does not have an As
                    if dealt_card > 1:
                        self.players_count_hard[player_id] = self.players_count_hard[player_id] + dealt_card  # Add the card to the count
                        self.players_count_soft[player_id] = self.players_count_soft[player_id] + dealt_card
                    else:  # Player gets an As
                        self.flag_player_playing_soft[player_id] = True  # Activate soft count
                        self.players_count_hard[player_id] = self.players_count_hard[player_id] + dealt_card + 10
                        self.players_count_soft[player_id] = self.players_count_soft[player_id] + dealt_card
                        if self.players_count_hard[player_id] == 21:  # Player has a blackjack
                            self.flag_blackjack[player_id] = True  # Player has a blackjack
                else:  # Player had an As
                    self.players_count_hard[player_id] = self.players_count_hard[player_id] + dealt_card
                    self.players_count_soft[player_id] = self.players_count_soft[player_id] + dealt_card
                    if dealt_card == 10:
                        self.flag_blackjack[player_id] = True  # Player has a blackjack
                print("The card is a", dealt_card, "and count is", self.players_count_hard[player_id], "for the split")
                if not self.flag_blackjack[player_id]:
                    self.player_round(original_player, player_id)
                else:
                    print("Player", player_id+1, "has a blackjack")
                self.players_splits[original_player] += 1  # Add 1 split to player count
                
                # Play the second card splited
                player_id = sum(self.players_splits[0:original_player+1]) + original_player  # Adjust the player_id to match the array position
                dealt_card = random.choice(self.cards_in_deck)  # Deal the card
                self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
                if dealt_card == self.players_count_soft[player_id]:
                    self.flag_split[player_id] = True
                if not self.flag_player_playing_soft[player_id]:  # Player does not have an As
                    if dealt_card > 1:
                        self.players_count_hard[player_id] = self.players_count_hard[player_id] + dealt_card  # Add the card to the count
                        self.players_count_soft[player_id] = self.players_count_soft[player_id] + dealt_card
                    else:  # Player gets an As
                        self.flag_player_playing_soft[player_id] = True  # Activate soft count
                        self.players_count_hard[player_id] = self.players_count_hard[player_id] + dealt_card + 10
                        self.players_count_soft[player_id] = self.players_count_soft[player_id] + dealt_card
                        if self.players_count_hard[player_id] == 21:  # Player has a blackjack
                            self.flag_blackjack[player_id] = True  # Player has a blackjack
                else:  # Player had an As
                    self.players_count_hard[player_id] = self.players_count_hard[player_id] + dealt_card
                    self.players_count_soft[player_id] = self.players_count_soft[player_id] + dealt_card
                    if dealt_card == 10:
                        self.flag_blackjack[player_id] = True  # Player has a blackjack
                print("The card is a", dealt_card, "and count is", self.players_count_hard[player_id], "for the split")
                if not self.flag_blackjack[player_id]:
                    self.player_round(original_player, player_id)
                else:
                    print("Player", player_id+1, "has a blackjack")
                playing = False  # Once all splits have ended, end player round
                
        if not action == 3:
            if not self.flag_player_playing_soft[player_id] or self.players_count_hard[player_id] <= 21:  # Player does not have an As or has an As but still ends with the hard count
                self.players_final_count[player_id] = self.players_count_hard[player_id]
            else:  # Player has an As and ends with the soft count
                self.players_final_count[player_id] = self.players_count_soft[player_id]
                    
                
    def croupier_round(self, stands_on_17):
        if stands_on_17:
            croupier_stands = 17
        else:
            croupier_stands = 18
        
        # Play first croupier round to see if croupier gets a blackjack
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
                if self.players_count_hard[-1] == 21:  # Croupier has a blackjack
                    self.flag_blackjack[-1] = True  # Croupier has a blackjack
        else:  # Croupier had an As
            self.players_count_hard[-1] = self.players_count_hard[-1] + dealt_card  # Add the card to the croupier count
            self.players_count_soft[-1] = self.players_count_soft[-1] + dealt_card
            if dealt_card == 10:
                self.flag_blackjack[-1] = True  # Croupier has a blackjack
                    
        print("Croupier deals a", dealt_card, "and count is", self.players_count_hard[-1])
        
        # Play until stand
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
            
        if self.players_count_hard[-1] > 21 and self.flag_player_playing_soft[-1]:  # Croupier has an As an has another chance with the soft count
            while self.players_count_soft[-1] < croupier_stands:  # self.players_count_soft[-1] is croupier soft count
                # Deal a card for croupier
                dealt_card = random.choice(self.cards_in_deck)  # Deal the card
                self.cards_in_deck.remove(dealt_card)  # Remove the card from the deck
                self.players_count_hard[-1] = self.players_count_hard[-1] + dealt_card  # Add the card to the croupier count
                self.players_count_soft[-1] = self.players_count_soft[-1] + dealt_card
                
                print("Croupier deals a", dealt_card, "and soft count is", self.players_count_soft[-1])
                
        if not self.flag_player_playing_soft[-1] or self.players_count_hard[-1] <= 21:  # Croupier does not have an As orhas an As but still ends with the hard count
            self.players_final_count[-1] = self.players_count_hard[-1]
        else:  # Croupier has an As and ends with the soft count
            self.players_final_count[-1] = self.players_count_soft[-1]
        
        # This if is for the print
        if self.players_final_count[-1] > 21:
            print("Croupier passes 21 and player wins")
        else:
            print("Croupier stands with", self.players_final_count[-1])
        
        
    def get_possible_actions(self, player_count, flag_split, croupier_count):  # TODO: develope this
        if player_count < 12:
            self.possible_actions = [1]
        else:
            self.possible_actions = [0, 1]
            
        if self.flag_first_action:
            self.possible_actions.append(2)
            self.flag_first_action = False
        
        if flag_split:
            self.possible_actions.append(3)
            
        if croupier_count == 11:  # Add the possibility of protect if croupier has an As
            self.possible_actions.append(4)
    
    
    def budget_delivery(self, bet):
        #[18, 22, 14,   20, 26,   20, 24,   20]
        croupier_count = self.players_final_count[-1]  # Note tha in the case where all player have passed this value will be 0, but the fact that players passed is dominant
        player_id = -1  # This will be used as a counter to point to the correct position of the arrays
        for ii in range(self.number_players):
            for jj in range(self.players_splits[ii] + 1):
                player_id += 1
                player_count = self.players_final_count[player_id]  # Note that in the case where the player has a blackjack this value will be 0, but flag_flagjack will appear before
                if player_count > 21:  # Player has passed, so player losses
                    self.players_budget[ii] = self.players_budget[ii] - bet*self.flag_double[player_id]
                else:  # Player has not passed
                    if self.flag_blackjack[player_id]:  # Player has a blackjack
                        if not self.flag_blackjack[-1]:  # And croupier does not
                            self.players_budget[ii] = self.players_budget[ii] + 1.5*bet
                    elif croupier_count > 21: # Croupier has passed, so player wins
                        self.players_budget[ii] = self.players_budget[ii] + bet*self.flag_double[player_id]
                    elif player_count > croupier_count:  # Player is closer to 21, so player wins
                        self.players_budget[ii] = self.players_budget[ii] + bet*self.flag_double[player_id]
                    elif player_count < croupier_count: # Croupier is closer to 21, so player losses
                        self.players_budget[ii] = self.players_budget[ii] - bet*self.flag_double[player_id]
                    # else game is tied so no need to adjust budget
