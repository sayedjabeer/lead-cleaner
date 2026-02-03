import streamlit as st
import pandas as pd
import io

# 1. Page Configuration (Browser Tab Name & Icon)
st.set_page_config(page_title="FortuneMarq Data Cleaners", page_icon="📈")

# 2. Main Header
st.title("FortuneMarq Data Cleaners")
st.markdown("Automated lead cleaning for high-quality data exports.")

# 3. User Input for City
city_name = st.text_input("Enter the city name for this dataset:", value="Hubli")

# 4. File Uploader
uploaded_file = st.file_uploader("Upload your raw scraped CSV file", type=["csv"])

if uploaded_file:
    try:
        # Load the raw file
        df = pd.read_csv(uploaded_file)
        
        # --- DATA CLEANING LOGIC ---
        
        # A. Remove businesses that have NEITHER a website NOR a phone number
        # (This keeps the lead if it has at least one way to be contacted)
        df = df.dropna(subset=['UsdlK', 'lcr4fd href'], how='all')
        
        # B. Remove rows where Business Name is missing
        df = df.dropna(subset=['qBF1Pd'])
        
        # --------------------------

        # 5. Create the Cleaned DataFrame
        cleaned = pd.DataFrame()
        cleaned['BUSINESS NAME'] = df['qBF1Pd']
        cleaned['PHONE'] = df['UsdlK']
        cleaned['WEBSITE LINK'] = df['lcr4fd href'].fillna('NIL')
        cleaned['CITY'] = city_name
        
        # 6. Display Stats and Preview
        st.success(f"Cleaning complete! Found {len(cleaned)} valid leads.")
        st.write("### Preview of Cleaned Data")
        st.dataframe(cleaned.head(10))
        
        # 7. Export and Download
        csv_buffer = io.StringIO()
        cleaned.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download Cleaned CSV", 
            data=csv_data, 
            file_name=f"Cleaned_{city_name}_Leads.csv", 
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Something went wrong while processing the file: {e}")
        st.info("Ensure the uploaded file contains the columns: 'qBF1Pd', 'UsdlK', and 'lcr4fd href'.")
