import streamlit as st
import matplotlib.pyplot as plt

st.title( "Statistics Page")


st.write(f"In average, you need {st.session_state.stats_df['TotalGuesses'].mean()} guesses to guess the correct country!")
st.write(f"In average, you need {st.session_state.stats_df['Hints'].mean()} hints to guess the correct country!")
st.write(f"In average, you need {st.session_state.stats_df['Question'].mean()} questions to guess the correct country!")


st.session_state.stats_df.set_index('Country', inplace=True)
st.session_state.stats_df.plot()

plt.title("How many guesses did you need for which country?")
plt.xlabel("Country")
plt.ylabel("Guesses")
plt.show()


st.write(st.session_state.stats_df)




