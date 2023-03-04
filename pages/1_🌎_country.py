import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

import process_data

st.set_page_config(page_title="Country", page_icon="📈")

@st.cache_data

# Cache state data from CSV files, dropping entries without a FIPS code
def collect_state_data():
    state_df = process_data.read_states()
    state_df = state_df.dropna(subset=['FIPS'])
    state_df["id"] = state_df["FIPS"].astype(int)
    return state_df

state_df = collect_state_data()
state_df["str_id"] = state_df["id"].astype(str)
msk = state_df['str_id'].str.len() <= 2
only_state_df = state_df.loc[msk] 
state_to_id = {v:i for (v,i) in zip(only_state_df.State, only_state_df.id) }

# Sidebar for data filtering widgets
with st.sidebar:

    # Multi-select widget for mortality causes
    display_causes = st.multiselect(
        label="Select one or more mortality causes",
        options=state_df["cause_name"].unique(),
        default="Alcohol use disorders"
    )

    # Radio buttons to select sex
    display_sex = st.radio(
        label="Select a sex to display",
        options=("Male", "Female", "Both"),
        index=0
    )

    # Slider widget to select year
    display_year = st.slider(
        label="Select a year",
        min_value=1980,
        max_value=2014,
        value=1990
    )
    
    # Select widget for mortality causes
    display_state = st.selectbox(
        label="Select a state",
        options=state_df["State"].unique(),
        index=0
    )
    display_state_id = state_to_id[display_state]

# Main chart title
st.write("Mortality rates by county")

subset_df = state_df[state_df.cause_name.isin(display_causes)]
subset_df = subset_df[subset_df.sex == display_sex]
subset_df = subset_df[subset_df.year_id == display_year]

counties = alt.topo_feature(data.us_10m.url, 'counties')
source = subset_df

selector = alt.selection_single()

us_mort = alt.Chart(counties).mark_geoshape().encode(
    color=alt.Color('mx:Q',
                    title="Deaths per 100,000")
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=source, key='id', fields=['mx'])
).project(
    "albersUsa"
).properties(
    width=800,
    height=500
)

subset_df_state = subset_df[subset_df.State == display_state]

map_state =alt.Chart(data = counties).mark_geoshape(
        stroke='black',
        strokeWidth=1
    ).transform_calculate(
        state_id = "(datum.id / 1000)|0"
    ).transform_filter(
        (alt.datum.state_id)==display_state_id
    ).encode(
        color=alt.Color('mx:Q', title="Deaths per 100,000")
    ).transform_lookup(
        lookup='id', 
        from_=alt.LookupData(data=subset_df_state , key='id', fields=['mx'])
    ).project("albersUsa").properties(
        width=2000,
        height=2000
    )

chart_mort = alt.vconcat(us_mort, map_state).resolve_scale(
        color = 'independent')

st.altair_chart(chart_mort,
    use_container_width=False)
