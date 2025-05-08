'''BSTA040 Final'''
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import streamlit as st
import scipy.stats as sci

dataset = pd.read_csv('ilidata.csv')
#dataset tracks influenze like illness (ILI) across US states over time

#plot ili data time series depending on the user selected state

st.title("ILI Statistical Characterizations By State")
st.subheader("BSTA-040 Final")
st.markdown("Visualize **Influenza-Like-Illness** (ILI) and its probability distribution across a time period of 15 years (2010 - 2025) for a number of locations across the US.")

with st.expander("Key info for understanding dataset + graphs", icon = "❓"):
    st.write("This dataset tracks influenza-like illness (ILI) across U.S. states over time.")
    st.write()
    st.markdown("Important descriptions for understanding data: ")
    col1, col2 = st.columns(spec = [0.3, 0.7], vertical_alignment = "bottom")
    with col1:
        st.markdown(''':red[**ILI**]''')
        st.markdown(''':red[**%ILI**]''')
        st.markdown(''':red[**Week**]''')
        st.markdown(''':red[**State**]''')  
    with col2:
        st.markdown("Influenza-Like-Illness")
        st.markdown("Unweighted # ILI / total hospital visits x 100")
        st.markdown("The week an observation was tracked (skipping offweeks)")
        st.markdown("State/location picked by user detailing area observed.")
    
states = dataset.state.unique()

selstate = st.selectbox("Select a state", states)

def numweeks(epiweek):
    adjustedweek = epiweek - startweek
    return adjustedweek

statedata = dataset.loc[dataset["state"] == selstate]
startweek = statedata['epiweek'].iloc[0]
for i in statedata:
    if statedata['season'] == 'offweek':
        statedata.drop(i)
    statedata = statedata.assign(Week=statedata["epiweek"].astype(int).apply(numweeks))
#print(statedata)
st.line_chart(statedata, y='ili',x='Week', color = "#FF0000")



#histogram

fig,ax = plt.subplots(facecolor = '#f9f0f0')
mean = np.mean(statedata.ili)

if mean < 0:
    st.write("Error with dataset.")
else:
    ax.set_facecolor('#f9f0f0')
    lambdaval = 1 / mean
    count, bins, _ = ax.hist(statedata['ili'], bins = 50, density = True, color = 'red')
    xmin, xmax = 0, np.max(statedata['ili'])
    x = np.linspace(xmin, xmax, 200)
    y = sci.expon.pdf(x, loc = 0, scale = mean)
    ax.plot(x,y, color ='#410505', linestyle = "dashed")
    st.pyplot(fig)
