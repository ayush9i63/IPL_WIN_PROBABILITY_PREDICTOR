import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Function to resize images
def resize_image(image_path, size=(150, 150)):
    img = Image.open(image_path)
    img = img.resize(size, Image.LANCZOS)  # Use LANCZOS for high-quality resizing
    return img

# Remove background image CSS
# No need for background styling since we are removing it

cols = st.columns(5)  # Change the number based on how many images you want in one line

# Place images in each column and use st.markdown for bold captions
with cols[0]:
    st.image(resize_image("C:\\Users\\harid\\PycharmProjects\\AppIPL\\CSK Logo.png"))
    st.markdown('<p style="font-weight: bold; color: black;">IPL Logo</p>', unsafe_allow_html=True)

with cols[1]:
    st.image(resize_image("C:\\Users\\harid\\PycharmProjects\\AppIPL\\Delhi Capitals Logo.jpg"))
    st.markdown('<p style="font-weight: bold; color: black;">Chennai Super Kings</p>', unsafe_allow_html=True)

with cols[2]:
    st.image(resize_image("C:\\Users\\harid\\PycharmProjects\\AppIPL\\Mumbai Indians Logo.jpg"))
    st.markdown('<p style="font-weight: bold; color: black;">Delhi Capitals</p>', unsafe_allow_html=True)

with cols[3]:
    st.image(resize_image("C:\\Users\\harid\\PycharmProjects\\AppIPL\\RCB Logo.png"))
    st.markdown('<p style="font-weight: bold; color: black;">Royal Challengers Bengaluru</p>', unsafe_allow_html=True)

# with cols[4]:
#     st.image(resize_image("C:\\Users\\harid\\PycharmProjects\\AppIPL\\AppIPL.iml"))
#     st.markdown('<p style="font-weight: bold; color: black;">Mumbai Indians</p>', unsafe_allow_html=True)

# Teams and Cities List
teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

# Load pre-trained model
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Streamlit Title using markdown for custom formatting
st.markdown('<h1 style="font-weight: bold; color: black;">IPL Win Predictor</h1>', unsafe_allow_html=True)

# Layout for team selections with bold labels using st.markdown
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('**Select the batting team**', sorted(teams))

with col2:
    bowling_team = st.selectbox('**Select the bowling team**', sorted(teams))

# Check if the selected teams are the same
if batting_team == bowling_team:
    st.warning("**Please select different teams for batting and bowling.**")

# Host city selection
selected_city = st.selectbox('**Select host city**', sorted(cities))

# Target input (max 721)
target = st.number_input('**Target (Max: 721)**', min_value=1, max_value=721, step=1, format='%d')

# Inputs for current score, overs completed, and wickets out
col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('**Score (Compulsory)**', min_value=0, step=1, format='%d')

with col4:
    overs = st.number_input('**Overs completed (Max: 20, Compulsory)**', min_value=0, max_value=20, step=1, format='%d')

with col5:
    wickets = st.number_input('**Wickets out (Max: 10, Compulsory)**', min_value=0, max_value=10, step=1, format='%d')

# Prediction button without unsafe_allow_html
if st.button('Predict Probability'):
    # Ensure batting and bowling teams are different
    if batting_team == bowling_team:
        st.warning("**Please select different teams for batting and bowling.**")
    # Ensure all fields are filled correctly
    elif target is None or score is None or overs is None or wickets is None:
        st.warning("**All fields are compulsory. Please enter all required values.**")
    elif score > target + 5:
        st.warning(f"**The score cannot exceed {target + 5}. Please enter a valid score.**")
    elif overs > 20:
        st.warning("**Overs completed cannot exceed 20. Please enter a valid number of overs.**")
    elif wickets < 0 or wickets > 10:
        st.warning("**Wickets out must be between 0 and 10.**")
    else:
        # Check if the batting team has successfully chased the target
        if target <= score <= target + 5:
            if wickets < 10:
                st.success(f"**{batting_team} has successfully chased the target of {target} runs!**")
            else:
                st.warning("**Wickets out should be less than 10 after chasing the target.**")
        else:
            if wickets == 10 or overs == 20:
                if score < target:
                    st.success(f"**{bowling_team} has won the match!**")
                elif score == target:
                    st.success("**Match tied!**")
            else:
                runs_left = target - score
                balls_left = 120 - (overs * 6)
                wickets_left = 10 - wickets
                crr = score / overs if overs > 0 else 0
                rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

                input_df = pd.DataFrame({
                    'batting_team': [batting_team],
                    'bowling_team': [bowling_team],
                    'city': [selected_city],
                    'runs_left': [runs_left],
                    'balls_left': [balls_left],
                    'wickets': [wickets_left],
                    'total_runs_x': [target],
                    'crr': [crr],
                    'rrr': [rrr]
                })

                result = pipe.predict_proba(input_df)
                loss = result[0][0]
                win = result[0][1]

                st.header(f"**{batting_team} - {round(win * 100)}%**")
                st.header(f"**{bowling_team} - {round(loss * 100)}%**")

                labels = [batting_team, bowling_team]
                sizes = [win * 100, loss * 100]
                colors = ['gold', 'lightcoral']
                explode = (0.1, 0)

                fig, ax = plt.subplots()
                ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                       autopct='%1.1f%%', shadow=True, startangle=140)
                st.pyplot(fig)

# Display your name with larger font size and bold
st.markdown("<h3 style='text-align: center; font-size: 24px; font-weight: bold;'>Krishna Dutt Ojha</h3>", unsafe_allow_html=True)

# Add logos for LinkedIn and GitHub with profile mentions
col1, col2 = st.columns([1, 1])  # Create two equal columns
with col1:
    st.markdown('<a href="https://www.linkedin.com/in/krishna6399/" target="_blank">'
                '<img src="https://cdn.worldvectorlogo.com/logos/linkedin-icon.svg" '
                'style="width: 30px; height: 30px;"></a> **My LinkedIn Profile**', unsafe_allow_html=True)

with col2:
    st.markdown('<a href="https://github.com/ayush9i63" target="_blank">'
                '<img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" '
                'style="width: 30px; height: 30px;"></a> **My GitHub Profile**', unsafe_allow_html=True)
