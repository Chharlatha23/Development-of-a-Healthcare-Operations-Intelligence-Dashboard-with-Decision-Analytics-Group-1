import pandas as pd
import os

def clean_data():
    raw_path = "Raw Dataset/Admissions_filled.csv"
    processed_dir = "Processed Dataset"
    processed_path = os.path.join(processed_dir, "Admissions_cleaned.csv")
    
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} not found.")
        return
        
    print(f"Loading raw dataset from {raw_path}...")
    df = pd.read_csv(raw_path)
    
    initial_shape = df.shape
    print(f"Initial shape: {initial_shape}")
    
    # 1. Clean Column Names (remove suffix duplicate columns like .1, .2)
    # Deduplicate columns by keeping primary domain columns and renaming appropriately
    df_cleaned = df.loc[:, ~df.columns.str.contains(r'\.\d+$')].copy()
    
    # Clean text columns formatting
    string_cols = df_cleaned.select_dtypes(include=['object']).columns
    for col in string_cols:
        df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
        
    # Standardize department names to Title Case
    if 'Department' in df_cleaned.columns:
        df_cleaned['Department'] = df_cleaned['Department'].str.title()
        
    # Standardize ward names
    if 'Ward' in df_cleaned.columns:
        df_cleaned['Ward'] = df_cleaned['Ward'].str.title()
        
    # 2. Datetime Parsing & Derivations
    date_cols = ['Admission_Date', 'Discharge_Date', 'Date', 'Registration_Date', 'Test_Date']
    for col in date_cols:
        if col in df_cleaned.columns:
            df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
            
    # Calculate Length of Stay (LOS) in days
    if 'Admission_Date' in df_cleaned.columns and 'Discharge_Date' in df_cleaned.columns:
        df_cleaned['Length_of_Stay_Days'] = (df_cleaned['Discharge_Date'] - df_cleaned['Admission_Date']).dt.days
        # Fill any missing/negative values with default 1 day
        df_cleaned['Length_of_Stay_Days'] = df_cleaned['Length_of_Stay_Days'].apply(lambda x: x if x > 0 else 1)
        
    # 3. Financial Derivations & Calculations
    if 'Total_Amount' in df_cleaned.columns and 'Insurance_Cover' in df_cleaned.columns:
        df_cleaned['Insurance_Coverage_Pct'] = (df_cleaned['Insurance_Cover'] / df_cleaned['Total_Amount'] * 100).round(2)
        
    if 'Total_Amount' in df_cleaned.columns and 'Insurance_Cover' in df_cleaned.columns and 'Patient_Paid' in df_cleaned.columns:
        df_cleaned['Outstanding_Balance'] = (df_cleaned['Total_Amount'] - df_cleaned['Insurance_Cover'] - df_cleaned['Patient_Paid']).round(2)
        # Outstanding balances less than 0 clipped to 0
        df_cleaned['Outstanding_Balance'] = df_cleaned['Outstanding_Balance'].apply(lambda x: max(0.0, x))
        
    # 4. Save processed dataset
    os.makedirs(processed_dir, exist_ok=True)
    df_cleaned.to_csv(processed_path, index=False)
    print(f"Cleaned dataset saved to {processed_path}. Shape: {df_cleaned.shape}")
    
    return df_cleaned

if __name__ == "__main__":
    clean_data()
