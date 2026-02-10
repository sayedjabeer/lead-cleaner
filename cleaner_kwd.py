import streamlit as st
import pandas as pd
import io

# 1. Page Configuration
st.set_page_config(page_title="FortuneMarq Commercial Keyword Finder", page_icon="💰")
st.title("FortuneMarq Commercial Keyword Finder")
st.markdown("### Filters: High Intent & Commercial Keywords Only")

# 2. File Uploader
uploaded_file = st.file_uploader("Upload Google Keyword Planner CSV", type=["csv"])

if uploaded_file:
    try:
        # Load with Google's Tab-Separated / UTF-16 format
        try:
            df = pd.read_csv(uploaded_file, sep='\t', encoding='utf-16', skiprows=2)
        except:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, sep='\t', skiprows=2)

        df.columns = df.columns.str.strip()
        kw_col = 'Keyword'
        vol_col = 'Avg. monthly searches'
        cpc_col = 'Top of page bid (high range)'

        # Convert to numeric
        df[vol_col] = pd.to_numeric(df[vol_col], errors='coerce').fillna(0)
        df[cpc_col] = pd.to_numeric(df[cpc_col], errors='coerce').fillna(0)

        # --- REFINED FILTERING LOGIC ---
        
        # 1. Remove Duplicates
        df = df.drop_duplicates(subset=[kw_col])

        # 2. Remove No-Volume Keywords
        df = df[df[vol_col] > 0]

        # 3. Define Intent Filters
        educational_terms = ['what is', 'how to', 'types of', 'meaning', 'causes', 'symptoms', 'history', 'example', 'defined']
        commercial_terms = ['near me', 'cost', 'price', 'clinic', 'specialist', 'treatment', 'implant', 'whitening', 'best', 'root canal', 'braces', 'dentist', 'fees']

        # Remove Educational Keywords
        for term in educational_terms:
            df = df[~df[kw_col].str.contains(term, case=False, na=False)]

        # Keep Commercial Intent: (Active Bidders OR High Intent Phrases)
        df_commercial = df[
            (df[cpc_col] > 0) | 
            (df[kw_col].str.contains('|'.join(commercial_terms), case=False, na=False))
        ]

        # 4. Sorting: Highest Volume First
        df_commercial = df_commercial.sort_values(by=vol_col, ascending=False)

        # 5. Metrics & Display
        st.success(f"Found {len(df_commercial)} Commercial High-Intent Keywords.")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Commercial Keywords", len(df_commercial))
        col2.metric("Total Commercial Volume", f"{df_commercial[vol_col].sum():,.0f}")
        col3.metric("Avg. Market CPC", f"₹{df_commercial[df_commercial[cpc_col] > 0][cpc_col].mean():.2f}")

        st.write("### High Intent Keyword List")
        st.dataframe(df_commercial[[kw_col, vol_col, cpc_col]].head(100))

        # 6. Export
        csv_buffer = io.StringIO()
        df_commercial.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="📥 Download Commercial Keywords",
            data=csv_data,
            file_name=f"Commercial_HighIntent_Keywords.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")