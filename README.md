# Olympic Data Analysis Web App
Live Demo: https://olympics-data-analysis-app-mnitingh.streamlit.app/

This repository contains a comprehensive data analysis of the Olympic Games dataset using Python and Streamlit. The study is structured into four main sections:

1. **Overall Medal Tally**: Analyzes the medal tally for all countries across various Olympic Games.
2. **Overall Analysis**: Covers key statistics, including participation trends, event counts, and the most popular athletes.
3. **Country-wise Analysis**: Focuses on each country's performance, breaking down medal counts by sport and highlighting top athletes.
4. **Athlete-wise Analysis**: Examines athlete demographics, including age distribution, height-weight correlations, and gender participation trends.

## Repository Structure

- **`app.py`**: The main file to run the Streamlit web app.
- **`helper.py`**: Contains helper functions used to process and analyze the data.
- **`plot_config.py`**: Configures the plots used throughout the analysis.
- **`EDA.ipynb`**: The Exploratory Data Analysis notebook where the initial data exploration was conducted.

## Technologies Used

- **Streamlit**: For building the interactive web app.
- **Pandas**: For data manipulation and analysis.
- **Matplotlib & Seaborn**: For static data visualization.
- **Plotly**: For interactive plots and visualizations.
- **NumPy**: For numerical computations.

## Dataset
Dataset link [click here](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)
The dataset includes 271,116 entries, each representing an athlete's participation in various Olympic events. Key attributes include athlete ID, name, gender, age, physical measurements (height and weight), team affiliation, event details, and medal outcomes.

## Insights

- Significant growth in the number of events and athlete participation over the years.
- A noticeable dip in participation in 1980 due to the boycott of the Moscow Olympics.
- The distribution of height and weight shows that medals are fairly spread across different categories.
- A steady increase in male and female participation over the years, with some historical dips in male participation.

## Documentation

The project is well-documented, with detailed explanations of the functions and processes used. Each script includes comprehensive docstrings to ensure clarity and ease of understanding.

## Deployed App

Check out the live version of the web app [here](https://olympics-data-analysis-app-mnitingh.streamlit.app/).
