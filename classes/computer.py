import random
from classes.cards import Card
from classes.player import Player

class Computer(Player):

    POINTS_TO_CALL_SUIT = 30

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
    
    def order_up_card(self, suit: str, flipped_c: Card, dealer: Player, testing: bool):
    # This function gives the computer the option to tell the dealer to pick up the card.
    # Aggressiveness of computer ordering up card depends on POINTS_TO_CALL_SUIT integer
        suit_dict = {'Clubs': 0, 'Diamonds': 1, 'Hearts': 2, 'Spades': 3}
        suit_idx = suit_dict.get(flipped_c.suit)
        if self.card_values[suit_idx] >= self.POINTS_TO_CALL_SUIT:
            suit = flipped_c.suit
            was_card_picked_up = True
            caller = self
            dealer.drop_card(flipped_c, self)
        else:
            was_card_picked_up = False
            caller = None
            not testing and print(f'{self.name}: Pass')
        return self, suit, was_card_picked_up, dealer, caller

    def drop_card(self, flipped_c: Card, caller: Player):
        ranks = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.hand.append(flipped_c)
        discard = None
        for rank in ranks:
            for each_card in self.hand:
                if each_card.get_rank() == rank and each_card.left_bower_suit != flipped_c.suit:
                    discard = each_card
                    break
            else:
                continue
            break
        try:
            self.hand.pop(self.hand.index(discard))
        except ValueError:  # This happens if dealer has no non-clincher cards
            len_hand = len(self.hand)
            self.hand.pop(random.randint(0, len_hand - 1))

    def choose_call_suit(self, suit: str, flipped_c: Card, testing: bool):
    # This will give the computer the option to call suit after everyone has refused to call the suit of flipped card
    # It will only call suit if the player has more pts in that suit than the variable POINTS_TO_CALL_SUIT

        was_suit_declared = False
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        best_suit_idx = self.card_values.index(max(self.card_values))
        if self.card_values[best_suit_idx] < self.POINTS_TO_CALL_SUIT:
            caller = None
            not testing and print(f'{self.name}: Pass')
            pass
        elif suits[best_suit_idx] == flipped_c.suit:  # Comp may not call suit that was turned down earlier
            self.card_values[best_suit_idx] = 0
            second_best_suit_idx = self.card_values.index(max(self.card_values))
            if self.card_values[second_best_suit_idx] < self.POINTS_TO_CALL_SUIT:
                caller = None
                not testing and print(f'{self.name}: Pass')
                pass
            else:
                was_suit_declared = True
                caller = self
                suit = suits[second_best_suit_idx]
        else:
            was_suit_declared = True
            caller = self
            suit = suits[best_suit_idx]
        return suit, was_suit_declared, caller
    
    def must_call_suit(self, suit: str, flipped_c: Card):
    # This forces the computer to call a suit after everyone has turned down the flipped card and then refused
    # to call suit. Only happens when comp is dealer. If the best suit for comp matched that of the flipped card,
    # comp card_values for that suit is set to 0.

        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        best_suit_idx = self.card_values.index(max(self.card_values))
        was_suit_declared = True
        caller = self
        if suits[best_suit_idx] == flipped_c.get_suit():
            self.card_values[best_suit_idx] = 0
            second_best_suit_idx = self.card_values.index(max(self.card_values))
            suit = suits[second_best_suit_idx]
        else:
            suit = suits[best_suit_idx]

        return suit, was_suit_declared, caller
    
    def lead_card(self):
    # This allows the computer player to play any card as the first card of the trick
    # Comp will always play a card of the highest rank - even if it is a clincher (legal play, but not always strategic)

        lead = None
        ranks = ['Ace', 'King', 'Queen', 'Jack', '10', '9']

        if len(self.hand) == 1:
            lead = self.hand[0]
            self.hand.pop(self.hand.index(lead))
        else:
            for rank in ranks:
                for each_card in self.hand:
                    if each_card.get_rank() == rank and not each_card.clincher:
                        lead = each_card
                        self.hand.pop(self.hand.index(lead))
                        break
                else:
                    continue
                break

            if not lead:  # If we didn't pick a card to lead earlier (this happens when comp. only has clinchers)
                clincher_ranks = ['Jack', 'Ace', 'King', 'Queen', '10', '9']
                for c_rank in clincher_ranks:
                    for clincher in self.hand:
                        if clincher.get_rank() == c_rank:
                            lead = clincher
                            self.hand.pop(self.hand.index(lead))
                            break
                    else:
                        continue
                    break

        return lead
    
    def follow_suit(self, lead_c: Card, played: list[Card]):
        if len(self.hand) == 1:
            card_to_play = self.hand[0]
        else:
            currently_winning_card = played[0]
            cards_to_follow_suit = {}
            for c in self.hand:
                if c.left_bower_suit == lead_c.left_bower_suit:  # If the card in hand has the same suit as card lead then..
                    cards_to_follow_suit[c] = c.point  # Add that card to dict of cards that follow suit
                else:
                    pass

            for played_card in played:  # This looks at all cards played already and determines which is winning so far
                if played_card.point > currently_winning_card.point:
                    currently_winning_card = played_card

            best_card = max(cards_to_follow_suit, key=cards_to_follow_suit.get)
            worst_card = min(cards_to_follow_suit, key=cards_to_follow_suit.get)

            if best_card.point > currently_winning_card.point:
                if len(played) == 3 and played.index(currently_winning_card) == 1:
                    card_to_play = worst_card
                else:
                    card_to_play = best_card
            else:
                card_to_play = worst_card
        self.hand.pop(self.hand.index(card_to_play))

        return card_to_play
    
    def play_clincher(self, played: list[Card], calling_player: Player):
        clinchers = {}
        currently_winning_card = played[0]
        players_yet_to_play = ['1', '2', '3', '4']

        for played_card in played:
            if played_card.point > currently_winning_card.point:
                currently_winning_card = played_card
            players_yet_to_play.pop(players_yet_to_play.index(str(played_card.owner)))

        for card in self.hand:  # this makes a dictionary of the clinchers in the computers hand. This is used to
            if card.get_clincher:  # decide which card to play later
                clinchers[card] = card.point

        card_to_play = max(clinchers, key=clinchers.get)

        for card in played:
            winning_card = played[0]
            if card.point > winning_card.point:
                winning_card = card

        if card_to_play.point < winning_card.point:  # If the computer's clincher cannot win the round,
            raise ValueError  # then raise an error and discard a bad card instead

        elif len(played) == 3 and played.index(winning_card) == 1:  # If the computer is last to play and teammate is
            raise ValueError  # winning, raise ValueError to discard bad card

        elif len(clinchers) > 1 and calling_player.number not in players_yet_to_play:  # If comp has >1 clincher and
            lowest_winning_card = card_to_play  # the player who called suit has yet to play, play lowest clincher
            for c in clinchers:  # that will still take the lead in the trick
                if winning_card.point < c.point < lowest_winning_card.point:
                    lowest_winning_card = c
            card_to_play = lowest_winning_card
            self.hand.pop(self.hand.index(card_to_play))
        else:
            self.hand.pop(self.hand.index(card_to_play))
        return card_to_play
    
    def discard_bad_card(self, suit: str):
    # This makes the computer discard their lowest rank, non-clincher card
    # If all cards are clincher, the lowest clincher will be played
        bad_card = None
        ranks = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
        clincher_ranks = ['9', '10', 'Queen', 'King', 'Ace', 'Jack']

        all_cards_are_clincher = True
        for each_card in self.hand:
            if not each_card.clincher:
                all_cards_are_clincher = False
        if all_cards_are_clincher:
            for rank in clincher_ranks:
                for each_card in self.hand:
                    if each_card.get_rank() == rank:
                        bad_card = each_card
                        break
                else:
                    continue
                break
        else:
            for rank in ranks:
                for each_card in self.hand:
                    if each_card.get_rank() == rank and each_card.left_bower_suit != suit:
                        bad_card = each_card
                        break
                else:
                    continue
                break
        self.hand.pop(self.hand.index(bad_card))
        return bad_card
