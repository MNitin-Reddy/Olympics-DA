import numpy as np

def medal_tally(df):
    """
    Calculate the total medal tally for each region.

    Args:
        df (DataFrame): Input DataFrame containing medal data.

    Returns:
        DataFrame: A DataFrame with total medals (Gold, Silver, Bronze) per region.
    """
    medal_tally = df.drop_duplicates(subset = ['Team','NOC','Year','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total']= medal_tally[['Gold','Silver','Bronze']].sum(axis = 1)

    return medal_tally

def country_year_list(df):
    """
    Returns lists of unique years and countries from the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing year and country data.

    Returns:
        tuple: A tuple containing two lists: 
            - List of sorted unique years.
            - List of sorted unique countries.
    """
    # Getting the list of years from data
    years =  df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'All')
    # Getting unique countries from data
    # we haven't used df['region'].unique because there are nan values
    # in this column which cause problem when sorting the list of Countries
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'All')

    return years, country

def fetch_medals(df, year,country):
    
    """
    Returns the medal tally for a specified year and country.

    Args:
        df (DataFrame): Input DataFrame containing medal data.
        year (str): Year of results ('All' for all years).
        country (str): Country name ('All' for all countries).

    Returns:
        DataFrame: Grouped DataFrame with total medals by year or country.
    """

    medal_tally = df.drop_duplicates(subset = ['Team','NOC','Year','City','Sport','Event','Medal'])

    flag = 0
    if year == 'All' and country == 'All':
        temp_df = medal_tally
    if year == 'All' and country != 'All':
        flag = 1
        temp_df = medal_tally[medal_tally['region'] == country]
    if year != 'All'  and country == 'All':
        temp_df = medal_tally[medal_tally['Year'] == int(year)]
    if year!= 'All'  and country != 'All':
        temp_df = medal_tally[(medal_tally['Year'] == int(year)) & (medal_tally['region'] == country)]
           
    if flag == 1:
        filtered_df = temp_df.groupby('Year')[['Gold','Silver','Bronze']].sum().sort_values('Year').reset_index()
        filtered_df['Year'] = filtered_df['Year'].astype(str)
    else:
        filtered_df = temp_df.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold', ascending=False).reset_index() 
    
    filtered_df['Total'] = filtered_df[['Gold','Silver','Bronze']].sum(axis = 1)
    
    return filtered_df

def data_over_time(df,base):
    """
    Returns a count of unique entries over the years for a specified base.

    Args:
        df (DataFrame): Input DataFrame containing the data.
        base (str): Column name to group by (e.g., 'region').

    Returns:
        DataFrame: Count of unique entries per year.
    """
    over_year_details = df.drop_duplicates(['Year',base])['Year'].value_counts().reset_index()
    over_year_details = over_year_details.sort_values('Year',ignore_index=True)

    return over_year_details

def sport_events(df):
    """
    Returns a pivot table of unique sports events by year.

    Args:
        df (DataFrame): Input DataFrame containing sports data.

    Returns:
        DataFrame: Pivot table with sports as index and years as columns.
    """
    sports = df.drop_duplicates(['Year','Sport','Event'])
    sports_pivot = sports.pivot_table(index = 'Sport', columns='Year',values = 'Event', aggfunc='count')
    sports_pivot = sports_pivot.fillna(0).astype('int')
    return sports_pivot

def most_popular(df,sport):
    """
    Returns a sorted DataFrame of athletes with the most medals in a specified sport.

    Args:
        df (DataFrame): Input DataFrame containing medal data.
        sport (str): Specific sport to filter by (use 'All' for all sports).

    Returns:
        DataFrame: Sorted DataFrame of athletes by total medals.
    """
    temp_df = df.dropna(subset = ['Medal'])
    if sport != 'All':
        temp_df = temp_df[temp_df['Sport'] == sport]
    temp_df = temp_df.groupby(['Name','Sport','region'])[['Gold','Silver','Bronze']].sum().reset_index()
    temp_df['Total'] = temp_df[['Gold','Silver','Bronze']].sum(axis = 1)
    temp_df.sort_values(by=['Total','Gold','Silver','Bronze'], ignore_index=True ,inplace=True, ascending = False)
    return temp_df
    
def get_sports_list(df):
    """
    Returns a sorted list of unique sports, including an 'All' option.

    Args:
        df (DataFrame): Input DataFrame containing sports data.

    Returns:
        list: Sorted list of unique sports.
    """
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'All')
    return sport_list

def regional_medals(df,region):
    """
    Returns a count of medals won per year for a specified region.

    Args:
        df (DataFrame): Input DataFrame containing medal data.
        region (str): Region to filter medal counts by.

    Returns:
        DataFrame: Count of medals won per year in the specified region.
    """
    df_medalists = df.dropna(subset=['Medal']) 
    df_medalists.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    df_medalists_region = df_medalists[df_medalists['region'] == region ]
    df_medalists_region =  df_medalists_region.groupby('Year')['Medal'].count().reset_index()
    return df_medalists_region

