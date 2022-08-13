# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 15:04:35 2022

@author: gelfm
"""

import cfbd
import datetime
import numpy as np
import pandas as pd

def date_sort(game):
    game_date = datetime.datetime.strptime(game['start_date'], "%Y-%m-%dT%H:%M:%S.000Z")
    return game_date

def elo_sort(team):
    return team['elo']

def get_games(start_year, end_year):
    # configure API key
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = '9cYyODmHzpyjf07e1lhK0oxu5HfUeJKzWuh2yKn78w7k0csr/yXUq8EraiEgcUXC'
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    
    # instantiate a games API instance
    games_api = cfbd.GamesApi(cfbd.ApiClient(configuration))
    
    games = []
    
    for year in range(start_year, end_year):
        response = games_api.get_games(year=year)
        games = [*games, *response]
        response = games_api.get_games(year=year,season_type="postseason")
        games = [*games, *response]
    
    games = [dict(
                start_date=g.start_date,
                season=g.season,
                home_team=g.home_team,
                home_conference=g.home_conference,
                home_points=g.home_points,
                away_team=g.away_team,
                away_conference=g.away_conference,
                away_points=g.away_points,
                nuetral=g.neutral_site
                ) for g in games if g.home_points is not None and g.away_points is not None]
    games.sort(key=date_sort)
    return games

# testgames = get_games(2021, 2022)
