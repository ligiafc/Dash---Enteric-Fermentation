#!/usr/bin/env python
# coding: utf-8

# # Plotly - Enteric Fermentation

# ## Importing Libraries

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px  
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output


# ## Loading Dataset

# - **Enteric Fermentation**

# In[2]:


ef = pd.read_csv("enteric_fermentation_countries.csv")


# In[3]:


ef.head()


# # Data Preparation

# In[4]:


ef.drop(["Domain","Source"],axis =1,inplace=True)


# In[5]:


for index in ef.index:
    if ef.loc[index,'Element']=='Stocks':
        ef.loc[index,'Heads'] =  ef.loc[index,'Value']
    if ef.loc[index,'Element']=='Emissions (CH4)':
        ef.loc[index,'Enteric CH4 Emissions (kt)'] =  ef.loc[index,'Value']


# In[6]:


ef = ef.drop(columns = ["Element","Unit","Value"])


# In[7]:


ef = ef.groupby(['Item','Year',"Area"], as_index = False).sum()


# In[8]:


ef = ef.rename(columns={"Item":"Animal","Area":"Country"})
ef.head(10)


# In[9]:


all_animals=ef.Animal.unique()
all_animals


# In[10]:


all_countries=ef.Country.unique()
all_countries


# ## Creating the Dash Components

# In[11]:


app = dash.Dash(__name__)


# In[12]:


app.layout = html.Div([
    
    html.H1("Methane Emissions from the Enteric Fermentation", style={"color":"white","backgroundColor":"green","text-align": "center"}),
    html.H2("Irish AgriBusiness and Top Countries Producers", style={"color":"white","backgroundColor":"green","text-align": "center"}),
    
    html.Br(),
    
    dcc.Checklist(
        id="animal_checklist",
        options=[{"label":x,"value":x} for x in all_animals],
        value="Cattle, dairy",
        labelStyle={"display":"inline=block"}
    ), 
    html.Br(),
    
    dcc.Checklist(
        id="country_checklist",
        options=[{"label":x,"value":x} for x in all_countries],
        value="Ireland",
        labelStyle={"display":"inline=block"}),
    
    dcc.Graph(id="line-chart",figure={}),
    
])                     


# In[13]:


ef.columns


# In[14]:


# Connect the Plotly graphs with Dash Components
@app.callback(
    Output("line-chart","figure"),
    Input("animal_checklist","value"),
    Input("country_checklist","value"))
    
def update_line_chart(animal_slct,country_slct):
    eff = ef[(ef.Animal.isin(animal_slct)) & (ef.Country.isin(country_slct))]
    fig = px.line(eff,x="Year",y="Enteric CH4 Emissions (kt)",color="Animal",symbol="Country",hover_data=["Heads","Country","Year","Enteric CH4 Emissions (kt)"])
    fig.update_layout(hovermode="y unified")
    return fig


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




