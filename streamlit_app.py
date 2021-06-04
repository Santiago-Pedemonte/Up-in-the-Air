import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image

import os
import requests
from dotenv import load_dotenv

import random
from web3 import Web3
import requests
import datetime
import json
from eth_account import Account

@st.cache(persist=True)
def load_data():
    data = pd.read_csv("Tweets.csv")
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

insurance_address = os.environ["INSURANCE_ACC"]
insurance_pk = os.environ["INSURANCE_PK"]
insurance_cost = 1900000000000000
insurance_account = Account.from_key(insurance_pk)

def uniqueid():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1

def create_raw_tx(account, recipient, amount):
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    gasEstimate = web3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": web3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": web3.eth.getTransactionCount(account.address),
    }


def send_tx(account, recipient, amount):
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    tx = create_raw_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return result.hex()


image = Image.open('airplane.jpg')

st.title("What's Up in the Air(line Industry)?")
st.image(image, caption='Airplane taking off from the airport. Image Credit: phaisarnwong2517')
st.markdown("This application is a dashboard that allows Users to locate real-time flights, view estimated departure/arrival times, whether or not a flight is delayed, and analyze public sentiment surrounding the airline industry through Tweets 🐦 ")

st.markdown("## Find Real-Time Flights (International and Domestic)")
departure_iata = st.text_input("Enter the 3-letter IATA code of the Airport you are departing from.", max_chars=3, type="default", help="The IATA code is a 3-letter code. For example, 'JFK' is John F. Kennedy International Airport")
arrival_iata = st.text_input("Please enter the IATA code of the Destination Airport.", max_chars=3, type="default", help="The IATA code is a 3-letter code. For example, 'JFK' is John F. Kennedy International Airport")

if st.button("Find Flights", key='55'):
    st.markdown("## FLIGHT DASHBOARD")
    st.text(f"Current Flights from {departure_iata} to {arrival_iata}")
    api_key = st.secrets["AVIATIONSTACK_API_KEY"]
    aviationstack_api = os.environ["AVIATIONSTACK_API_KEY"]
    aviationstack_url = 'http://api.aviationstack.com/v1/flights'
    params = {
  'access_key': aviationstack_api,
  'dep_iata': departure_iata,
  'arr_iata': arrival_iata,
}
    api_result = requests.get(aviationstack_url, params)
    api_response = api_result.json()
    for i in range(0, len(api_response['data'])-1):
        airline = api_response['data'][i]['airline']['name']
        est_departure = api_response['data'][i]['departure']['estimated'].split("T")
        departure_delay = api_response['data'][i]['departure']['delay']
        est_arrival = api_response['data'][i]['arrival']['estimated'].split("T")
        arrival_delay = api_response['data'][i]['arrival']['delay']
        flight = api_response['data'][i]['flight']['iata']
        
        st.text(f"Airline Name: {airline}")
        st.text(f"Flight IATA: {flight}")
        st.text(f"Est departure date and time: {est_departure[0]}:{est_departure[1].split('+')[0]}")
        st.text(f"Departure Delay:{departure_delay}")
        st.text(f"Est arrival date and time: {est_arrival[0]}:{est_departure[1].split('+')[0]}")
        st.text(f"Arrival Delay:{arrival_delay}")
        st.text("-----------------------------------------------------")
        
st.markdown("## Buy Insurance for Your Flight")
first_name = st.text_input("First Name", type="default")
last_name = st.text_input("Last Name", type="default")
ticket_num = st.text_input("Ticket #", type = 'default')
airline = st.text_input("Airline Code", max_chars=2, type="default", help="For example, American Airlines is 'AA'")
flight_num = st.text_input("Flight Number", max_chars=4, type="default", help="Enter the numbers listed after the airline code.")
flight_date = st.text_input("Date of Departure (Format: YYYY-MM-DD)", max_chars=10, type="default")
public_user = st.text_input("Public Address", max_chars = 42, value = '0x', type= 'default', help="ETH wallet address begins with 'Ox'.")
private_user = st.text_input("Private Key", max_chars = 64, type = 'default', help="To sign the transaction, enter your private key.")

if st.button("Buy Insurance", key='66'):

    account_temp = Account.from_key(private_user)
        
        # Placeholder to verify wallet credentials and pay for insurance.
    tx = send_tx(account_temp, insurance_address, insurance_cost)
        
    unique_sequence = uniqueid()
    claim_id = next(unique_sequence)
    user_temp = {
        "First Name": first_name,
        "Last Name": last_name,
        "Ticket #": ticket_num,
        "Flight": airline + flight_num,
        "Flight Date": flight_date,
        "Public Address": public_user,
        "Tx #": tx,
        "Claim ID": claim_id
        }
    user_json = json.dumps(user_temp)
        
    with open(f'{str(user_json[7])}.json', 'w') as json_file:
        json.dump(user_temp, json_file)
        
        
st.markdown("## Claim Your Insurance")

user_claim = st.number_input("Write down your claim ID")


if st.button("Claim Insurance", key = '77'):
    user_json = open(f'{str(user_claim)}.json', 'w')
    if user_json: # Need to compare claim id to some database.
        api_key = st.secrets["AVIATIONSTACK_API_KEY"]
        aviationstack_api = os.environ["AVIATIONSTACK_API_KEY"]
        aviationstack_url = 'http://api.aviationstack.com/v1/flights'
        params = {
          'access_key': aviationstack_api,
          'flight_date': user_json[4],
          'flight_status': 'landed',
          'flight_iata': user_json[3],
          'min_delay_arr': 60
        }
        api_result = requests.get(aviationstack_url, params)
        api_response = api_result.json()
        if api_result:
            delay = api_response['data'][i]['arrival']['delay']
            # Extract user's Public address from json, calculate payout, and send the transaction.
            amount_to_pay = (delay / 2) * 10000
            claim_tx = send_tx(insurance_account, user_json[5], amount_to_pay)
        else: print("No flights found.")
    else: print("Claim doesn't exist.")
              
st.sidebar.title("Taking a look at Tweets about U.S. Airlines")

st.sidebar.markdown("Use the dashboard to explore public sentiment about the airline industry.")

st.sidebar.subheader("View a random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of Tweets (Categorized by Sentiment)")
select = st.sidebar.selectbox('Visualization Type', ['Histogram', 'Pie Chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of Tweets by Sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)


st.sidebar.subheader("When and Where are Users Tweeting from?")
hour = st.sidebar.slider("Time of Day (In Military Time)", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Hide", True, key='1'):
    st.markdown("### Tweet Locations (based on the time of day)")
    st.markdown("%i Tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1) %24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown Airline Tweets by Sentiment")
choice = st.sidebar.multiselect('Pick Airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment',
    facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display Word Cloud for Which Sentiment?', ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("Hide", True, key='3'):
    st.header('Word Cloud for %s sentiment' %(word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
