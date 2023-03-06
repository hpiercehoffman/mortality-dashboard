import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

import process_data

# Configure how the page appears in browser tab
st.set_page_config(page_title="Explore Trends", page_icon="⬆️")

@st.cache_data
def collect_diff_data():
    diff_df = process_data.read_diff_csv()
    diff_df["id"] = diff_df["FIPS"].astype(int)
    return diff_df

@st.cache_data
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
        options=state_df["State"].unique(),
        index=0
    )

subset_diff = diff_df[diff_df.cause_name == display_cause]
subset_diff = subset_diff[subset_diff.sex == display_sex]

subset_state = state_df[state_df.cause_name == display_cause]
# subset_state = subset_state[subset_state.sex == display_sex]
subset_state = subset_state[subset_state.State == display_state]

# county_to_id = {v:i for (v,i) in zip(subset_state.location_name, subset_state.id)}
# id_to_county = {v: k for k, v in county_to_id.items()}

# Map of the U.S. by counties
counties = alt.topo_feature(data.us_10m.url, 'counties')

# def ret_fips():
#     from streamlit_vega_lite import altair_component
#     def country_map_diff():
#         selection = alt.selection_single(fields=['id'], empty="none")
#         return (alt.Chart(counties).mark_geoshape().transform_lookup(
#             lookup='id',
#             from_=alt.LookupData(data=subset_diff, key='id', fields=['pc_change_val', 'location_name'])
#         ).encode(
#             color='pc_change_val:Q',
#             tooltip=[alt.Tooltip('location_name:N', title='County Name'),
#                      alt.Tooltip('pc_change_val:Q', title='Percentage change', format='.2f')]
#         ).project(
#             "albersUsa"
#         ).add_selection(selection
#         ).properties(
#             width=600,
#             height=300
#         ))
#     return altair_component(altair_chart=country_map_diff()).get("id")

# st.write("Select a county to see its trends")

# fips_c = ret_fips()
# print(fips_c)
# if fips_c:
#     county_fips = fips_c[0]
#     st.write(f"Mortality trends across sexes for {id_to_county[county_fips]}")
#     state_trends = alt.Chart(source_states).mark_line(point=True).encode(
#         x='year_id:O',
#         y='mx:Q',
#         color='sex:N'
#     ).properties(
#         width=800,
#         height=600
#     )
#     st.altair_chart(state_trends)


# # Map showing the US colored by percent change in mortality
# mort_diff = alt.Chart(counties).mark_geoshape().encode(
#     color=alt.Color("pc_change_val:Q", title="Percent change in mortality")
# ).transform_lookup(
#     lookup='id',
#     from_=alt.LookupData(data=source_diff,
#                          key='id',
#                          fields=['pc_change_val'])
# ).project(
#     "albersUsa"
# ).properties(
#     title="Percent Change in Mortality",
#     width=800,
#     height=600
# )

# # Line plot showing mortality trends for the selected state
# state_trends = alt.Chart(source_states).mark_line(point=True).encode(
#     x='year_id:O',
#     y='sum(mx):Q',
#     color='sex:N'
# ).properties(
#     width=800,
#     height=600
# )

# chart_trend = alt.vconcat(mort_diff, state_trends)

# st.altair_chart(chart_trend,
#     use_container_width=False)
