import altair as alt
import pandas as pd
import streamlit as st
from process import *
from vega_datasets import data

@st.cache_data
def collect_state_data():
    state_df = read_states()
    return state_df

state_df = collect_state_data()