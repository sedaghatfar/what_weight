import streamlit as st
import pandas as pd
import re
import os
import plotly.express as px

# Function to process the file
def process_file(uploaded_file):
    dates = []
    speakers = []
    msgs = []
    weights = []

    for line in uploaded_file:
        line = line.decode("utf-8")  # Decoding to convert from binary
        date_match = re.search(r'\[(.*?)\]', line)
        speaker_match = re.search(r'\] (.*?):', line)
        msg_match = re.search(r': (.*)', line)
        weight_match = re.search(r': (\d+)', line)

        if date_match and speaker_match and msg_match and weight_match:
            dates.append(date_match.group(1))
            speakers.append(speaker_match.group(1))
            msgs.append(msg_match.group(1))
            weights.append(weight_match.group(1))

    df = pd.DataFrame({
        'Date': pd.to_datetime(dates),
        'Speaker': speakers,
        'Msg': msgs,
        'Weight': pd.to_numeric(weights, errors='coerce')
    })
    return df

# Function to remove outliers
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Streamlit app
# st.image('weds_export.jpeg', use_column_width=True)
def main():
    st.title("Weight What[sApp]?")
    st.write("Current working directory:", os.getcwd())



    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type="txt")
    if uploaded_file is not None:
        data = process_file(uploaded_file)
        st.write(data)

        # Speaker selection
        speaker_list = data['Speaker'].unique()
        selected_speaker = st.selectbox("Select a Speaker", speaker_list)

        # Checkbox for outlier removal
        remove_outliers_option = st.checkbox("Remove Outliers")

        # Filter data based on selected speaker
        filtered_data = data[data['Speaker'] == selected_speaker]

        # Remove outliers if option is selected
        if remove_outliers_option:
            filtered_data = remove_outliers(filtered_data, 'Weight')

        # Plot
        fig = px.scatter(filtered_data, x='Date', y='Weight', hover_data=['Msg'], color='Speaker')
        fig.update_layout(xaxis_range=[100, None], showlegend=False)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
