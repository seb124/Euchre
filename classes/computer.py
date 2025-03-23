import random
from classes.cards import Card
from classes.player import Player
import time

class Computer(Player):

    POINTS_TO_CALL_SUIT = 30 
    
    def order_up_card(self, suit: str, flipped_c: Card, dlr_index: int, dealer: Player, testing: bool):
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
            not testing and print(f'{self.name} passed on calling {flipped_c.suit} as the trump suit.')
            not testing and time.sleep(1)
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
            not testing and print(f'{self.name} passed on choosing a trump suit.')
            not testing and time.sleep(1)
            pass
        elif suits[best_suit_idx] == flipped_c.suit:  # Comp may not call suit that was turned down earlier
            self.card_values[best_suit_idx] = 0
            second_best_suit_idx = self.card_values.index(max(self.card_values))
            if self.card_values[second_best_suit_idx] < self.POINTS_TO_CALL_SUIT:
                caller = None
                not testing and print(f'{self.name} passed on choosing a trump suit.')
                not testing and time.sleep(1)
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
