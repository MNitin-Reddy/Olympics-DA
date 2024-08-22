import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff

import preprocessor
import helper
import plot_configs

# import the .csv files
df = pd.read_csv(r'athlete_events.csv')
df_region = pd.read_csv(r'noc_regions.csv')

df = preprocessor.preprocess(df,df_region)

# setting page configuration
st.set_page_config(
    page_title="Olympic Analysis App",
    page_icon=":sports_medal:",
    layout="wide",
    initial_sidebar_state="expanded"
)

#st.sidebar.title('Summer Olympics Analysis')
st.sidebar.markdown('<h1 style="font-size: 32px" >Summer Olympics Analysis</h1>', unsafe_allow_html=True)
st.sidebar.image('olympic_logo.png')

# Menu to select the analysis
menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Country-wise Analysis','Athelete-wise Analysis','Overall Analysis')
)

st.markdown(
    """<style>
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 22px;
div[class*="st-emotion-cache-fm8pe0 e1nzilvr4"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 20px;
}
    </style>
    """, unsafe_allow_html=True)



if menu == 'Medal Tally':
    st.sidebar.header(':violet[Medal Tally]')
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',country)

    medals = helper.fetch_medals(df, selected_year,selected_country)

    if selected_year == 'All' and selected_country=='All':
        st.title(':violet[Overall Medal Tally]')
    if selected_year != 'All' and selected_country=='All':
        st.title(':violet[Medal Tally in Year:] '+ 'str(selected_year)')
    if selected_year == 'All' and selected_country !='All':
        st.title(selected_country+'\'s overall performance')
    if selected_year != 'All' and selected_country !='All':
        st.title(selected_country+'\'s performance in year '+str(selected_year))
    
    st.table(medals)

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# 1. Overall Anlysis option

