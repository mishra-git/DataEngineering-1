import os
import pandas as pd
df = pd.read_json('data/log_data/2018/11/2018-11-01-events.json', lines=True)
print(df)