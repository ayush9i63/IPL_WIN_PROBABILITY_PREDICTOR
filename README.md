# IPL Win Predictor

The **IPL Win Predictor** is a web application built using **Streamlit** to predict the probability of a team's victory in an IPL match based on various parameters like target score, current score, overs completed, and wickets lost. The app uses a pre-trained machine learning model for predictions and provides a user-friendly interface for IPL enthusiasts.

## Features
- **Team Selection**: Choose the batting and bowling teams from a dropdown menu.
- **Host City Selection**: Select the city where the match is being played.
- **Match Details**: Input the target score, current score, overs completed, and wickets lost.
- **Predictions**: Get probabilities of winning for both teams.
- **Visualization**: Pie chart representation of winning probabilities.
- **Error Handling**: Validates user inputs to ensure correctness.
- **Dynamic Display**: Displays IPL team logos and app branding.

## Technologies Used
- **Streamlit**: For creating the web application interface.
- **Python Libraries**: 
  - `pickle` for loading the pre-trained machine learning model.
  - `Pandas` for handling input data.
  - `Matplotlib` for visualizing results.
  - `Pillow` for image processing.

## Prerequisites
- **Python Version**: Python 3.8 or later.
- **Required Python Libraries**:
  ```bash
  pip install streamlit pandas matplotlib pillow
