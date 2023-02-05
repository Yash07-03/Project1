#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_white"
data = pd.read_csv("T-20 World cup.csv")
print(data.head())



# In[7]:


figure = px.bar(data, 
                x=data["winner"],
                title="Number of Matches Won by teams in t20 World Cup 2022")
figure.show()


# In[8]:


won_by = data["won by"].value_counts()
label = won_by.index
counts = won_by.values
colors = ['blue','lightgreen']

fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Number of Matches Won By Runs Or Wickets')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=32,
                  marker=dict(colors=colors, line=dict(color='white', width=5)))
fig.show()


# In[9]:


toss = data["toss decision"].value_counts()
label = toss.index
counts = toss.values
colors = ['skyblue','yellow']

fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Toss Decisions in T20 World Cup 2022')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=32,
                  marker=dict(colors=colors, line=dict(color='green', width=5)))
fig.show()


# In[10]:


figure = px.bar(data, 
                x=data["top scorer"], 
                y = data["highest score"], 
                color = data["highest score"],
                title="Top Scorers in T-20 World Cup 2022")
figure.show()


# In[12]:


figure = px.bar(data, 
                x = data["player of the match"], 
                title="Player of the Match Awards in T-20 World Cup 2022")
figure.show()


# In[13]:


figure = px.bar( data,
                x=data["best bowler"],
                title="Best Bowlers in T-20 World Cup 2022")
figure.show()


# In[14]:


fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["venue"],
    y=data["first innings score"],
    name='First Innings Runs',
    marker_color='green'
))
fig.add_trace(go.Bar(
    x=data["venue"],
    y=data["second innings score"],
    name='Second Innings Runs',
    marker_color='blue'
))
fig.update_layout(barmode='group', 
                  xaxis_tickangle=-45, 
                  yaxis_tickangle=0,
                  title="Best Stadiums to Bat First or Chase")
fig.show()


# In[15]:


fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["venue"],
    y=data["first innings wickets"],
    name='First Innings Wickets',
    marker_color='yellow'
))
fig.add_trace(go.Bar(
    x=data["venue"],
    y=data["second innings wickets"],
    name='Second Innings Wickets',
    marker_color='red'
))
fig.update_layout(barmode='group', 
                  xaxis_tickangle=-45, 
                  title="Best Statiums to Bowl First or Defend")
fig.show()


# In[16]:


figure = px.bar(data, 
                x=data["venue"],
                y=data["Stadium Capacity"],
                title="Biggest stadium in term of capacity")
figure.show()


# In[ ]:




