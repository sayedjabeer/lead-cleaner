import pandas as pd
import numpy as np

# 1. Load the dataset
df = pd.read_csv('Hubli_Car_Rental_Keywords.csv')

# 2. Clean percentage columns (remove '%' and convert to float)
def clean_pct(val):
    if isinstance(val, str):
        val = val.replace('%', '').replace('∞', '0')
        try:
            return float(val) / 100
        except ValueError:
            return 0.0
    return 0.0

df['Three month change'] = df['Three month change'].apply(clean_pct)
df['YoY change'] = df['YoY change'].apply(clean_pct)

# 3. Handle missing values
# Fill missing bids with 0 and indexed competition with the median or 0
df['Top of page bid (low range)'] = df['Top of page bid (low range)'].fillna(0)
df['Competition (indexed value)'] = df['Competition (indexed value)'].fillna(0)

# 4. Remove columns that are entirely empty (like Ad/Organic impression shares)
df_cleaned = df.dropna(axis=1, how='all')

# Save the cleaned version for the next steps
df_cleaned.to_csv('Cleaned_Hubli_Keywords.csv', index=False)

print("Data cleaning complete. Column 'Three month change' and 'YoY change' are now numeric.")
print(df_cleaned[['Keyword', 'Avg. monthly searches', 'Three month change']].head())
