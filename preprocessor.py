import pandas as pd


def preprocess(df , df_region):
    # filtering for the summer Olympics
    df = df[df['Season'] == 'Summer']
    # merge with the region_df
    df = df.merge(df_region,on='NOC' ,how='left')
    # Dropping Duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding on medals
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df
