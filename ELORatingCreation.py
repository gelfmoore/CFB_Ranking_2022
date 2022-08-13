# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 14:26:00 2022

@author: gelfm
"""

expected_scaling = 600
base_k = 25
home_field_advantage = 12.75 # results in a 3 point home field advantage

def get_expected_win_perecentage(rating, opp_rating):
    exp = (opp_rating - rating) / expected_scaling
    return 1 / (1 + 10**exp)

def get_new_elos(home_rating, away_rating, margin, k=base_k, nuetral=0, hfa=home_field_advantage):

    # score of 1 for a win
    home_score = 0.5 + margin/(2*40)
    if home_score > 1:
        home_score = 1
    if home_score < 0:
        home_score = 0
        
    if nuetral == 1:
        home_field_advantage = 0

    # get expected home score
    expected_home_score = get_expected_win_perecentage(home_rating+hfa, away_rating)
    # multiply difference of actual and expected score by k value and adjust home rating
    new_home_score = home_rating + k * (home_score - expected_home_score)

    # repeat these steps for the away team
    # away score is inverse of home score
    away_score = 1 - home_score
    expected_away_score = get_expected_win_perecentage(away_rating, home_rating+hfa)
    new_away_score = away_rating + k * (away_score - expected_away_score)

    # return a tuple
    return (round(new_home_score), round(new_away_score))
    


# print(get_expected_win_perecentage(1550, 1450)) # Standard Game
# print(get_expected_win_perecentage(1800, 1500)) # Big Dog vs Average
# print(get_expected_win_perecentage(1800, 1200)) # Big Dog vs FCS

# print(get_new_elos(1525, 1475, 42, base_k))
# print(get_new_elos(1525, 1475, 14, base_k))
# print(get_new_elos(1525, 1475, 7, base_k))
# print(get_new_elos(1525, 1475, -14, base_k))
# print(get_new_elos(1525, 1475, -42, base_k))

# print(get_new_elos(1800, 1500, 42, base_k))
# print(get_new_elos(1800, 1500, 14, base_k))
# print(get_new_elos(1800, 1500, -14, base_k))

# print(get_new_elos(1800, 1200, 42, base_k))
# print(get_new_elos(1800, 1200, 14, base_k))
# print(get_new_elos(1800, 1200, -14, base_k))

# print(get_new_elos(1500, 1500, 9, base_k))
# print(get_new_elos(1500, 1500, 6, base_k))
# print(get_new_elos(1500, 1500, 3, base_k))
# print(get_new_elos(1500, 1500, 0, base_k))
# print(get_new_elos(1500, 1500, -3, base_k))