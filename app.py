import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import base_page, data_adquisition, data_cleaning  # import your pages here

# Create an instance of the app 
app = MultiPage()

apptitle = 'Data Science & Big Data'
st.set_page_config(page_title=apptitle, page_icon="🦈", layout='wide')

# Add all your applications (pages) here
app.add_page("Data Cleaning", data_cleaning.app)
app.add_page("Importing Data", data_adquisition.app)

# The main app
app.run()