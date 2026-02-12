import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="FortuneMarq Market Intelligence", page_icon="📊", layout="wide")
st.title("FortuneMarq Bulk Market Reporter")
st.markdown("Upload multiple Keyword Planner CSVs to generate a comparative market analysis.")

# 1. Bulk File Uploader
uploaded_files = st.file_uploader("Upload all niche CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    report_data = []

    for file in uploaded_files:
        try:
            # Handle Google's TSV/UTF-16 format
            try:
                df = pd.read_csv(file, sep='\t', encoding='utf-16', skiprows=2)
            except:
                file.seek(0)
                df = pd.read_csv(file, sep='\t', skiprows=2)

            df.columns = df.columns.str.strip()
            
            # Clean and filter for Commercial Intent
            df['Avg. monthly searches'] = pd.to_numeric(df['Avg. monthly searches'], errors='coerce').fillna(0)
            df['Top of page bid (high range)'] = pd.to_numeric(df['Top of page bid (high range)'], errors='coerce').fillna(0)
            
            commercial_terms = ['near me', 'cost', 'price', 'clinic', 'specialist', 'treatment', 'implant', 'best', 'dentist']
            df_commercial = df[
                (df['Top of page bid (high range)'] > 0) | 
                (df['Keyword'].str.contains('|'.join(commercial_terms), case=False, na=False))
            ]

            # 2. Extract niche name from filename
            niche_name = file.name.replace(".csv", "").replace("_", " ")

            # 3. Calculate Intelligence Metrics
            report_data.append({
                "Niche/Market": niche_name,
                "Total Keywords": len(df_commercial),
                "Total Monthly Searches": df_commercial['Avg. monthly searches'].sum(),
                "Avg. CPC (Market Value)": df_commercial[df_commercial['Top of page bid (high range)'] > 0]['Top of page bid (high range)'].mean(),
                "Top Keyword": df_commercial.sort_values(by='Avg. monthly searches', ascending=False).iloc[0]['Keyword'] if not df_commercial.empty else "N/A"
            })

        except Exception as e:
            st.error(f"Could not process {file.name}: {e}")

    # 4. Generate the Master Report Table
    if report_data:
        master_df = pd.DataFrame(report_data)
        master_df = master_df.sort_values(by="Total Monthly Searches", ascending=False)

        st.write("### 📈 Master Comparative Report")
        st.dataframe(master_df, use_container_width=True)

        # 5. Export Master Report
        output = io.StringIO()
        master_df.to_csv(output, index=False)
        st.download_button(
            label="📥 Download Master Market Report",
            data=output.getvalue(),
            file_name="FortuneMarq_Market_Intelligence_Report.csv",
            mime="text/csv"
        )
