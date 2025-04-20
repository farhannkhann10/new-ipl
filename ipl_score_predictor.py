# Import the libraries
import math
import numpy as np
import pickle
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(page_title='IPL Score Predictor 2022', layout="centered")

# Load the ML model
filename = 'ml_model.pkl.gz'
model = pickle.load(open(filename, 'rb'))

# Title of the page with custom CSS
st.markdown("<h1 style='text-align: center; color: white;'>IPL Score Predictor 2022</h1>", unsafe_allow_html=True)

# Background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://4.bp.blogspot.com/-F6aZF5PMwBQ/Wrj5h204qxI/AAAAAAAABao/4QLn48RP3x0P8Ry0CcktxilJqRfv1IfcACLcBGAs/s1600/GURU%2BEDITZ%2Bbackground.jpg");
        background-attachment: fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Description section
with st.expander("Description"):
    st.info("""A Simple ML Model to predict IPL Scores between teams in an ongoing match. To ensure the model provides a reasonably accurate score prediction, it requires a minimum of 5 overs to be completed.""")

# Team encoding
teams = ['Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 'Kolkata Knight Riders',
         'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']

# Batting team selection
batting_team = st.selectbox('Select the Batting Team', teams)

# Bowling team selection
bowling_team = st.selectbox('Select the Bowling Team', teams)

# Ensure different teams
if batting_team == bowling_team:
    st.error("Bowling and Batting teams should be different")

# Encoding teams using one-hot encoding
def encode_team(team_name):
    return [1 if team == team_name else 0 for team in teams]

# Form layout
col1, col2 = st.columns(2)

with col1:
    overs = st.number_input('Enter the Current Over (e.g., 5.3 for 5 overs and 3 balls)', min_value=5.1, max_value=19.5, value=5.1, step=0.1)
    if overs - math.floor(overs) > 0.5:
        st.error('Please enter valid over input as one over only contains 6 balls')

with col2:
    runs = st.number_input('Enter Current Runs', min_value=0, max_value=354, step=1, format='%i')

wickets = st.slider('Enter Wickets Fallen Till Now', 0, 9)

col3, col4 = st.columns(2)

with col3:
    runs_in_prev_5 = st.number_input('Runs Scored in the Last 5 Overs', min_value=0, max_value=runs, step=1, format='%i')

with col4:
    wickets_in_prev_5 = st.number_input('Wickets Fallen in the Last 5 Overs', min_value=0, max_value=wickets, step=1, format='%i')

# Prepare input features
if batting_team != bowling_team:
    prediction_array = []
    prediction_array.extend(encode_team(batting_team))
    prediction_array.extend(encode_team(bowling_team))
    prediction_array.extend([runs, wickets, overs, runs_in_prev_5, wickets_in_prev_5])
    prediction_array = np.array([prediction_array])

    # Predict button
    if st.button('Predict Score'):
        prediction = model.predict(prediction_array)
        predicted_score = int(round(prediction[0]))
        st.success(f'🏏 PREDICTED MATCH SCORE : {predicted_score - 5} to {predicted_score + 5}')
