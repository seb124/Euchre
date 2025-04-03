import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.computer import Computer
from classes.aiv1 import AIV1
from classes.aiv2 import AIV2
from classes.aiv3 import AIV3
from classes.aiv4 import AIV4
import engine

"""
This file collects data for games of Euchre for statistical analysis. Column 1 is the number
of times Team 1 wins, and Column 2 is the number of times Team 2 wins. It writes 10 lines per
function no matter the number of games played to avoid huge files.
"""

player_mapper = {"computer": Computer, "aiv1": AIV1, "aiv2": AIV2, "aiv3": AIV3, "aiv4": AIV4}

def game_data_collection(p1: str, p2: str, p3: str, p4: str, games: int):
    team1_wins = 0
    team2_wins = 0

    player_1 = player_mapper[p1.lower()]
    player_2 = player_mapper[p2.lower()]
    player_3 = player_mapper[p3.lower()]
    player_4 = player_mapper[p4.lower()]

    if p1 == p3 and p2 == p4:
        path = f"test/data/game_data/{p1.lower()}_{p2.lower()}_game_data.txt"
    else:
        path = f"test/data/game_data/{p1.lower()}_{p2.lower()}_{p3.lower()}_{p4.lower()}_game_data.txt"

    for game in range(1, (games + 1)):
        res = engine.play_game(player_1(1), player_2(2), player_3(3), player_4(4), True)

        if res == "Team 1":
            team1_wins += 1
        else:
            team2_wins += 1

        if game % (games / 10) == 0:
            file = open(path, "a")
            file.write(f"{team1_wins} {team2_wins}\n")
            team1_wins = 0
            team2_wins = 0


# Put any players here to get/add game data based on those teams.
# We deemed these 10 the most important to measure overall effectiveness.

# game_data_collection("AIV1", "Computer", "AIV1", "Computer", 100000)
# game_data_collection("AIV2", "Computer", "AIV2", "Computer", 100000)
# game_data_collection("AIV3", "Computer", "AIV3", "Computer", 100000)
# game_data_collection("AIV4", "Computer", "AIV4", "Computer", 100000)

# game_data_collection("AIV2", "AIV1", "AIV2", "AIV1", 100000)
# game_data_collection("AIV3", "AIV1", "AIV3", "AIV1", 100000)
# game_data_collection("AIV4", "AIV1", "AIV4", "AIV1", 100000)

# game_data_collection("AIV3", "AIV2", "AIV3", "AIV2", 100000)
# game_data_collection("AIV4", "AIV2", "AIV4", "AIV2", 100000)

# game_data_collection("AIV3", "AIV4", "AIV3", "AIV4", 100000) # not needed
