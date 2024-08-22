import pandas as pd


def preprocess(df,df_region):
    """
    Preprocesses the data:
        filters based on season
        drops duplicate values
        creates dummy columns for Medals
        returns a combined dataframe 
    """
    # Filtering dataframe for summer season
    df = df[df['Season'] == 'Summer']
    # merging the two data frames on NOC
    df = df.merge(df_region,how='left',on = 'NOC')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # Using One Hot Encoding on medals column
    medal_dummies = pd.get_dummies(df['Medal'])
    df = pd.concat([df,medal_dummies],axis = 1)

    return df