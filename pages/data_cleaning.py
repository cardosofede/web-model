import streamlit as st
import time
import glob
import pandas as pd

def get_datasets():
    return glob.glob('datasets/*.csv')

def app():
    st.title('Data Cleaning')
    st.write('---')
    files = get_datasets()
    df = pd.DataFrame()
    with st.expander('Step 1: Load and clean'):
        col1, col2, col3 = st.columns(3)
        with col1:
            dataset_file = st.selectbox('Select dataset', files)
        with col2:
            conv_dtypes = st.checkbox('Convert Dtypes')
            drop_duplicates = st.checkbox('Drop duplicates')
            drop_na = st.checkbox('Drop NA')
        with col3:
            load_df = st.button('Load and transform')
            if load_df:
                with st.spinner(text='Saving...'):
                        df = pd.read_csv(dataset_file)
                        if conv_dtypes:
                            df = df.convert_dtypes()
                        if drop_duplicates:
                            df = df.drop_duplicates()
                        if drop_na:
                            df = df.dropna()
                        st.success('Done! Continue with Step 2.')
                    
    if not df.empty:
        print(df.dtypes)
    