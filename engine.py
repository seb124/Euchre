import random
import time
from termcolor import colored
from classes.cards import Deck
from classes.player import Team

# This is the card game Euchre. Rules: https://bicyclecards.com/how-to-play/euchre/
# Cards used are 9 up to Ace. 'Going alone' for a round is not a feature of this script

def determine_winning_trick_so_far(played):
    # This function determines which played is currently winning the trick, as in who has played the best card so far
    # Used to help the computer make strategic decisions about which card to play

    points_scored = {}
    for pc in played:
        points_scored[pc.owner] = pc.point
    player_in_lead = max(points_scored, key=points_scored.get)
    return player_in_lead


def assign_point_trick_winner(winning_play, play1, play2, play3, play4):
    #  Keeps track of the numbers of tricks each player has won
    if winning_play == 1:
        play1.tricks_won += 1
    elif winning_play == 2:
        play2.tricks_won += 1
    elif winning_play == 3:
        play3.tricks_won += 1
    elif winning_play == 4:
        play4.tricks_won += 1
    return play1, play2, play3, play4


def determine_trick_winner(played, testing):
    # After all 4 cards are played, this function finds the one with the highest point value. that card wins the trick
    # and the winning player (owner of that card) is returned
    cards_points = {}
    for c in played:
        cards_points[c] = c.point
        if not testing:
            print(f'{c.display} (P{c.owner})')
            time.sleep(.4)
    winning_card = max(cards_points, key=cards_points.get)
    winner = winning_card.owner
    not testing and print(f'\nPlayer{winner} won with the {winning_card.display}')
    return winner


def play_trick(p1, p2, p3, p4, round_leader, best_suit, caller, testing):
    # The user can now play a card by choosing the index (1-5) of the card to play. That suit is lead
    # and must be followed by other players
    not testing and print(colored(f'\nClincher: {best_suit} ({caller.name})', 'green'))

    p1.assign_clincher(best_suit)
    p2.assign_clincher(best_suit)
    p3.assign_clincher(best_suit)
    p4.assign_clincher(best_suit)

    player_map = {1: p1, 2: p2, 3: p3, 4: p4}
    round_order = [round_leader, round_leader % 4 + 1, (round_leader + 1) % 4 + 1, (round_leader + 2) % 4 + 1]

    lead_card = player_map[round_leader].lead_card()

    played_cards = [lead_card]

    p1.assign_points(best_suit, lead_card)
    p2.assign_points(best_suit, lead_card)
    p3.assign_points(best_suit, lead_card)
    p4.assign_points(best_suit, lead_card)

    player_in_lead = round_leader

    not testing and time.sleep(1.75)

    for player in round_order[1:]:
        try:
            played_card = player_map[player].follow_suit(lead_card, played_cards)
        except ValueError:
            try:
                if player_in_lead == (player + 1) % 4 + 1:
                    raise ValueError
                else:
                    played_card = player_map[player].play_clincher(played_cards, caller)
            except ValueError:
                played_card = player_map[player].discard_bad_card(best_suit)
        played_cards.append(played_card)
        player_in_lead = determine_winning_trick_so_far(played_cards)

    winning_player = determine_trick_winner(played_cards, testing)

    p1, p2, p3, p4 = assign_point_trick_winner(winning_player, p1, p2, p3, p4)

    not testing and print(colored(f'\nRound Score: {p1.tricks_won + p3.tricks_won}-{p2.tricks_won + p4.tricks_won}', 'green'))

    return p1, p2, p3, p4, winning_player


