#!/usr/bin/env python
# coding: utf-8

# importing the necessary packages
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np



# reading the necessary CSV files into dataframes
df_nba_data = pd.read_csv("NBA_Team_Data.csv")
df_misc_data = pd.read_csv("NBA_Team_Miscellaneous_Data.csv")






# this is creating the effective field goal percentage, 
# turnover percentage, and free throw factor columns in the dataframe
EFG_percent = (df_nba_data['FG'] + 0.5 * df_nba_data['3P']) / df_nba_data['FGA']
df_nba_data['eFG%'] = EFG_percent

TOV_percent = df_nba_data['TOV'] / (df_nba_data['FGA'] + 0.44 * df_nba_data['FTA'] + df_nba_data['AST']                                     + df_nba_data['TOV'])
df_nba_data['TOV%'] = TOV_percent

FT_factor = df_nba_data['FT'] / df_nba_data['FGA']
df_nba_data['FTF'] = FT_factor



# this is dropping the unneeded columns in the first dataframe 
dropping_nba_columns = ['Rk', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT',                         'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']
df_nba_data = df_nba_data.drop(dropping_nba_columns, axis=1)



# creating a win percentage column in the second dataframe using wins and losses
win_pct = df_misc_data['W'] / (df_misc_data['W'] + df_misc_data['L'])
df_misc_data['WPCT'] = win_pct




# this is dropping the unneeded columns in the second dataframe  
dropping_misc_columns = ['Rk', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'TS%',                     'eFG%', 'TOV%', 'FT/FGA', 'eFG%.1', 'TOV%.1', 'FT/FGA.1', 'Arena', 'Attend.', 'Attend./G']
df_misc_data = df_misc_data.drop(dropping_misc_columns, axis=1)



# merging the two dataframes together by Team
df_all_team_stats = pd.merge(df_nba_data, df_misc_data, on='Team')

# sorting the values in ascending order by win percentage
df_all_team_stats = df_all_team_stats.sort_values(by='WPCT', ascending=True)

# this creates a variable for league average stats
league_avg_stats = df_all_team_stats.iloc[30]

# this drops the league average stats from the dataframe
df_all_team_stats = df_all_team_stats.drop(df_all_team_stats.index[[30]])


# Now we define separate dataframes for the NBA Team and their 
# statistical category, while also making the Team name the index each time

df_pts = df_all_team_stats.melt(id_vars=['Team'], value_vars=['PTS'])
df_pts = df_pts.drop('variable', axis=1)
df_pts = df_pts.rename(columns={'value': 'Points Per Game'})
df_pts = df_pts.set_index('Team')

df_efg = df_all_team_stats.melt(id_vars=['Team'], value_vars=['eFG%'])
df_efg = df_efg.drop('variable', axis=1)
df_efg = df_efg.rename(columns={'value': 'Effective Field Goal Percentage'})
df_efg = df_efg.set_index('Team')

df_tov = df_all_team_stats.melt(id_vars=['Team'], value_vars=['TOV%'])
df_tov = df_tov.drop('variable', axis=1)
df_tov = df_tov.rename(columns={'value': 'Turnover Percentage'})
df_tov = df_tov.set_index('Team')

df_ftf = df_all_team_stats.melt(id_vars=['Team'], value_vars=['FTF'])
df_ftf = df_ftf.drop('variable', axis=1)
df_ftf = df_ftf.rename(columns={'value': 'Free Throw Factor'})
df_ftf = df_ftf.set_index('Team')

df_nrtg = df_all_team_stats.melt(id_vars=['Team'], value_vars=['NRtg'])
df_nrtg = df_nrtg.drop('variable', axis=1)
df_nrtg = df_nrtg.rename(columns={'value': 'Net Rating'})
df_nrtg = df_nrtg.set_index('Team')

df_orb = df_all_team_stats.melt(id_vars=['Team'], value_vars=['ORB%'])
df_orb = df_orb.drop('variable', axis=1)
df_orb = df_orb.rename(columns={'value': 'Offensive Rebounding Percentage'})
df_orb = df_orb.set_index('Team')

df_drb = df_all_team_stats.melt(id_vars=['Team'], value_vars=['DRB%'])
df_drb = df_drb.drop('variable', axis=1)
df_drb = df_drb.rename(columns={'value': 'Defensive Rebounding Percentage'})
df_drb = df_drb.set_index('Team')

# the header of the dashboard
st.write('NBA Team Statistics Graphed in Ascending Order of Wins', fontsize=50)


# giving the user a choice of which plot to look at
choice = st.selectbox("Which graph of team stats would you like to see?", \
                      ('Points Per Game', 'Effective Field Goal Percentage', \
                       'Turnover Percentage', \
                       'Free Throw Factor (Free Throws Made / Field Goal Attempts)', \
                       'Net Rating', 'Offensive Rebounding Percentage', \
                       'Defensive Rebounding Percentage'), index=0)

# making the if statements for what the user selects
if choice == 'Points Per Game':
    df_pts.plot()
    plt.gcf().set_size_inches(10,10)
    plt.title('Points Per Game of Every Team in the NBA, in Ascending Order of Wins', fontsize=14)
    plt.xticks(np.arange(30), (df_pts.index),rotation=90)
    plt.ylabel('Points Per Game', fontsize=10)
    plt.xlabel('Team (* Indicates a Playoff Team)', fontsize=10)
    st.pyplot(plt.gcf())
    st.write(df_pts)
    

if choice == 'Effective Field Goal Percentage':
    df_efg.plot()
    plt.gcf().set_size_inches(10,10)
    plt.title('Effective Field Goal Percentage of Every Team in the NBA, in Ascending Order of Wins', fontsize=14)
    plt.xticks(np.arange(30), (df_efg.index),rotation=90)
    plt.ylabel('Effective Field Goal Percentage', fontsize=10)
    plt.xlabel('Team (* Indicates a Playoff Team)', fontsize=10)
    st.pyplot(plt.gcf())
    st.write(df_efg)

if choice == 'Turnover Percentage':
    df_tov.plot()
    plt.gcf().set_size_inches(10,10)
    plt.title('Turnover Percentage of Every Team in the NBA, in Ascending Order of Wins', fontsize=14)
    plt.xticks(np.arange(30), (df_tov.index),rotation=90)
    plt.ylabel('Turnover Percentage', fontsize=10)
    plt.xlabel('Team (* Indicates a Playoff Team)', fontsize=10)
    st.pyplot(plt.gcf())
    st.write(df_tov)

if choice == 'Free Throw Factor (Free Throws Made / Field Goal Attempts)':
    df_ftf.plot()
    plt.gcf().set_size_inches(10,10)
    plt.title('Free Throw Factor of Every Team in the NBA, in Ascending Order of Wins', fontsize=14)
    plt.xticks(np.arange(30), (df_ftf.index),rotation=90)
    plt.ylabel('Free Throw Factor (Free Throws Made / Field Goal Attempts)', fontsize=10)
    plt.xlabel('Team (* Indicates a Playoff Team)', fontsize=10)
    st.pyplot(plt.gcf())
    st.write(df_ftf)

if choice == 'Net Rating':
    df_nrtg.plot()
    plt.gcf().set_size_inches(10,10)
    plt.title('Net Rating of Every Team in the NBA, in Ascending Order of Wins', fontsize=14)
    plt.xticks(np.arange(30), (df_nrtg.index),rotation=90)
    plt.ylabel('Net Rating', fontsize=10)
    plt.xlabel('Team (* Indicates a Playoff Team)', fontsize=10)
    st.pyplot(plt.gcf())
    st.write(df_nrtg)

if choice == 'Offensive Rebounding Percentage':
    df_orb.plot()
    plt.gcf().set_size_inches(10,10)
    plt.title('Offensive Rebounding Percentage of Every Team in the NBA, in Ascending Order of Wins', fontsize=14)
    plt.xticks(np.arange(30), (df_orb.index),rotation=90)
    plt.ylabel('Offensive Rebounding Percentage', fontsize=10)
    plt.xlabel('Team (* Indicates a Playoff Team)', fontsize=10)
    st.pyplot(plt.gcf())
    st.write(df_orb)

if choice == 'Defensive Rebounding Percentage':
    df_drb.plot()
    plt.gcf().set_size_inches(10,10)
    plt.title('Defensive Rebounding Percentage of Every Team in the NBA, in Ascending Order of Wins', fontsize=14)
    plt.xticks(np.arange(30), (df_drb.index),rotation=90)
    plt.ylabel('Defensive Rebounding Percentage', fontsize=10)
    plt.xlabel('Team (* Indicates a Playoff Team)', fontsize=10)
    st.pyplot(plt.gcf())
    st.write(df_drb)


# links
st.write('The original data comes from NBA reference, with the link here: https://www.basketball-reference.com/leagues/NBA_2020.html')
st.write('To view the python script and written report in Deepnote, use the link here: https://deepnote.com/publish/25c09a60-88c7-4b10-a6d8-d4f0e19605ae')
st.write('To view the Github repository, use the link here: https://github.com/nkomarovsky/MA346_Final_Project_NBA_Data.git')



