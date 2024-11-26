import streamlit as st
import pandas as pd
import random

st.title("Country Guessr")

st.subheader("How to play")

st.write("I am thinking of a country. You have to guess which country it is. You can ask me questions to help you guess the country. You can also ask for hints.")

#use cache to only load the data once
@st.cache_data
def load_countries():
    df = pd.read_csv(r'C:\Users\auris\Downloads\world-data-2023.csv')
    return df

countries = load_countries()

@st.cache_data
def get_random_country():
    random_index = random.randint(0, len(countries) - 1)
    random_country = countries.iloc[random_index]['Country']
    return random_country
    
st.write("Solution: ", get_random_country())

question = st.text_input("Ask me a question")