def play_round(team1, team2, player1, player2, player3, player4, deck, dlr_index, dlr, ldr_index, testing):
    #  This function runs each round of Euchre and will be looped over until enough points are scored (11 by 1 team)
    not testing and deck.show()
    deck.deal_cards(player1)
    deck.deal_cards(player2)
    deck.deal_cards(player3)
    deck.deal_cards(player4)

    player1.tricks_won = 0
    player2.tricks_won = 0
    player3.tricks_won = 0
    player4.tricks_won = 0

    flipped_card = deck.flip_card()

    not testing and print(f'\nDealer: {dlr.name}\nFlipped: {flipped_card.display}\n')
    not testing and time.sleep(1.5)

    best_suit = ''

    player1.evaluate_cards()
    player2.evaluate_cards()
    player3.evaluate_cards()
    player4.evaluate_cards()

    player_map = {1: player1, 2: player2, 3: player3, 4: player4}

    player_order = [(dlr_index) % 4 + 1, (dlr_index + 1) % 4 + 1, (dlr_index + 2) % 4 + 1, dlr_index]

    was_suit_picked = False

    for player in player_order:
        player_map[player], best_suit, was_suit_picked, player_map[dlr_index], calling_player = \
            player_map[player].order_up_card(best_suit, flipped_card, dlr_index, player_map[dlr_index], testing)
        if was_suit_picked:
            break
        else:
            other_players = [player_num for player_num in player_order if player_num != player]
            for other_player in other_players:
                player_map[other_player].update_probability_table(player, "pass", flipped_card)
                random_integer = random.randint(1, 100)
                if ((player % 2) != (other_player % 2) and (random_integer <=20)):
                    not testing and player_map[other_player].generate_smack_talk("pass")

    if not was_suit_picked:
        for player in player_order:
            best_suit, was_suit_picked, calling_player = \
                player_map[player].choose_call_suit(best_suit, flipped_card, testing)
            if was_suit_picked:
                break

    if not was_suit_picked:
        best_suit, was_suit_picked, calling_player = player_map[dlr_index].must_call_suit(best_suit, flipped_card)

    for c in player1.hand:
        c.owner = 1
    for c in player2.hand:
        c.owner = 2
    for c in player3.hand:
        c.owner = 3
    for c in player4.hand:
        c.owner = 4

    not testing and print(colored(f'{calling_player.name}: {best_suit} is clincher suit.', 'green'))
    not testing and time.sleep(1.3)

    player1.assign_left_bower(best_suit)
    player2.assign_left_bower(best_suit)
    player3.assign_left_bower(best_suit)
    player4.assign_left_bower(best_suit)

    for _ in range(5):
        player1, player2, player3, player4, ldr_index = play_trick(player1, player2, player3, player4,
                                                               ldr_index, best_suit, calling_player, testing)

    team1.tricks = player1.tricks_won + player3.tricks_won
    team2.tricks = player2.tricks_won + player4.tricks_won

    if team1.tricks > team2.tricks:
        if calling_player.name == 'Player2' or calling_player.name == 'Player4' or team1.tricks == 5:
            team1.points += 2
            not testing and print(f'\nYou win! Team 1 won, taking {team1.tricks} tricks. Your team scored 2 points!')
        else:
            team1.points += 1
            not testing and print(f'\nYou win! Team 1 won, taking {team1.tricks} tricks. Your team scored 1 point!')
    elif team2.tricks > team1.tricks:
        if calling_player.name == 'Player1' or calling_player.name == 'Player3' or team2.tricks == 5:
            team2.points += 2
            not testing and print(f'\nYou lost this round! Team 2 won, taking {team2.tricks} tricks. They scored 2 points!')
        else:
            team2.points += 1
            not testing and print(f'\nYou lost this round! Team 2 won, taking {team2.tricks} tricks. They scored 1 point!')

    not testing and time.sleep(2.5)
    not testing and print(f'\nThe game score is {team1.points}-{team2.points}')
    not testing and time.sleep(2.5)

    return team1, team2, player1, player2, player3, player4

def play_game(p1, p2, p3, p4, testing):
    # Create the 4 players and the deck out of the 24 possible cards.
    # Randomly assign 5 cards to each player (no repeats)
    # Flip one remaining card

    d = Deck()
    d.show()

    team_1 = Team(p1, p3, 0, 0)
    team_2 = Team(p2, p4, 0, 0)


    players = {p1: 1, p2: 2, p3: 3, p4: 4}
    dealer, dealer_index = random.choice(list(players.items()))
    leader_index = (dealer_index % 4) + 1

    while team_1.points < 11 and team_2.points < 11:
        team_1, team_2, p1, p2, p3, p4 = play_round(team_1, team_2, p1, p2, p3,
                                                                            p4, d, dealer_index, dealer, leader_index, testing)
        dealer_index = dealer_index % 4 + 1
        leader_index = leader_index % 4 + 1
        dealer = list(players.keys())[list(players.values()).index(dealer_index)]
        d.destroy()
        d.build()

        p1.reset_probability_table(d)
        p2.reset_probability_table(d)
        p3.reset_probability_table(d)
        p4.reset_probability_table(d)

        if team_1.points >= 11:
            not testing and print(f'You win the game! Final Score: {team_1.points}-{team_2.points}')
            return "Team 1"
        elif team_2.points >= 11:
            not testing and print(f'You lose the game! Final Score: {team_1.points}-{team_2.points}')
            return "Team 2"
