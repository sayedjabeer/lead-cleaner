import streamlit as st
import pandas as pd
import io

# Setup the interface
st.set_page_config(page_title="Mac Mini M4 Lead Cleaner", page_icon="💻")
st.title("Business Lead Cleaner")
st.markdown("### Optimized for Mac Mini M4")

# Input for the City
city_name = st.text_input("Which city is this data for?", value="Hubli")

# File Uploader
uploaded_file = st.file_uploader("Upload your raw CSV", type=["csv"])

if uploaded_file:
    try:
        # Load the raw file
        df = pd.read_csv(uploaded_file)
        
        # --- NEW CLEANING LOGIC ---
        # 1. Remove rows where BOTH Phone (UsdlK) and Website (lcr4fd href) are missing
        # 'how=all' means only drop if both columns are null
        df = df.dropna(subset=['UsdlK', 'lcr4fd href'], how='all')
        
        # 2. Remove rows where Business Name (qBF1Pd) is missing
        df = df.dropna(subset=['qBF1Pd'])
        # --------------------------

        # Process the data using your specific scraper IDs
        cleaned = pd.DataFrame()
        cleaned['BUSINESS NAME'] = df['qBF1Pd']
        cleaned['PHONE'] = df['UsdlK']
        cleaned['WEBSITE LINK'] = df['lcr4fd href'].fillna('NIL')
        cleaned['CITY'] = city_name
        
        st.write(f"### Preview (Total Leads: {len(cleaned)})")
        st.dataframe(cleaned.head(10))
        
        # Generate Download Button
        csv = cleaned.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned CSV", 
            data=csv, 
            file_name=f"Cleaned_{city_name}_Leads.csv", 
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Something went wrong: {e}")
