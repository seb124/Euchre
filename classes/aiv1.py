import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.computer import Computer
from classes.cards import Card
from classes.player import Player

class AIV1(Computer):
    # update functions as needed - for example, change the order_up_card function to change how this AI behaves when its called in engine.py
    # right now, it's the exact same as the Naive AI "Computer" class

    POINTS_TO_CALL_SUIT = 30
    # At the start of each round, initialize the PT for each player
    def __init__(self, number):
        super().__init__(number)
        
        # Probability table for opponents (keys: player numbers, values: probability distributions)
        self.PT = {
            2: [1/3 for _ in range(24)],  # Equal probability distribution initially
            3: [1/3 for _ in range(24)],
            4: [1/3 for _ in range(24)]
        }


    def assign_points(self, best: str, lead: Card):
    # This is called at the start of every round after the 1st card is played
    # This gives point values to every card that could potentially win the round (clincher > suit of 1st card)
    # This will act as a ranking system to determine which was the best card played that round

        c_clincher = {'Jack of Clubs': 13, 'Jack of Spades': 12, 'Ace of Clubs': 11, 'King of Clubs': 10,
                    'Queen of Clubs': 9, '10 of Clubs': 8, '9 of Clubs': 7}
        d_clincher = {'Jack of Diamonds': 13, 'Jack of Hearts': 12, 'Ace of Diamonds': 11, 'King of Diamonds': 10,
                    'Queen of Diamonds': 9, '10 of Diamonds': 8, '9 of Diamonds': 7}
        h_clincher = {'Jack of Hearts': 13, 'Jack of Diamonds': 12, 'Ace of Hearts': 11, 'King of Hearts': 10,
                    'Queen of Hearts': 9, '10 of Hearts': 8, '9 of Hearts': 7}
        s_clincher = {'Jack of Spades': 13, 'Jack of Clubs': 12, 'Ace of Spades': 11, 'King of Spades': 10,
                    'Queen of Spades': 9, '10 of Spades': 8, '9 of Spades': 7}
        c_lead = {'Ace of Clubs': 6, 'King of Clubs': 5, 'Queen of Clubs': 4, 'Jack of Clubs': 3,
                '10 of Clubs': 2, '9 of Clubs': 1}
        d_lead = {'Ace of Diamonds': 6, 'King of Diamonds': 5, 'Queen of Diamonds': 4, 'Jack of Diamonds': 3,
                '10 of Diamonds': 2, '9 of Diamonds': 1}
        h_lead = {'Ace of Hearts': 6, 'King of Hearts': 5, 'Queen of Hearts': 4, 'Jack of Hearts': 3,
                '10 of Hearts': 2, '9 of Hearts': 1}
        s_lead = {'Ace of Spades': 6, 'King of Spades': 5, 'Queen of Spades': 4, 'Jack of Spades': 3,
                '10 of Spades': 2, '9 of Spades': 1}

        if best == 'Clubs':
            if lead.left_bower_suit == 'Spades':
                s_lead.pop('Jack of Spades')
                c_clincher.update(s_lead)
            elif lead.left_bower_suit == 'Hearts':
                c_clincher.update(h_lead)
            elif lead.left_bower_suit == 'Diamonds':
                c_clincher.update(d_lead)
            elif lead.left_bower_suit == 'Clubs':
                pass
            lead.point = c_clincher.get(lead.card_string, 0)
            for crd in self.hand:
                crd.point = c_clincher.get(crd.card_string, 0)

        elif best == 'Diamonds':
            if lead.left_bower_suit == 'Clubs':
                d_clincher.update(c_lead)
            elif lead.left_bower_suit == 'Diamonds':
                pass
            elif lead.left_bower_suit == 'Hearts':
                h_lead.pop('Jack of Hearts')
                d_clincher.update(h_lead)
            elif lead.left_bower_suit == 'Spades':
                d_clincher.update(s_lead)
            lead.point = d_clincher.get(lead.card_string, 0)
            for crd in self.hand:
                crd.point = d_clincher.get(crd.card_string, 0)

        elif best == 'Hearts':
            if lead.left_bower_suit == 'Clubs':
                h_clincher.update(c_lead)
            elif lead.left_bower_suit == 'Diamonds':
                d_lead.pop('Jack of Diamonds')
                h_clincher.update(d_lead)
            elif lead.left_bower_suit == 'Hearts':
                pass
            elif lead.left_bower_suit == 'Spades':
                h_clincher.update(s_lead)
            lead.point = h_clincher.get(lead.card_string, 0)
            for crd in self.hand:
                crd.point = h_clincher.get(crd.card_string, 0)

        elif best == 'Spades':
            if lead.left_bower_suit == 'Clubs':
                c_lead.pop('Jack of Clubs')
                s_clincher.update(c_lead)
            elif lead.left_bower_suit == 'Diamonds':
                s_clincher.update(d_lead)
            elif lead.left_bower_suit == 'Hearts':
                s_clincher.update(h_lead)
            elif lead.left_bower_suit == 'Spades':
                pass
            lead.point = s_clincher.get(lead.card_string, 0)
            for crd in self.hand:
                crd.point = s_clincher.get(crd.card_string, 0)

    def evaluate_cards(self):
    # This function is run before clincher suit is called
    # It assigns points based on the cards in the players hand
    # It gives points to each suit based on how strong the players hand would be if that suit were clincher
    # This exists so the computer players can use strategy to decide whether to call clincher and which suit to call

        self.card_values = [0, 0, 0, 0]  # [Clubs, Diamonds, Hearts, Spades]
        point_dict_clubs = {'Jack of Clubs': 15, 'Jack of Spades': 13, 'Ace of Clubs': 11, 'King of Clubs': 10,
                            'Queen of Clubs': 9, '10 of Clubs': 8, '9 of Clubs': 7,
                            'Ace of Diamonds': 4, 'Ace of Hearts': 4, 'Ace of Spades': 4}
        point_dict_diamonds = {'Jack of Diamonds': 15, 'Jack of Hearts': 13, 'Ace of Diamonds': 11,
                               'King of Diamonds': 10, 'Queen of Diamonds': 9, '10 of Diamonds': 8, '9 of Diamonds': 7,
                               'Ace of Clubs': 4, 'Ace of Hearts': 4, 'Ace of Spades': 4}
        point_dict_hearts = {'Jack of Hearts': 15, 'Jack of Diamonds': 13, 'Ace of Hearts': 11, 'King of Hearts': 10,
                             'Queen of Hearts': 9, '10 of Hearts': 8, '9 of Hearts': 7,
                             'Ace of Clubs': 4, 'Ace of Diamonds': 4, 'Ace of Spades': 4}
        point_dict_spades = {'Jack of Spades': 15, 'Jack of Clubs': 13, 'Ace of Spades': 11, 'King of Spades': 10,
                             'Queen of Spades': 9, '10 of Spades': 8, '9 of Spades': 7,
                             'Ace of Clubs': 4, 'Ace of Diamonds': 4, 'Ace of Hearts': 4}
        for c in self.hand:
            if c.card_string in point_dict_clubs:
                self.card_values[0] += point_dict_clubs.get(c.card_string)
            else:
                pass
            if c.card_string in point_dict_diamonds:
                self.card_values[1] += point_dict_diamonds.get(c.card_string)
            else:
                pass
            if c.card_string in point_dict_hearts:
                self.card_values[2] += point_dict_hearts.get(c.card_string)
            else:
                pass
            if c.card_string in point_dict_spades:
                self.card_values[3] += point_dict_spades.get(c.card_string)
        return self.card_values    
    
    def update_probability_table(self, player_num: int, action: str, trump_suit: str):
        """
        Update probability table when a player passes or calls trump.
        
        player_num: The player who made the decision (2, 3, or 4)
        action: "pass" or "call"
        trump_suit: The suit in question (e.g., "Spades")
        """
        # Indices for all 8 trump suit cards in the probability table
        trump_cards_indices = [0, 1, 2, 3, 4, 5, 6, 7]  # Jack of Trump, Jack of Off-Suit, A, K, Q, J, 10, 9
        
        top_5_trump_indices = trump_cards_indices[:5]  

        #Ensure no opponent has AI's cards
        for p in self.PT:  
            if p != self.number:  
                removed_prob = 0  # Track total probability removed
                count_unknown_cards = 0  # Count cards that can receive redistributed probability

                for card_idx, card in enumerate(self.hand):  # Check each card in AI's hand
                    removed_prob += self.PT[p][card_idx] 
                    self.PT[p][card_idx] = 0  # No one else can have AI's cards

                #Redistribute probability to remaining unknown cards
                for idx in range(len(self.PT[p])):
                    if self.PT[p][idx] > 0:  # Count valid (unknown) cards
                        count_unknown_cards += 1

                if count_unknown_cards > 0: 
                    redistribute_value = removed_prob / count_unknown_cards  # Evenly distribute lost probability
                    for idx in range(len(self.PT[p])):
                        if self.PT[p][idx] > 0:
                            self.PT[p][idx] += redistribute_value 

        # Adjust Probabilities
        if action == "pass":
            # Player is less likely to have top trump cards
            for idx in top_5_trump_indices:
                self.PT[player_num][idx] *= 0.2  # Reduce their prob

            # Distribute missing probability to other players (only top 5 cards)
            redistribute_amount = sum(self.PT[player_num][idx] for idx in top_5_trump_indices) / 2  
            for p in self.PT:
                if p != player_num:
                    for idx in top_5_trump_indices:
                        self.PT[p][idx] += redistribute_amount / 2

        elif action == "call":
            # Player is more likely to have top trump cards
            for idx in top_5_trump_indices:
                self.PT[player_num][idx] *= 1.5  # Increase their prob

            # Reduce probability of others having these trump cards
            for p in self.PT:
                if p != player_num:
                    for idx in top_5_trump_indices:
                        self.PT[p][idx] *= 0.5  # Reduce their prob

        # ensure prob sum up to 1
        for p in self.PT:
            total = sum(self.PT[p])
            if total > 0:
                self.PT[p] = [x / total for x in self.PT[p]]  # Normalize probabilities



    
    def order_up_card(self, suit: str, flipped_c: Card, dealer: Player, testing: bool):
        """
        Determines whether the AI should order the dealer to pick up the card.
        Updates probability tables based on the AI's decision.
        """
        suit_dict = {'Clubs': 0, 'Diamonds': 1, 'Hearts': 2, 'Spades': 3}
        suit_idx = suit_dict.get(flipped_c.suit)

        if self.card_values[suit_idx] >= self.POINTS_TO_CALL_SUIT:
            suit = flipped_c.suit
            was_card_picked_up = True
            caller = self
            dealer.drop_card(flipped_c, self)
            
            # Update probabilities: AI is more likely to have strong trump cards
            for player in self.PT:
                self.update_probability_table(player, "call", flipped_c.suit)
        
        else:
            was_card_picked_up = False
            caller = None
            not testing and print(f'{self.name}: Pass')

            # Update probabilities: AI is less likely to have strong trump cards
            for player in self.PT:
                self.update_probability_table(player, "pass", flipped_c.suit)

        return self, suit, was_card_picked_up, dealer, caller