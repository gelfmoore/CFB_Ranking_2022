# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 11:10:16 2022

@author: gelfm
"""

import cfbd
import numpy as np
import pandas as pd

from fastai.tabular import *
from fastai.tabular.all import *

# Hit Api
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = '9cYyODmHzpyjf07e1lhK0oxu5HfUeJKzWuh2yKn78w7k0csr/yXUq8EraiEgcUXC'
configuration.api_key_prefix['Authorization'] = 'Bearer'

api_config = cfbd.ApiClient(configuration)

teams_api = cfbd.TeamsApi(api_config)
ratings_api = cfbd.RatingsApi(api_config)
games_api = cfbd.GamesApi(api_config)
stats_api = cfbd.StatsApi(api_config)
betting_api = cfbd.BettingApi(api_config)

games = []
lines = []

# Pull games from 2015 to 2022
for year in range(2015, 2022):
    response = games_api.get_games(year=year)
    games = [*games, *response]

    response = betting_api.get_lines(year=year)
    lines = [*lines, *response]
    
games = [g for g in games if g.home_conference is not None and g.away_conference is not None and g.home_points is not None and g.away_points is not None]

games = [
    dict(
        id = g.id,
        year = g.season,
        week = g.week,
        neutral_site = g.neutral_site,
        home_team = g.home_team,
        home_conference = g.home_conference,
        home_points = g.home_points,
        home_elo = g.home_pregame_elo,
        away_team = g.away_team,
        away_conference = g.away_conference,
        away_points = g.away_points,
        away_elo = g.away_pregame_elo
    ) for g in games]

for game in games:
    game_lines = [l for l in lines if l.id == game['id']]

    if len(game_lines) > 0:
        game_line = [l for l in game_lines[0].lines if l['provider'] == 'consensus']

        if len(game_line) > 0 and game_line[0]['spread'] is not None:
            game['spread'] = float(game_line[0]['spread'])
            
games = [g for g in games if 'spread' in g and g['spread'] is not None]

for game in games:
    game['margin'] = game['away_points'] - game['home_points']
    
df = pd.DataFrame.from_records(games).dropna()
df.head()

test_df = df.query("year == 2021")
train_df = df.query("year != 2021")

excluded = ['id','year','week','home_team','away_team','margin', 'home_points', 'away_points']
cat_features = ['home_conference','away_conference','neutral_site']
cont_features = [c for c in df.columns.to_list() if c not in cat_features and c not in excluded]

splits = RandomSplitter(valid_pct=0.2)(range_of(train_df))

to = TabularPandas(train_df, procs=[Categorify, Normalize],
                    y_names="margin",
                    cat_names = cat_features,
                    cont_names = cont_features,
                   splits=splits)

dls = to.dataloaders(bs=64)
print(dls.show_batch())

learn = tabular_learner(dls, metrics=mae, lr=10e-1)
learn.lr_find()

learn = tabular_learner(dls, metrics=mae, lr=10e-2)
learn.fit(10)

learn.show_results()

pdf = test_df.copy()
dl = learn.dls.test_dl(pdf)
pdf['predicted'] = learn.get_preds(dl=dl)[0].numpy()
pdf.head()
pdf[['home_team','away_team','spread','predicted']].round(1)

learn.export('talking_tech_neural_net')
learn = load_learner('talking_tech_neural_net')