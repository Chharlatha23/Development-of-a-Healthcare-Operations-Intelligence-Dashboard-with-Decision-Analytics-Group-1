import pandas as pd
import json
import os

def run_eda():
    cleaned_path = "Processed Dataset/Admissions_cleaned.csv"
    output_summary = "Processed Dataset/eda_summary.json"
    
    if not os.path.exists(cleaned_path):
        print(f"Error: {cleaned_path} not found. Run data_cleaning.py first.")
        return
        
    df = pd.read_csv(cleaned_path)
    print("Executing Exploratory Data Analysis...")
    
    summary = {
        "dataset_metrics": {
            "total_records": len(df),
            "total_departments": df['Department'].nunique() if 'Department' in df.columns else 0,
            "total_revenue_inr": float(df['Total_Amount'].sum()) if 'Total_Amount' in df.columns else 0.0,
            "total_insurance_cover_inr": float(df['Insurance_Cover'].sum()) if 'Insurance_Cover' in df.columns else 0.0,
            "total_patient_paid_inr": float(df['Patient_Paid'].sum()) if 'Patient_Paid' in df.columns else 0.0,
            "avg_length_of_stay_days": float(round(df['Length_of_Stay_Days'].mean(), 2)) if 'Length_of_Stay_Days' in df.columns else 0.0
        },
        "department_distribution": df['Department'].value_counts().to_dict() if 'Department' in df.columns else {},
        "ward_distribution": df['Ward'].value_counts().to_dict() if 'Ward' in df.columns else {},
        "room_type_distribution": df['Room_Type'].value_counts().to_dict() if 'Room_Type' in df.columns else {},
        "emergency_admission_ratio": df['Emergency'].value_counts().to_dict() if 'Emergency' in df.columns else {},
        "payment_status_distribution": df['Payment_Status'].value_counts().to_dict() if 'Payment_Status' in df.columns else {},
        "top_diagnoses": df['Diagnosis'].value_counts().head(10).to_dict() if 'Diagnosis' in df.columns else {}
    }
    
    with open(output_summary, "w") as f:
        json.dump(summary, f, indent=4)
        
    print(f"EDA Completed successfully! Summary saved to {output_summary}.")
    print("Key Highlights:")
    print(" - Total Billed Revenue: INR", summary["dataset_metrics"]["total_revenue_inr"])
    print(" - Avg Length of Stay:", summary["dataset_metrics"]["avg_length_of_stay_days"], "days")
    print(" - Top 3 Departments:", list(summary["department_distribution"].keys())[:3])

if __name__ == "__main__":
    run_eda()
