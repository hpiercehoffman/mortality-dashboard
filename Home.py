import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.write("# U.S. Mental Health Mortality")

st.markdown(
    """
    ## BMI 706 Final Project ##
    ### Varun Ullanat and Hannah Pierce-Hoffman ###

    ### Dive into the data ###
    - Explore mortality causes by state in the **States** tab
    - Visualize data trends in the **Trends** tab
    - Compare poverty and mortality data in the **Poverty** tab

    ### Learn more about this project ###
    - Visit [our GitHub repo](https://github.com/hpiercehoffman/bmi706-outliers/blob/main/README.md)
    - Take a look at [our mortality dataset](https://ghdx.healthdata.org/record/ihme-data/united-states-substance-use-disorders-intentional-injuries-mortality-rates-county-1980-2014)
    - Take a look at [our poverty dataset](https://www.census.gov/data/datasets/2014/demo/saipe/2014-state-and-county.html)
"""
)