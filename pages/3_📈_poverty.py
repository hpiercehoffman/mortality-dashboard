import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

import process_data

# Configure how the page appears in browser tab
st.set_page_config(page_title="2014 Poverty Rates", page_icon="📈")

@st.cache_data

def collect_poverty_data():
    poverty_df = process_data.read_poverty_csv()
    poverty_df = poverty_df.rename({'Poverty Percent, All Ages': 'percent'},
                                    axis='columns')
    poverty_df["County FIPS Code"] = poverty_df["County FIPS Code"].astype(str).str.zfill(3)
    poverty_df["id"] = poverty_df["State FIPS Code"].astype(str) + poverty_df["County FIPS Code"].astype(str)
    poverty_df["id"] = poverty_df["id"].astype(int)
    return poverty_df

def collect_state_data():
    state_df = process_data.read_states()
    state_df = state_df.dropna(subset=['FIPS'])
    state_df["id"] = state_df["FIPS"].astype(int)
    return state_df

poverty_df = collect_poverty_data()
state_df = collect_state_data()

with st.sidebar:

    # Selectbox widget for mortality cause
    display_cause = st.selectbox(
        label="Select a mortality cause",
        options=state_df["cause_name"].unique(),
        index=0
    )

    # Radio buttons to select sex
    display_sex = st.radio(
        label="Select a sex to display",
        options=("Male", "Female", "Both"),
        index=0
    )

    # Year is restricted to 2014
    display_year = 2014
    
    # Selectbox widget for state to show in line plot
    display_state = st.selectbox(
        label="Select a state",
        options=state_df["State"].unique(),
        index=0
    )

subset_df = state_df[state_df.cause_name == display_cause]
subset_df = subset_df[subset_df.sex == display_state]
subset_df = subset_df[subset_df.year_id == display_year]

st.title("2014 poverty and mortality rates")

# Map of the U.S. by counties
counties = alt.topo_feature(data.us_10m.url, 'counties')
source_poverty = poverty_df
source_mort = subset_df

selection = alt.selection_single(fields=['id'], empty="none")

# Map showing the US colored by poverty rates
us_poverty = alt.Chart(counties).mark_geoshape().encode(
    color=alt.condition(selection, alt.value('red'), "percent:Q"),
    tooltip=[alt.Tooltip('Name:N', title='County'),
             alt.Tooltip('percent:Q', title='Percent Poverty')]
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=source_poverty,
                         key='id',
                         fields=['percent', 'Name'])
).project(
    "albersUsa"
).properties(
    title="2014 Poverty Rates",
    width=650,
    height=300
).add_selection(selection)

# Map showing the US colored by mortality rates
us_mort = alt.Chart(counties).mark_geoshape().encode(
    color=alt.condition(selection, alt.value('red'), "mx:Q"),
    tooltip=[alt.Tooltip('location_name:N', title='County Name'),
             alt.Tooltip('mx:Q', title='Deaths per 100,000', format='.2f')]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(data=source_mort,
                             key='id',
                             fields=['mx', 'location_name'])
    ).project(
        "albersUsa"
    ).properties(
        title="2014 Mortality Rates",
        width=650,
        height=300
    ).add_selection(selection)

chart_2014 = alt.vconcat(us_poverty, us_mort).resolve_scale(
    color='independent'
)

merged_df = source_mort.merge(source_poverty, how='inner')
st.write(merged_df)

scatter_state = alt.Chart(source_mort).mark_circle(size=60).encode(
    x='',
    y='Miles_per_Gallon',
    color='Origin',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).interactive()

st.altair_chart(chart_2014,
    use_container_width=False)

