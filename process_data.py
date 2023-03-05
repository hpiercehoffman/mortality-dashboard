import numpy as np
import pandas as pd
import altair as alt
import streamlit
import vega_datasets
import os

def read_state_csv(fl):
    to_remove = ['index', 'measure_id','measure_name', 'age_id', 'metric','measure_ID']
    df = pd.read_csv(fl)
    df = df.drop(columns = [col for col in df.columns if col in to_remove])
    df['State'] = df.loc[0,'location_name']
    return df

def read_states():
    main_dir = 'data/states'
    fls = os.listdir(main_dir)
    data_list = []
    for fl in fls:
        if os.path.splitext(os.path.join(main_dir,fl))[1].lower() == '.csv':
            data_list.append(read_state_csv(os.path.join(main_dir,fl)))
    df_mort = pd.concat(data_list)
    df_mort = df_mort.reset_index(drop=True)
    return df_mort

def read_poverty_csv():
    df_poverty = pd.read_excel('data/poverty/poverty_2014.xls')
    df_poverty = df_poverty[df_poverty.columns.drop(
        list(df_poverty.filter(regex='CI|Estimate|Postal Code')))]
    return df_poverty

def read_diff_csv():
    diff_df = pd.read_csv(
        'data/percent_diff/IHME_USA_COUNTY_USE_INJ_MORTALITY_1980_2014_PCT_DIFF_Y2018M03D13.CSV')
    diff_df = diff_df.dropna(subset=['FIPS'])
    return diff_df