import streamlit as st
import pandas as pd
import time
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

def app():
    st.title('Data Adquisition')
    st.write('---')
    file = st.file_uploader('Import dataset:')
    if file:
        print(file)
        df = pd.read_csv(file)
        with st.expander('Save dataset for data cleaning'):
            col1, col2 = st.columns([2, 1])
            with col1:
                name = st.text_input('Filename:')
                save = st.button('Save')
            with col2:
                st.write('')
                st.write('The dataset will be saved and it could be used later for data cleaning and building ML moldels.')
            if save:
                print(save)
                with st.spinner(text='Saving...'):
                    df.to_csv(f'datasets/{name}.csv', index=False)
                    time.sleep(2)
                    st.success('Done')
        profile_report = st.button('Generate profile report')
        if profile_report:
            pr = df.profile_report()
            st_profile_report(pr)
    