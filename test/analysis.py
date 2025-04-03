import sys
import os
import scipy.stats
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This file runs some analysis on the data collected in "game_data_collection.py". 
Results are shown below, and functions can be run below to replicate results.
"""

def statistical_analysis(p1: str, p2: str, p3: str, p4: str):
    # run binomial dist test on the results to see if AI versions made a significant difference
    # tests to see whether % of team 1 wins != 0.5

    if p1 == p3 and p2 == p4:
        path = f"test/data/game_data/{p1.lower()}_{p2.lower()}_game_data.txt"
    else:
        path = f"test/data/game_data/{p1.lower()}_{p2.lower()}_{p3.lower()}_{p4.lower()}_game_data.txt"

    if not os.path.exists(path):
        raise FileNotFoundError("Path specified \"" + path + "\" does not exist.")

    wins = 0
    total = 0
    with open(path) as data:
        for line in data:
            arr = line.split(" ")
            wins += int(arr[0])
            total += int(arr[0]) + int(arr[1])
            
    # measure pvalue
    stats = scipy.stats.binomtest(k=wins, n=total)

    # prints win % along with p-value and 95% confidence interval (CI)
    print(f"Team 1 wins {(wins / total) * 100}% of the time.")
    print(f"p-value: {stats.pvalue}")
    print(f"CI: {stats.proportion_ci()}")


# VS COMPUTER (100,000 GAMES EACH)
statistical_analysis("AIV1", "Computer", "AIV1", "Computer") # AIV1 win rate: 53.239000000000004%, p-value: 2.6862671971923357e-93, 95% CI: (low=0.5292916320469402, high=0.5354864890286386)
statistical_analysis("AIV2", "Computer", "AIV2", "Computer") # AIV2 win rate: 61.882999999999996%, p-value: 0.0, 95% CI: (low=0.6158114039982123, high=0.6218417023422181)
statistical_analysis("AIV3", "Computer", "AIV3", "Computer") # AIV3 win rate: 62.531000000000006%, p-value: 0.0, 95% CI: (low=0.6223013272859204, high=0.628311403077847)
statistical_analysis("AIV4", "Computer", "AIV4", "Computer") # AIV4 win rate: 62.81099999999999%, p-value: 0.0, 95% CI: (low=0.6251057922847414, high=0.6311067756171674)

# VS AIV1 (100,000 GAMES EACH)
statistical_analysis("AIV2", "AIV1", "AIV2", "AIV1") # AIV2 win rate: 57.809999999999995%, p-value: 0.0, 95% CI: (low=0.5750318347504272, high=0.5811636346157978)
statistical_analysis("AIV3", "AIV1", "AIV3", "AIV1") # AIV3 win rate: 57.620000000000005%, p-value: 0.0, 95% CI: (low=0.5731300508287185, high=0.5792655287639541)
statistical_analysis("AIV4", "AIV1", "AIV4", "AIV1") # AIV4 win rate: 58.577%, p-value: 0.0, 95% CI: (low=0.5827095091591896, high=0.5888255152373761)

# VS AIV2 (100,000 GAMES EACH)
statistical_analysis("AIV3", "AIV2", "AIV3", "AIV2") # AIV3 win rate: 50.198%, p-value: 0.2116284059513479, 95% CI: (low=0.4988760293604932, high=0.5050838557812223)
statistical_analysis("AIV4", "AIV2", "AIV4", "AIV2") # AIV4 win rate: 50.407999999999994%, p-value: 0.009958458801279513 , 95% CI: (low=0.5009760473257705, high=0.5071837159968597)

# VS AIV3 (100,000 GAMES)
statistical_analysis("AIV4", "AIV3", "AIV4", "AIV3") # AIV4 win rate: 50.858000000000004%, p-value: 5.846460960629578e-08, 95% CI: (low=0.5054762699255869, high=0.5116832323559826)


# So, we conlcude that effectively all AI iterations improve upon the baseline Computer team and against themselves. 
# The only inconclusive test is AIV3 vs AIV2 with 100,000 games - here, we fail to reject the null hypothesis, so
# the win rate could be equal.
