# imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# loading the dataset
df = pd.read_csv('calories.csv') # source: https://www.kaggle.com/datasets/ruchikakumbhar/calories-burnt-prediction/data
df = df.set_index('User_ID')

def model():
    # creating a linear regression model with Sklearn
    # variables
    X = np.array(df['Duration'])
    X = X.reshape(-1, 1) 
    y = df['Calories']

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # model 
    model = LinearRegression()
    model.fit(X_train, y_train)

    # score
    score = model.score(X_test, y_test)
    
    return model, score

def app(model, model_score):
    # interface with streamlit
    st.set_page_config(page_title='Calories Prediction')
    st.markdown("Hey, I'm Leo. I'm a 17-year-old programmer currently building my knowledge in **AI and Data Science**. I developed this project to practice what I learned in my Data Science introdutory course, working with **Pandas, Numpy, Statsmodels and Scikit-learn**.")
    st.markdown("# Business question: is it possible to predict the amount of calories burnt during a workout?")
    st.markdown("In this simple project, I analysed the data to find correlations between the variables and then created a ML model using **Linear Regression**, it's not the best model for this case, but it predicts with a **92% accuracy** in the test cases.")


    st.markdown("## Sample of the dataset")
    st.markdown("Source: https://www.kaggle.com/datasets/ruchikakumbhar/calories-burnt-prediction/data")
    st.write(df.sample(10))

    # plot
    st.markdown("## Scatter plot with a OLS line")
    fig = px.scatter(
        df, 
        x='Duration',
        y='Calories',
        color='Gender',
        size='Heart_Rate',
        trendline='ols', # linear regression line
        hover_data=['Height', 'Weight', 'Heart_Rate', 'Body_Temp'],
        labels={'Gender': 'Gender', 'Heart_Rate': 'Heart Rate (bpm)'},
        color_discrete_sequence=['blue', 'red']  # used for categorical variables color
    )

    fig.update_layout(
        title='Calories Burnt During a Workout',
        xaxis_title='Workout Duration (minutes)',
        yaxis_title='Calories Burnt'
    )

    fig.update_layout(width=1000, height=700)
    st.plotly_chart(fig)

    st.markdown("## Model prediction (not to be considered)")

    st.write(f":green[Model score: {model_score:.2f}]")
    duration = st.number_input("Enter workout duration (minutes)", min_value=1, max_value=120, value=30, step=1)

    # trigger to button
    if st.button("Predict Calories Burned"):
        # Make prediction using the model
        prediction = model.predict([[duration]])[0]
        
        # Display the prediction with formatting
        st.success(f"Predicted calories burned: **{prediction:.2f}** calories")
        
if __name__ == "__main__":
    model, score_model = model()
    app(model, score_model)