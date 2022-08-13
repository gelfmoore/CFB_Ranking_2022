# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 13:23:14 2022

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

