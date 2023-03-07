import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

import process_data

# Configure how the page appears in browser tab
st.set_page_config(page_title="Explore Trends", page_icon="⬆️")

@st.cache_data
# Collect data on the percent difference in mortality across years
def collect_diff_data():
    diff_df = process_data.read_diff_csv()
    diff_df["id"] = diff_df["FIPS"].astype(int)
    return diff_df

@st.cache_data
# Collect the main dataframe with yearly mortality rates
def collect_state_data():
    state_df = process_data.read_states()
    state_df = state_df.dropna(subset=['FIPS'])
    state_df["id"] = state_df["FIPS"].astype(int)
    return state_df

diff_df = collect_diff_data()
state_df = collect_state_data()

st.title("Explore trends in the data")

with st.sidebar:
    # Selectbox widget for mortality cause
    display_cause = st.selectbox(
        label="Select a mortality cause",
        options=state_df["cause_name"].unique(),
        index=0
    )

    display_sex = "Both"
    
    # Selectbox widget for state to show in line plot
    display_state = st.selectbox(
        label="Select a state",
        options=state_df.sort_values(by="State").State.unique(),
        index=0
    )

state_df["str_id"] = state_df["id"].astype(str)
msk = state_df['str_id'].str.len() <= 2
only_state_df = state_df.loc[msk] 
state_to_id = {v:i for (v,i) in zip(only_state_df.State, only_state_df.id) }
display_state_id = state_to_id[display_state] 
    
subset_diff = diff_df[diff_df.cause_name == display_cause]
subset_diff = subset_diff[subset_diff.sex == display_sex]

subset_state = state_df[state_df.cause_name == display_cause]
# subset_state = subset_state[subset_state.sex == display_sex]
subset_state = subset_state[subset_state.State == display_state]

# Map of the U.S. by counties
counties = alt.topo_feature(data.us_10m.url, 'counties')

st.write(subset_diff.head())

# Map showing the US colored by percent change in mortality
mort_diff = alt.Chart(counties).mark_geoshape().transform_calculate(
    state_id = "(datum.id / 1000)|0"
).encode(
    color=alt.condition(alt.datum.state_id == display_state_id, alt.value('red'), "pc_change_val:Q"),
    tooltip=[alt.Tooltip('location_name:N', title='County Name'),
                 alt.Tooltip('pc_change_val:Q', title='Percent change in mortality (1980-2014)', format='.2f')]
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=subset_diff,key='id',fields=['pc_change_val', 'location_name'])
).project(
    "albersUsa"
).properties(
    title="Percent Change in Mortality 1980-2014",
    width=650,
    height=300
)

# Line plot showing mortality trends for the selected state
state_trends = alt.Chart(subset_state).mark_line(point=True).transform_filter(
    (alt.datum.sex == 'Male') | (alt.datum.sex == 'Female')
).encode(
    x=alt.X('year_id:O', title='Year'),
    y=alt.Y('sum(mx):Q', title='Deaths per 100,000'),
    color='sex:N'
).properties(
    width=650,
    height=300,
    title=(f'Trends across sex for {display_state}')
)

chart_trend = alt.vconcat(mort_diff, state_trends, spacing=50)

st.altair_chart(chart_trend,
    use_container_width=False)
