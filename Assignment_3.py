import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

#Give the page a title
st.title("NBA: Politically or Player Performance Driven?")


#Read the dataframe 
nba_df = pd.read_csv('nba-players.csv')

#Create a version which we will be using without affecting the original dataframe
nba_df_new = nba_df.drop("Unnamed: 0", axis=1, inplace=False)


#Calculate the overall career minutes and add it as a new column
nba_df_new['Total Min'] = nba_df_new['gp'] * nba_df_new['min']

#Categorize the data into 2 dataframes, one for players with long career and another for players with short career
long_career = nba_df_new[nba_df_new['target_5yrs'] == 1]
short_career = nba_df_new[nba_df_new['target_5yrs'] == 0]

#View if their seems to be a relation between a players career length and the number of games played

# Short career histogram
short_career_hist = px.histogram(short_career, x="Total Min", nbins=7)
short_career_hist.update_layout(title = {"text": "Distribution of Total Minutes Played for Players with Short Career", "y": 0.95, "x":0.2})

#Remove the grid in the background of the histogram to reduce clutter
short_career_hist.update_xaxes(showgrid=False)
short_career_hist.update_yaxes(showgrid=False,title = "Number of Players")

st.plotly_chart(short_career_hist, use_container_width=True)

# Long career histogram
long_career_hist = px.histogram(long_career, x="Total Min", nbins=7, color_discrete_sequence=['indianred'])
long_career_hist.update_layout(title = {"text": "Distribution of Total Minutes Played for Players with Long Career", "y": 0.95, "x":0.2})

long_career_hist.update_xaxes(showgrid=False)
long_career_hist.update_yaxes(showgrid=False,title = "Number of Players")

st.plotly_chart(long_career_hist, use_container_width=True)


#Visualize the Offensive Performance of Players
min_games_played = nba_df_new['gp'].min()
max_games_played = nba_df_new['gp'].max()

# Interactive slider button
games_increase = st.slider("Increase Games Played by 10",min_value =min_games_played ,max_value = max_games_played,value = nba_df_new['gp'].min() )


# Filter data based on current games played
filtered_data = nba_df_new[nba_df_new['gp'] <= games_increase]
fig2 = px.scatter(filtered_data, x = 'gp', y = 'pts', labels = {'gp': "Games Played", 'pts': "Points per game"})
fig2.update_layout(title = {'text': "Relation b/w PPG and GP",'x': 0.4,'y': 0.95, 'font': {'size': 25}},xaxis_range=[min_games_played, max_games_played], yaxis_range = [0,30])


fig2.update_xaxes(showgrid=False)
fig2.update_yaxes(showgrid=False)
st.plotly_chart(fig2)

#Review Defensive and Offensive Performance of Players at the same time

#Define the metrics that will appear in the heatmap

#Allow the user to select any metrics they want to see to understand the players performance

#Create the dataframe based on the metrics the user chooses
x_column = st.selectbox("Select X variable:", nba_df_new.columns)
y_column = st.selectbox("Select Y variable:", nba_df_new.columns)


fig5 = px.scatter(nba_df_new, x=x_column, y=y_column, log_x=True)
fig5.update_layout(title = {'text':"Relation between {} and {}".format(x_column, y_column),'x': 0.4,'y': 0.95, 'font': {'size': 25}})
fig5.update_xaxes(showgrid=False)
fig5.update_yaxes(showgrid=False)

st.plotly_chart(fig5)

#View the whole table
st.dataframe(nba_df)