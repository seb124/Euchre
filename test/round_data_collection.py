import sys
import os
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random
from classes.computer import Computer
from classes.aiv1 import AIV1
from classes.aiv2 import AIV2
from classes.aiv3 import AIV3
from classes.aiv4 import AIV4
from classes.cards import Deck
from classes.player import Team
import engine


"""
This file collects data for every *round* played. Run the function below to collect this data.
Because up to 20 rounds can be played per game, the round_data csv files are not created - otherwise, they
could have up to 20,000,000 lines of data in them. As such, only the game wins data, found in the 
"game_data_collection.py" file, is recorded/analyzed for now.

round_data_collection can be ran (shown below) to create/populate the corresponding round_data csv files.
We only record player 1's hand/decisions for now.

Round data could be used for more sophisticated analysis and for machine learning purposes (for example,
reducing the number of times a team loses after a player on that team orders up the trump card).
"""

# binomial test this. null: p = 0.5 alt: p != 0.5
# scipy.stats.binomtest
# count # wins and find p-value. Awesome
# also record all hands and status of round in a csv file for completeness

line = [[], None, "none", None]


def play_round(team1, team2, player1, player2, player3, player4, deck, dlr_index, dlr, ldr_index, testing, path):
    global line

    deck.deal_cards(player1)
    deck.deal_cards(player2)
    deck.deal_cards(player3)
    deck.deal_cards(player4)

    player1.tricks_won = 0
    player2.tricks_won = 0
    player3.tricks_won = 0
    player4.tricks_won = 0

    flipped_card = deck.flip_card()

    line[0] = [c.card_string for c in player1.hand]
    line[1] = flipped_card.card_string


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
            if player == 1:
                line[2] = "call"
            break
        else:
            if player == 1:
                line[2] = "pass"
            other_players = [player_num for player_num in player_order if player_num != player]
            for other_player in other_players:
                player_map[other_player].update_probability_table(player, "pass", flipped_card, flipped_card.suit)

    if not was_suit_picked:
        for player in player_order:
            best_suit, was_suit_picked, calling_player = \
                player_map[player].choose_call_suit(best_suit, flipped_card, testing)
            if was_suit_picked:
                break
            else:
                other_players = [player_num for player_num in player_order if player_num != player]
                for other_player in other_players:
                    for suit in ['Clubs', 'Diamonds', 'Hearts', 'Spades']:
                        if suit != flipped_card.suit:
                            player_map[other_player].update_probability_table(player, "pass", flipped_card, suit)


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

    player1.assign_left_bower(best_suit)
    player2.assign_left_bower(best_suit)
    player3.assign_left_bower(best_suit)
    player4.assign_left_bower(best_suit)


    for _ in range(5):
        player1, player2, player3, player4, ldr_index = engine.play_trick(player1, player2, player3, player4,
                                                               ldr_index, best_suit, calling_player, testing)

    team1.tricks = player1.tricks_won + player3.tricks_won
    team2.tricks = player2.tricks_won + player4.tricks_won

    if team1.tricks > team2.tricks:
        line[3] = True
        if calling_player.name == 'Player2' or calling_player.name == 'Player4' or team1.tricks == 5:
            team1.points += 2
        else:
            team1.points += 1
    elif team2.tricks > team1.tricks:
        line[3] = False
        if calling_player.name == 'Player1' or calling_player.name == 'Player3' or team2.tricks == 5:
            team2.points += 2
        else:
            team2.points += 1


    # write data for round to csv file
    with open(path, "a") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(line)

    line = [[], None, "none", None]

    return team1, team2, player1, player2, player3, player4

def play_game(p1, p2, p3, p4, testing, path):
    d = Deck()
    d.show()

    team_1 = Team(p1, p3, 0, 0)
    team_2 = Team(p2, p4, 0, 0)


    players = {p1: 1, p2: 2, p3: 3, p4: 4}
    dealer, dealer_index = random.choice(list(players.items()))
    leader_index = (dealer_index % 4) + 1

    while team_1.points < 11 and team_2.points < 11:
        team_1, team_2, p1, p2, p3, p4 = play_round(team_1, team_2, p1, p2, p3,
                                                                            p4, d, dealer_index, dealer, leader_index, testing, path)
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
            return "Team 1"
        elif team_2.points >= 11:
            return "Team 2"
        
player_mapper = {"computer": Computer, "aiv1": AIV1, "aiv2": AIV2, "aiv3": AIV3, "aiv4": AIV4}

def round_data_collection(p1: str, p2: str, p3: str, p4: str, games: int):
    global line

    player_1 = player_mapper[p1.lower()]
    player_2 = player_mapper[p2.lower()]
    player_3 = player_mapper[p3.lower()]
    player_4 = player_mapper[p4.lower()]

    if p1 == p3 and p2 == p4:
        path = f"test/data/round_data/{p1.lower()}_{p2.lower()}_round_data.csv"
    else:
        path = f"test/data/round_data/{p1.lower()}_{p2.lower()}_{p3.lower()}_{p4.lower()}_round_data.csv"

    if not os.path.exists(path):
        with open(path, "w") as file:
            file.write("hand,trump,action,round_win\n")
    
    for _ in range(games):
        play_game(player_1(1), player_2(2), player_3(3), player_4(4), True, path)


# put any players here to get/add round data based on those teams
round_data_collection("computer", "aiv1", "computer", "aiv1", 1000)

# TODO: put this in another file - statistical_analysis or something
# stats = scipy.stats.binomtest(k=wins, n=10000)
# print(wins / 10000)
# print(stats.pvalue)
