pip install streamlit pandas
import streamlit as st
import pandas as pd

# Load dataset
@st.cache
def load_data():
    return pd.read_csv('data.csv')

data = load_data()

# Streamlit app layout
st.title("Simple Search Engine")

# Input for search
search_query = st.text_input("Search for:")

if search_query:
    # Filter data based on search query
    results = data[data['title'].str.contains(search_query, case=False, na=False)]
    
    if not results.empty:
        st.write(f"Found {len(results)} result(s):")
        for _, row in results.iterrows():
            st.subheader(row['title'])
            st.write(row['description'])
    else:
        st.write("No results found.")
