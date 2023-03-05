import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

import process_data

# Configure how the page appears in browser tab
st.set_page_config(page_title="Explore Trends", page_icon="⬆️")

# @st.cache_data

def collect_diff_data():
    diff_df = process_data.read_diff_csv()
    return diff_df

diff_df = collect_diff_data()

st.dataframe(diff_df)