def sports_region(df,region):
    """
    Returns a pivot table of medal counts for each sport in a specified region.

    Args:
        df (DataFrame): Input DataFrame containing medal data.
        region (str): Region to filter the data by.

    Returns:
        DataFrame: Pivot table of medal counts by sport and year, with integer values.
    """
    temp_df = df.dropna(subset=['Medal']) 
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    temp_df = temp_df[temp_df['region'] == region ]
    if temp_df.empty:
        return temp_df
    df_sports_region = temp_df.pivot_table(index='Sport',columns='Year',values='Medal', aggfunc = 'count').fillna(0)
    return df_sports_region.astype('int')

def top_10_region(df,region):
    """
    Returns the top 10 athletes by total medals in a specified region.

    Args:
        df (DataFrame): Input DataFrame containing medal data.
        region (str): Region to filter the data by.

    Returns:
        DataFrame: Top 10 athletes sorted by total medals.
    """
    temp_df = df.dropna(subset = ['Medal'])
    temp_df = temp_df[temp_df['region'] == region]
    temp_df = temp_df.groupby(['Name','Sport'])[['Gold','Silver','Bronze']].sum().reset_index()
    temp_df['Total'] = temp_df[['Gold','Silver','Bronze']].sum(axis = 1)
    temp_df.sort_values(by=['Total','Gold','Silver','Bronze'], ignore_index=True ,inplace=True, ascending = False)

    if temp_df.empty:
        return temp_df

    rows_to_return = min(len(temp_df),10)
    return temp_df.head(rows_to_return)


def athelete_ages(df):
    """
    Returns the distribution of athlete ages and gold medalists' ages in various sports.

    Args:
        df (DataFrame): Input DataFrame containing athlete data.

    Returns:
        tuple: A list of ages, a list of gold medalist ages per sport, and a list of sports names.
    """
    # dropping details of atheletes that are duolicated
    df_atheletes = df.drop_duplicates(subset=['Name','region'])
    df_atheletes= df_atheletes.dropna(subset=['Age'])
    ages = df_atheletes['Age']
    gold_ages = df_atheletes[df_atheletes['Medal']=='Gold']['Age']
    silver_ages = df_atheletes[df_atheletes['Medal']=='Silver']['Age']
    bronze_ages = df_atheletes[df_atheletes['Medal']=='Bronze']['Age']

    age_dist = [ages,gold_ages,silver_ages,bronze_ages]

    sport_gold_ages=[]
    name=[]
    famous_sport = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                    'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                    'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling'
                    'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Shooting',
                    'Boxing', 'Taekwondo', 'Cycling', 'Diving' , 'Canoeing'
                    'Tennis', 'Golf', 'Softball', 'Archery',
                    'Volleyball', 'Synchronized Swimming', 'Table Tennis','Baseball'
                    'Rhythmic Gymnastics', 'Rugby Sevens',
                'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
                ]
    for sport in famous_sport:
        temp_df = df_atheletes[df_atheletes['Sport']==sport]
        gold_medal_ages = temp_df[temp_df['Medal']=='Gold']['Age'].dropna()
        
        if not gold_medal_ages.empty:  # Check if the list is not empty
            sport_gold_ages.append(gold_medal_ages)
            name.append(sport)

    return age_dist, sport_gold_ages, name

def athelete_weights_heights(df, sport):
    """
    Returns a DataFrame of athletes' weights and heights, optionally filtered by sport.

    Args:
        df (DataFrame): Input DataFrame containing athlete data.
        sport (str): Sport to filter by; use 'All' for no filter.

    Returns:
        DataFrame: DataFrame of athletes with weights and heights.
    """
    df_atheletes = df.drop_duplicates(subset=['Name','region'])
    df_atheletes['Medal'].fillna('No Medal', inplace = True)
    if sport == 'All':
        return df_atheletes
    df_atheletes = df_atheletes[df_atheletes['Sport'] == sport]
    return df_atheletes

def male_female_participation(df):
    """
    Returns a DataFrame of male and female participation counts by year.

    Args:
        df (DataFrame): Input DataFrame containing athlete data.

    Returns:
        DataFrame: DataFrame with counts of male and female participants per year.
    """
    male = df[df['Sex'] == 'M'][['Sex','Year']]
    male = male.groupby('Year').count().reset_index()
    male.rename(columns = {'Sex':'Male'},inplace = True)

    female = df[df['Sex'] == 'F'][['Sex','Year']]
    female = female.groupby('Year').count().reset_index()
    female.rename(columns = {'Sex':'Female'},inplace = True)

    male_female_count = male.merge(female, on='Year', how = 'left')
    male_female_count.fillna(0, inplace = True)

    return male_female_count






