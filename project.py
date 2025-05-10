import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import streamlit as st
import scipy.stats as sci

dataset = pd.read_csv('ilidata.csv')
#dataset tracks influenze like illness (ILI) across US states over time

#plot ili data time series depending on the user selected state

st.title("ILI Statistical Characterizations By State")
project, readbutton = st.columns(spec = [0.8, 0.2], vertical_alignment = "bottom")
with project:
    st.subheader("Cheyenne Desmond - BSTA-040 Final")
with readbutton:
    st.link_button("About the Author", "https://github.com/chd428/chd428/blob/main/README.md")
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

st.markdown("Please select a state/location below:")
selstate = st.selectbox("state/location", states)

#def numweeks(epiweek):
    #adjustedweek = epiweek - startweek
    #return adjustedweek

statedata = dataset.loc[dataset["state"] == selstate]
startweek = statedata['epiweek'].iloc[0]
statedata = statedata[statedata['season'] != 'offseason']
#statedata = statedata.assign(Week=statedata["epiweek"].astype(int).apply(numweeks))
statedata['Week'] = range(len(statedata))
#print(statedata)

st.subheader("ILI Percentage Across All Epidemic Periods")
st.line_chart(statedata, y='ili',x='Week', color = "#FF0000")
st.caption("In the figure above, ILI percentage is shown for all weeks excluding off season for a given state. This shows peaks and lows for a selected state, and allows for a user to view trends in data.")


#histogram

fig,ax = plt.subplots(facecolor = '#f9f0f0')
mean = np.mean(statedata.ili)

if mean < 0:
    st.write("Error with dataset.")
else:
    ax.set_facecolor('#f9f0f0')
    lambdaval = 1 / mean
    st.subheader("Probability Distribution of ILI Percentage")
    count, bins, _ = ax.hist(statedata['ili'], bins = 50, density = True, color = 'red')
    xmin, xmax = 0, np.max(statedata['ili'])
    x = np.linspace(xmin, xmax, 200)
    y = sci.expon.pdf(x, loc = 0, scale = mean)
    ax.plot(x,y, color ='#410505', linestyle = "dashed")
    ax.set_xlabel("Percent ILI")
    ax.set_ylabel("Probability")
    st.pyplot(fig)
    st.caption("In the figure above, the probability distribution of ILI percentage is plotted on a histogram. These percentages can be seen in the 'ILI Percentage Across All Epidemic Periods' graph for cross reference. Each box in the histogram represents a distribution of ILI Percentage. The dotted line represents an exponential distribution curve. If the exponential distribution curve matches the general pattern of the histogram, it can be assumed that the probability ILI percentage follows an exponential distribution.")