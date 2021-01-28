import requests
import streamlit as st
import secrets_beta
from streamlit_google_oauth import st_google_oauth


st.write('Hello')

credentials = st_google_oauth(st.secrets["CLIENT_ID"], st.secrets["CLIENT_SECRET"], [st.secrets["SCOPE"]])
if credentials is not None:
  token = credentials["access_token"]
  r = requests.get('https://www.googleapis.com/drive/v3/about?fields=user&access_token=' + token)
  st.write(r.json())