if menu == 'Overall Analysis':
    st.title(':violet[Overall Analysis]')

    editions = df[ 'Year']. unique().shape [0]
    cities = df[ 'City'].unique().shape[0]
    sports = df[ 'Sport' ].unique().shape[0] 
    events = df[ 'Event'].unique().shape[0]
    athletes = df[ 'Name'].unique().shape[0]
    nations = df[ 'region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)
# --------------------------------------------------------------------------------------------------
    # Nations particiaption over the Years
    st.title("Nations participation over the years")

    nations_participation_over_years = helper.data_over_time(df,'region')

    fig = px.line(nations_participation_over_years, x='Year', y='count',)
    fig = plot_configs.update_plot_layout(fig,'Year','No. of participants')
    
    st.plotly_chart(fig)
# --------------------------------------------------------------------------------------------------
    # Number of events conducted in each year
    st.title("Events count over the years")
    events_over_years = helper.data_over_time(df,'Event')

    fig = px.line(events_over_years, x='Year', y='count',)
    fig = plot_configs.update_plot_layout(fig,'Year','No. of Events')
    
    st.plotly_chart(fig)
# --------------------------------------------------------------------------------------------------
    # Particiaption of atheletes 
    st.title("Participation of Atheletes over the years")

    athletes_over_years = helper.data_over_time(df,'Name')

    fig = px.line(athletes_over_years, x='Year', y='count')
    fig = plot_configs.update_plot_layout(fig,'Year','No. of Atheletes participated')

    st.plotly_chart(fig)
# --------------------------------------------------------------------------------------------------
    # HEatmap of how many sports are being considered in each event over the years
    st.title('No. of Events over time(Every sport)')
    sports = helper.sport_events(df)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(sports, annot = True)
    st.pyplot(fig)
# --------------------------------------------------------------------------------------------------
    # list og most popualar atheletes based on medals won
    st.title('Most Popular Atheletes')

    sport_list = helper.get_sports_list(df)
    selected_sport = st.selectbox('Select a sport', sport_list)

    popular_athl = helper.most_popular(df,selected_sport)

    st.table(popular_athl)
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# Country Wise Analysis

if menu == 'Country-wise Analysis':
    st.title(':violet[Country-wise Analysis]')

    st.sidebar.title('Country-wise Analysis')

    _,country_list = helper.country_year_list(df)

    country_list.pop(0) # helper.country_year_list return an 'All' option  which is not needed here.
    country_list.insert(0,'USA') # Set 'USA' as the initial parameter for country-wise analysis.

    selected_region = st.sidebar.selectbox('Select a country', country_list)

    region_medals = helper.regional_medals(df,selected_region)

    st.title(selected_region+'\'s Medals count over the years')

    fig = px.line(region_medals, x='Year', y='Medal')
    fig = plot_configs.update_plot_layout(fig,'Year','Medals won')

    st.plotly_chart(fig)
# --------------------------------------------------------------------------------------------------
    # medals won in each sport by a specific region/country
    st.title(selected_region+'\'s Medals won in each sport over the years')

    sport_region_pivot = helper.sports_region(df,selected_region)

    # if sport_region_pivot is empty it raises and error and won't display the plot
    # we use if else statements to not try to plot when dataframe is empty
    if len(sport_region_pivot)!=0:
        fig,ax = plt.subplots(figsize=(20,20))
        ax = sns.heatmap(sport_region_pivot, annot = True)
        st.pyplot(fig)
    else:
        st.write(selected_region+' hasn\'t won any medals yet')
# --------------------------------------------------------------------------------------------------
    # top 10 atheletes of that region/country
    st.title(selected_region+'\'s top 10 atheletes')

    top_atheletes = helper.top_10_region(df,selected_region)

    st.table(top_atheletes)
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

# Athelete wise Analysis

if menu == 'Athelete-wise Analysis':
    st.title(':violet[Athelete-wise Analysis]')

    # Distribution is athelete ages based on Gold, Silver and Bronze medalists
    st.title('Distribution of Age')

    ages, sport_gold_ages, name = helper.athelete_ages(df)
    fig = ff.create_distplot(ages,['Overall Age Distribution','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig = plot_configs.update_displot_layout(fig,'Age','Density')

    st.plotly_chart(fig)

# --------------------------------------------------------------------------------------------------
    # Age distribution based on sport played
    st.title('Distribution of Age based on sport')

    fig = ff.create_distplot(sport_gold_ages,name,show_hist=False,show_rug=False)
    fig = plot_configs.update_displot_layout(fig,'Age','Density')

    st.plotly_chart(fig)
# --------------------------------------------------------------------------------------------------
    # Male_Female weight and height distributions plot
    st.title('Height-Weight Distribution')

    sport_list = helper.get_sports_list(df)
    selected_sport = st.selectbox('Select a sport', sport_list)

    H_W_dist = helper.athelete_weights_heights(df, selected_sport)

    plt.figure(figsize = (15,20))
    fig = px.scatter(H_W_dist, x="Weight", y="Height", color="Medal", 
                    facet_col = 'Sex' ,title="Scatter Plot",
                    color_discrete_map={
                        'No Medal':'#5B97CA',
                        'Gold': '#FFDC73',
                        'Silver': '#DCDCDC',
                        'Bronze': '#7F6244'
                        }  
                    )
    fig = plot_configs.update_scatter_plot(fig)

    st.plotly_chart(fig)
# --------------------------------------------------------------------------------------------------
    # How male and female participation changed over the years
    st.title('Male-Female participation over the years')

    M_F_count = helper.male_female_participation(df)

    fig = px.line(M_F_count, x='Year', y=['Male','Female'])
    fig = plot_configs.update_plot_layout(fig,'Year','Participation_count')
    # Update traces to set colors for the lines
    fig.update_traces(line=dict(color='#1f77b4'), selector=dict(name='Male'))
    fig.update_traces(line=dict(color='#ff7f0e'), selector=dict(name='Female'))

    st.plotly_chart(fig)
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

    


