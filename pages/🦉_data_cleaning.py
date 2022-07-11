import streamlit as st
import time
import glob
import pandas as pd

def get_datasets():
    return glob.glob('datasets/*.csv')

@st.experimental_memo
def import_df(path, conv_dtypes, drop_duplicates, drop_na):
    df = pd.read_csv(path)
    if conv_dtypes:
        df = df.convert_dtypes()
    if drop_duplicates:
        df = df.drop_duplicates()
    if drop_na:
        df = df.dropna()
    return df

@st.cache
def fetch_data(df):
    return df


def clean_df(df, data_manipulation):
    pass

st.title('Data Cleaning')
st.write('---')
files = get_datasets()
with st.expander('Step 1: Load and clean.'):
    # with st.form('Read dataframe'):
        col1, col2, col3 = st.columns(3)
        with col1:
            dataset_file = st.selectbox('Select dataset', files)
        with col2:
            conv_dtypes = st.checkbox('Convert Dtypes')
            drop_duplicates = st.checkbox('Drop duplicates')
            drop_na = st.checkbox('Drop NA')
        with col3:
            # load_df = st.form_submit_button('Load and transform')
            # if load_df:
            with st.spinner(text='Saving...'):
                df = import_df(dataset_file, conv_dtypes, drop_duplicates, drop_na)
                st.success('Done! Continue with Step 2.')
        st.write(df)

with st.expander('Step 2: Imputing strategy.'):
    data_manipulation = dict()
    try:
        nan_cols = [i for i in df.columns if df[i].isnull().any()]
        if len(nan_cols) == 0:
            st.write("There's nothing to impute, all cells contain not null values.")
        else:
            st.write('The following columns contain missing data, please select for each one the imputing strategy.')
            st.write('---')
            with st.form('imputing_form'):
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.write('Column:')
                with c2:
                    st.write('Type:')
                with c3:
                    st.write('Impute Strategy:')
                with c4:
                    st.write('Transform Strategy:')
                st.write('---')
                for col in df.columns:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write(col)
                    with col2:
                        col_dtype = df[f'{col}'].dtype
                        st.write(col_dtype)
                    with col3:
                        if col_dtype in ['Int64', 'Float64', 'Int32', 'Float32']:
                            impute_options = ['Drop NA', 'Mean', 'Median']
                            transform_options = ['None', 'Drop Column','StandardScaler', 'PowerTransformer', 'Normalizer']
                        else:
                            impute_options = ['Drop NA', 'Most Frequent']
                            transform_options = ['Drop Column', 'OneHotEncoder', 'LabelEncoder']
                        if col in nan_cols:
                            data_manipulation[f'{col}_impute'] = st.selectbox(
                                'Choose impute strategy', impute_options, key=f'{col}_impute', on_change=None)
                        else:
                            st.write('All good!')
                    with col4:
                        data_manipulation[f'{col}_transform'] = st.selectbox(
                            'Choose transform strategy', transform_options, key=f'{col}_transform', on_change=None)
                    st.write('---')
                    
                col1, col2 = st.columns([2, 1])
                with col1:
                    cleaned_df_name = st.text_input('Filename:')
                    confirm_impute = st.form_submit_button('Clean, transform and save Dataset')
                with col2:
                    st.write('')
                    st.write(
                        'The dataset will be saved and it could be used later for building ML moldels.')
                if confirm_impute:
                    with st.spinner(text='Saving...'):
                        df_cleaned = clean_df(
                            df, data_manipulation)
                        st.write(data_manipulation)
                        # df_cleaned.to_csv(
                        #     f'cleaned_datasets/{cleaned_df_name}.csv', index=False)
                        time.sleep(2)
                        st.success('Done')
                
    except:
        st.write('Please complete Step 1 to continue')
