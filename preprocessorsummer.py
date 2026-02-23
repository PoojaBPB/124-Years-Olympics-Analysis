import pandas as pd
df1 = pd.read_csv('Athletes_summer_games.csv')
df2 = pd.read_csv('regions.csv')
def preprocess(df1,df2):
    global df
    #merge df
    df = (
        df1.merge(
            df2[['region', 'NOC']],
            on='NOC',
            how='left'
        )
    )
    #dropping duplicates
    df = df.drop_duplicates()
    #one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)
    return df
