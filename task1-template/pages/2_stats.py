import streamlit as st
import matplotlib.pyplot as plt
import pandas as pdstre

st.title( "Statistics Page")


st.write(f"Average amount of guesses/inputs needed: {st.session_state.stats_df['TotalGuesses'].mean()}")
st.write(f"Average amount of hints needed:{st.session_state.stats_df['Hints'].mean()}")



# creating line chart (we do not know why it is sorted alphabetically)
st.line_chart(st.session_state.stats_df, x = 'Country', y = ['TotalGuesses','Hints'])


st.write(st.session_state.stats_df)
