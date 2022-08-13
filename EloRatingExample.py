# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 12:07:43 2022

@author: gelfm
"""

import cfbd
import datetime
import numpy as np
import pandas as pd

# configure API key
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = '9cYyODmHzpyjf07e1lhK0oxu5HfUeJKzWuh2yKn78w7k0csr/yXUq8EraiEgcUXC'
configuration.api_key_prefix['Authorization'] = 'Bearer'

# instantiate a games API instance
api_config = cfbd.ApiClient(configuration)
games_api = cfbd.GamesApi(cfbd.ApiClient(configuration))

def get_expected_score(rating, opp_rating):
    exp = (opp_rating - rating) / 200
    return 1 / (1 + 10**exp)

print(get_expected_score(1500, 1500))
print(get_expected_score(1400, 1500))
print(get_expected_score(2000, 1500))

def get_new_elos(home_rating, away_rating, margin):
    k = 20

    # score of 0.5 for a tie
    home_score = 0.5
    if margin > 0:
        # score of 1 for a win
        home_score = 1
    elif margin < 0:
        #score of 0 for a loss
        home_score = 0

    # get expected home score
    expected_home_score = get_expected_score(home_rating, away_rating)
    # multiply difference of actual and expected score by k value and adjust home rating
    new_home_score = home_rating + k * (home_score - expected_home_score)

    # repeat these steps for the away team
    # away score is inverse of home score
    away_score = 1 - home_score
    expected_away_score = get_expected_score(away_rating, home_rating)
    new_away_score = away_rating + k * (away_score - expected_away_score)

    # return a tuple
    return (round(new_home_score), round(new_away_score))

def date_sort(game):
    game_date = datetime.datetime.strptime(game['start_date'], "%Y-%m-%dT%H:%M:%S.000Z")
    return game_date

def elo_sort(team):
    return team['elo']

games = []

for year in range(1975, 2022):
    response = games_api.get_games(year=year)
    games = [*games, *response]

games = [dict(
            start_date=g.start_date,
            home_team=g.home_team,
            home_conference=g.home_conference,
            home_points=g.home_points,
            away_team=g.away_team,
            away_conference=g.away_conference,
            away_points=g.away_points
            ) for g in games if g.home_points is not None and g.away_points is not None]
games.sort(key=date_sort)

# dict object to hold current Elo rating for each team
teams = dict()

# loop through games in order
for game in games:
    # if game['home_team'] is 'BYU':
    #     print(f"game['home_conference']")
    # get current rating for home team
    if game['home_team'] in teams:
        home_elo = teams[game['home_team']]
    elif game['home_conference'] is None:
        # if no rating, set initial rating to 1500 for FBS teams
        home_elo = 1200
    else:
        # otherwise, set initial rating to 1200 for non-FBS teams
        home_elo = 1100

    # get current rating for away team
    if game['away_team'] in teams:
        away_elo = teams[game['away_team']]
    elif game['away_conference'] is not None:
        # if no rating, set initial rating to 1500 for FBS teams
        away_elo = 1500
    else:
        # otherwise, set initial rating to 1200 for non-FBS teams
        away_elo = 1100

    # calculate score margin from game
    margin = game['home_points'] - game['away_points']
    
    # get new elo ratings
    new_elos = get_new_elos(home_elo, away_elo, margin)
    
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
end_elos.sort(key=elo_sort, reverse=True)

# print(end_elos)

import matplotlib.pyplot as plt

# This is the styling I use. Check out other themes here: https://matplotlib.org/3.2.1/gallery/style_sheets/style_sheets_reference.html
plt.style.use('fivethirtyeight')

# Graph sizing
plt.rcParams["figure.figsize"] = [20,10]

def generate_chart(team):
    team_games = []
    for game in games:
        if game['home_team'] == team:
            team_games.append(dict(start_date=game['start_date'], elo=game['postgame_home_elo']))

        if game['away_team'] == team:
            team_games.append(dict(start_date=game['start_date'], elo=game['postgame_away_elo']))

    df = pd.DataFrame.from_records(team_games)

    fig, ax = plt.subplots()
    ax.plot(df.index, df['elo'])

    ax.set(xlabel='Game No.', ylabel='Elo Rating',
           title="Historical Elo Rating - {0}".format(team))

    plt.show()

generate_chart('Utah State')