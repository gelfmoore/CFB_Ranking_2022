# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 15:19:53 2022

@author: gelfm
"""

import ELORatingCreation
import QueryGames


year_projection = 2022
years_back = 4
start_year = year_projection-years_back

print(f"Getting games from {start_year} to {year_projection-1} Seasons and Post Seasons")
games = QueryGames.get_games(start_year, year_projection)
print(len(games))

"""
Block of code?
"""
FBSlist = ["SEC","Big Ten","Big 12","Pac-12","ACC","Mountain West",
           "Sun Belt","American Athletic","Mid-American","Conference USA",
           "FBS Independents"]
k_base = 30
teams = dict()
# loop through games in order
for game in games:
    if game['home_team'] == 'BYU':
        print(game['home_conference'])
    # get current rating for home team
    if game['home_team'] in teams:
        home_elo = teams[game['home_team']]
    elif game['home_conference'] is None:
        # if no rating, set initial rating to 1500 for FBS teams
        home_elo = 1200
    elif (game['home_conference'] in FBSlist):
        home_elo = 1500
    else:
        # otherwise, set initial rating to 1200 for non-FBS teams
        home_elo = 1200

    # get current rating for away team
    if game['away_team'] in teams:
        away_elo = teams[game['away_team']]
    elif game['away_conference'] is None:
        # if no rating, set initial rating to 1500 for FBS teams
        away_elo = 1200
    elif game['away_conference'] in FBSlist:
        away_elo = 1500
    else:
        # otherwise, set initial rating to 1200 for non-FBS teams
        away_elo = 1200

    # calculate score margin from game
    margin = game['home_points'] - game['away_points']
    k_used = k_base/((2**abs(year_projection-game['season']-1)))
    
    # get new elo ratings
    new_elos = ELORatingCreation.get_new_elos(home_elo, away_elo, margin, k=k_used, nuetral=game['nuetral'])
    
    # set pregame elos on game dict
    game['pregame_home_elo'] = home_elo
    game['pregame_away_elo'] = away_elo
    
    # set postgame elos on game dict
    game['postgame_home_elo'] = new_elos[0]
    game['postgame_away_elo'] = new_elos[1]
    
    # set current elo values in teams dict
    teams[game['home_team']] = new_elos[0]
    teams[game['away_team']] = new_elos[1]
    
end_elos = [dict(team=key, elo=teams[key]) for key in teams]
end_elos.sort(key=QueryGames.elo_sort, reverse=True)


