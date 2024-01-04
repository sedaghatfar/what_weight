import streamlit as st
import pandas as pd
import re
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

# Streamlit app
def main():
    st.title("Text File Processor")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type="txt")
    if uploaded_file is not None:
        data = process_file(uploaded_file)
        st.write(data)

        # Speaker selection
        speaker_list = data['Speaker'].unique()
        selected_speaker = st.selectbox("Select a Speaker", speaker_list)

        # Filter data based on selected speaker
        filtered_data = data[data['Speaker'] == selected_speaker]

        # Plot
        fig = px.scatter(filtered_data, x='Date', y='Weight', hover_data=['Msg'], color='Speaker')
        fig.update_layout(xaxis_range=[100, None], showlegend=False)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
