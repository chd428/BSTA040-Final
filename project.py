'''BSTA040 Final'''
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import streamlit as st

dataset = pd.read_csv('ilidata.csv')
#dataset tracks influenze like illness (ILI) across US states over time
#
#plot ili data time series depending on the user selected state


states = dataset.state.unique()

selstate = st.selectbox("Select a state", states)

def numweeks(epiweek):
    adjustedweek = epiweek - dataset.epiweek[0]
    return adjustedweek

statedata = dataset.loc[dataset["state"] == selstate]
statedata = statedata.assign(Week=statedata["epiweek"].astype(int).apply(numweeks))
#print(statedata)

st.line_chart(statedata, y='ili',x='Week')
fig,ax = plt.subplots()
#ax.plot((statedata['ili']))
#plt.show()
ax.hist(statedata['ili'], bins = 50)