import altair as alt
import pandas as pd
import streamlit as st
import process_data
from vega_datasets import data

# Global vars
PROJECTION_TYPE = "albersUsa"

@st.cache_data
def collect_state_data():
    state_df = process_data.read_states()
    return state_df

state_df = collect_state_data()
state_df = state_df.dropna(subset=['FIPS'])
state_df["id"] = state_df["FIPS"].astype(int)

st.write("Mortality rates by county")

alc_df = state_df[state_df.cause_name == 'Alcohol use disorders']
alc_df = alc_df[alc_df.sex == 'Both']
alc_df = alc_df[alc_df['year_id'] == 1990]

counties = alt.topo_feature(data.us_10m.url, 'counties')
source = alc_df

us_map = alt.Chart(counties).mark_geoshape(
    fill = '#aaa',
    stroke = 'white'
).properties(
    width = 800,
    height = 500
).project(PROJECTION_TYPE)


us_mort = alt.Chart(counties).mark_geoshape().encode(
    color=alt.Color('mx:Q')
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=source, key='id', fields=['mx'])
).project(
    PROJECTION_TYPE
).properties(
    width=800,
    height=500
)

chart_mort = alt.vconcat(us_mort).resolve_scale(
        color = 'independent'
    )

st.altair_chart(chart_mort,
    use_container_width=False)
