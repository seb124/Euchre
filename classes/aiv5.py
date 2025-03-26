from classes.aiv3 import AIV3

class AIV5(AIV3):
    
    def choose_call_suit(self, suit, flipped_c, testing, dlr_index):

        was_card_picked = False
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        best_suit = ['', 0]

        # calculate the best suit that wasn't the flipped card suit
        for suit_type in suits:
            if suit_type == flipped_c.suit:
                continue

            teammate_number = ((self.number + 1) % 4) + 1
            opponent_numbers = [p for p in [1, 2, 3, 4] if p not in [self.number, teammate_number]]
            high_value_cards = self.get_high_value_cards(suit_type)
            teammate_trump_prob = sum(self.PT[teammate_number][card] for card in high_value_cards)
            opponent_trump_prob = sum(self.PT[opponent_numbers[0]][card] for card in high_value_cards) + sum(self.PT[opponent_numbers[1]][card] for card in high_value_cards)

            picked_value = self.eval_trump_choice(teammate_trump_prob, opponent_trump_prob, suit_type)

            if (picked_value) > best_suit[1]:
                best_suit = [suit_type, picked_value]

        passed_value = self.eval_alternative_call_suit(flipped_c.suit)

        # if our best suit is better than the predicted value of our opponent's best suit, call the suit. Otherwise, pass
        # and hope either we can stop them from taking all 5 tricks in the next stage of the game or that our teammate has a
        # better hand
        if (best_suit[1]) >= passed_value:
            suit = best_suit[0]
            was_card_picked  = True
            caller = self
        else:
            was_card_picked = False
            caller = None
            not testing and print(f'{self.name} passed on calling a trump suit.')
        return suit, was_card_picked, caller
    
    def eval_alternative_call_suit(self, suit):
        teammate_number = ((self.number + 1) % 4) + 1
        opponent_numbers = [p for p in [1, 2, 3, 4] if p not in [self.number, teammate_number]]
        suit_prob = {suit: 0 for suit in ['Clubs', 'Diamonds', 'Hearts', 'Spades']}

        # calculate suit that they're most likely to have a good hand in 
        for suit_type in ['Clubs', 'Diamonds', 'Hearts', 'Spades']:
            if suit == suit_type:
                continue
            high_value_cards = self.get_high_value_cards(suit_type)
            opponent_trump_prob = sum(self.PT[opponent_numbers[0]][card] for card in high_value_cards) + sum(self.PT[opponent_numbers[1]][card] for card in high_value_cards)
            suit_prob[suit_type] = opponent_trump_prob

        max_prob = 0
        best_suit = ''
        for suit_type in ['Clubs', 'Diamonds', 'Hearts', 'Spades']:
            if suit == suit_type:
                continue
            if suit_prob[suit_type] >= max_prob:
                max_prob = suit_prob[suit_type]
                best_suit = suit_type

        off_suit = {"Spades": "Clubs", "Clubs": "Spades", "Diamonds": "Hearts", "Hearts": "Diamonds"}

        # make an educated guess on the most likely value of opponents' cards
        point_dict = {f'Jack of {best_suit}': 15, f'Jack of {off_suit[best_suit]}': 13, f'Ace of {best_suit}': 11, f'King of {best_suit}': 10,
                            f'Queen of {best_suit}': 9, f'10 of {best_suit}': 8, f'9 of {best_suit}': 7}
        total = 0
        
        # find 5 most likely cards opponent has in their best suit
        card_list = {f'Jack of {best_suit}': max(self.PT[opponent_numbers[0]][f'Jack of {best_suit}'], self.PT[opponent_numbers[1]][f'Jack of {best_suit}']),
                     f'Jack of {off_suit[best_suit]}':max(self.PT[opponent_numbers[0]][f'Jack of {off_suit[best_suit]}'], self.PT[opponent_numbers[1]][ f'Jack of {off_suit[best_suit]}']),
                     f'Ace of {best_suit}':  max(self.PT[opponent_numbers[0]][f'Ace of {best_suit}'], self.PT[opponent_numbers[1]][f'Ace of {best_suit}']),
                     f'King of {best_suit}': max(self.PT[opponent_numbers[0]][f'King of {best_suit}'], self.PT[opponent_numbers[1]][f'King of {best_suit}']),
                     f'Queen of {best_suit}': max(self.PT[opponent_numbers[0]][f'Queen of {best_suit}'], self.PT[opponent_numbers[1]][f'Queen of {best_suit}']),
                     f'10 of {best_suit}': max(self.PT[opponent_numbers[0]][f'10 of {best_suit}'], self.PT[opponent_numbers[1]][f'10 of {best_suit}']),
                     f'9 of {best_suit}': max(self.PT[opponent_numbers[0]][f'9 of {best_suit}'], self.PT[opponent_numbers[1]][f'9 of {best_suit}'])}

        # add up point values (divided by 2 since a single opponent won't have all 5 of the most likely cards) 
        for card in sorted(card_list, key=card_list.get, reverse=True)[0:5]:
            total += point_dict[card] / 2

        return total        