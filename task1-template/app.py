import streamlit as st
import pandas as pd
import random
from openai import OpenAI

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Country Guesser")
st.image("https://tse4.mm.bing.net/th?id=OIP.4cXjNUsskNTDylthxHqMFwHaDq&pid=Api")
#i think keys get blocked if they are on github
key = st.text_input("Please put your OpenAI key here")


#making it look like its from chat bot
with st.chat_message("assistant"):
    st.write("Helloooo! \nI am thinking of a country. You have to guess which country it is. You can ask me questions to help you guess the country. You can also ask for hints.")

#use cache to only load the data once
@st.cache_data
def load_countries():
    df = pd.read_csv('world-data-2023.csv')
    return df
countries = load_countries()

#defining the guessing goal
def get_random_country():
    random_index = random.randint(0, len(countries) - 1)
    random_country = countries.iloc[random_index]['Country']
    return random_country

#storing goal in session
if 'country_to_guess' not in st.session_state:
    st.session_state.country_to_guess = get_random_country()


#storing stats in session
if 'hint_number' not in st.session_state:
    st.session_state.hint_number = 0
if 'question_number' not in st.session_state:
    st.session_state.question_number = 0
if 'total_number' not in st.session_state:
    st.session_state.total_number = 0

if 'stats_df' not in st.session_state:
    st.session_state.stats_df = pd.DataFrame({'Country': [], 'TotalGuesses': [], 'Hints': [], 'Question': []})




#st.write("Solution: ", st.session_state.country_to_guess)



#adding the chat history to be able to put in the prompt
chat_history_string = "\n".join(st.session_state.chat_history)

#Prompt gpt-4o-mini
template = f"You are playing a guessing game with a user. You act as the game master who thought of a country. The country to be guessed is {st.session_state.country_to_guess}. The user will ask you questions about the country and you will answer them. If the user input is not related to the game you kindly inform them that you can only answer questions about the country. If they make a false guess you tell them that this is not the right answer. Please always be polite and eloquent. You will evalute the users guesses or questions. That means if they ask general questions early in the game, like: Is the country in Africa? or: what is the official language of the country? You will praise their question. If they guess without having much information you will kindly encourage them to start with more generell questions and they should slowly try to narrow down the country they are supposed to guess. But if they guess a country that is really close to {st.session_state.country_to_guess} you tell them that they are really close. Your chat history with the user is: {chat_history_string}"  
template_2 = f"I set up a game. The goal of the game is to guess the right country. You will know the answer and act as game master. The answer is {st.session_state.country_to_guess}. I do not know the answer. Refer to the counry in the answer as 'The Country I am thinking of'. There are three types of questionning allowed. The first one is a hint. You will state a fact about the country, if asked for a hint. When stating the hint, your answer should start with: 'Hint: '. The second possible question/statement is a guess for the right solution. If the country is guessed correctly, your output is 'Congratulations! Your guessed the country correctly!'. If the country is not guessed correctly, your answer begins with 'Your answer is incorrect!'. After this give an evaluation how far the stated guess is away from the answer. The third possible question is a question that narrows the scope of the guesser. The answer should begin with 'Fact: ' and then state the correct answer to the question about the country while not revealing the name of the country. If the stated question do not pass as one of this three types of question or the question is not about finding the country, then nicely state that the goal of the game is to find the right country. Your chat history with the user is: {chat_history_string}"

#setting up guesser's input
message = st.chat_input("Ask me a question about a country or give a guess :)")

#setting up OpenAi API
client = OpenAI(api_key = key)
model = "gpt-4o-mini"

#setup of chat feature
if message:
    chat_completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": template_2 + "The users newest input: " + message},
        ],
    )

    with st.chat_message("assistant"):
        st.markdown(chat_completion.choices[0].message.content)

    # appending the chat to chat history
    st.session_state.chat_history.append(f"User: {message}")
    st.session_state.chat_history.append(f"Your answer: {chat_completion.choices[0].message.content}")
    
    #counting guesses/inputs for stats
    st.session_state.total_number = st.session_state.total_number + 1


    #counting and evaluating various scenarios
    if chat_completion.choices[0].message.content[0:25] == "Your answer is incorrect!":
        #AURELIO HERE , pull the guessed country out of user message to evaluate the guess
        guessed_country = client.chat.completions.create( model=model, messages=[ {"role": "user", "content": f"Give me the name of the country the user incorrectly guessed in this conversation: {message}. The answer can not possibly be: {st.session_state.country_to_guess} The answer only consists of the name of the country. Possible country names are {countries['Country']}." },],)
        st.write(guessed_country.choices[0].message.content)
    if chat_completion.choices[0].message.content[0:5] == "Fact:":
        st.session_state.question_number = st.session_state.question_number + 1

    if chat_completion.choices[0].message.content[0:5] == "Hint:":
        st.session_state.hint_number = st.session_state.hint_number + 1
    
    if chat_completion.choices[0].message.content[0:15] == "Congratulations":
        st.write("Number of hints: ", st.session_state.hint_number)
        st.write("Number of questions: ", st.session_state.hint_number)
        st.write("Total guesses: ", st.session_state.total_number)

        #giving the number og guesses to a statistics dataframe
        new_row = pd.DataFrame({'Country': [st.session_state.country_to_guess], 'TotalGuesses': [st.session_state.total_number], 'Hints': [st.session_state.hint_number], 'Question': [st.session_state.hint_number]})
        st.session_state.stats_df = pd.concat([st.session_state.stats_df, new_row], ignore_index=True)


        #resetting game if guess is correct
        st.session_state.total_number = 0
        st.session_state.hint_number = 0
        st.session_state.hint_number = 0
        st.session_state.country_to_guess = get_random_country()

        with st.chat_message("assistant"):
            st.write("Oh, I thougtht of another country rigth now, try to guess it!")





#looking for the answer
#st.write("Solution: ", st.session_state.country_to_guess)
#myenv\Scripts\activate
#pip install -r requirements.txt





        