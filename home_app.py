# home_app.py - Simple launcher that starts with the GDPR chatbot
import streamlit as st

# Configure the app to start with the GDPR chatbot as the main page
pages = [
    st.Page("pages/1_🛡️_GDPR_AI_Compliance_Assistant.py", title="GDPR Assistant", icon="🛡️"),
    st.Page("pages/2_About_the_app.py", title="About the App", icon="ℹ️"),
]

# Set up navigation - first page becomes the default/landing page
pg = st.navigation(pages)
pg.run()