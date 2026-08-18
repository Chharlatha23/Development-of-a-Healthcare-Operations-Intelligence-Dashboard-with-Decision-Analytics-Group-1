import pandas as pd
import json
import os

def run_comprehensive_eda():
    cleaned_path = "Processed Dataset/Admissions_cleaned.csv"
    output_json = "Processed Dataset/eda_insights.json"
    
    if not os.path.exists(cleaned_path):
        print(f"Error: {cleaned_path} not found.")
        return
        
    df = pd.read_csv(cleaned_path)
    df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
    
    # 1. Key Business Metrics (KPIs)
    total_patients = int(df['Patient_ID'].nunique())
    total_admissions = int(len(df))
    total_revenue = float(df['Total_Amount'].sum())
    total_insurance = float(df['Insurance_Cover'].sum())
    total_patient_paid = float(df['Patient_Paid'].sum())
    total_outstanding = float(df['Outstanding_Balance'].sum())
    # Estimated collected = Revenue minus outstanding dues (consistent with dashboard definition)
    estimated_collected = float(max(0.0, total_revenue - total_outstanding))
    collection_rate = float(round(estimated_collected / max(1, total_revenue) * 100, 2))
    avg_age = float(round(df['Age'].mean(), 1))
    # Use NaN-safe mean so invalid LOS records (Discharge < Admission) are excluded
    avg_los = float(round(df['Length_of_Stay_Days'].mean(skipna=True), 2))
    emergency_admissions = int(df['Emergency'].value_counts().get('Yes', 0))
    emergency_rate = float(round((emergency_admissions / total_admissions) * 100, 2))
    
    # 2. Department Analysis
    dept_kpis = df.groupby('Department').agg(
        admissions=('Admission_ID', 'count'),
        avg_los=('Length_of_Stay_Days', 'mean'),
        total_revenue=('Total_Amount', 'sum'),
        avg_bill=('Total_Amount', 'mean')
    ).round(2).reset_index().to_dict(orient='records')
    
    # 3. Financial Breakdown by Payment Status
    payment_status = df.groupby('Payment_Status').agg(
        count=('Admission_ID', 'count'),
        total_amount=('Total_Amount', 'sum'),
        patient_paid=('Patient_Paid', 'sum'),
        outstanding=('Outstanding_Balance', 'sum')
    ).round(2).reset_index().to_dict(orient='records')
    
    # 4. Ward & Room Type Distribution
    ward_occupancy = df['Ward'].value_counts().to_dict()
    room_types = df['Room_Type'].value_counts().to_dict()
    
    # 5. Diagnostic & Lab Insights
    top_diagnoses = df['Diagnosis'].value_counts().head(10).to_dict()
    top_labs = df['Test_Name'].value_counts().head(10).to_dict()
    top_medicines = df['Medicine'].value_counts().head(10).to_dict()
    
    # 6. Monthly Trend Analysis
    # Dynamically exclude the latest month if it is incomplete (i.e., dataset ends before the last calendar day of that month)
    import calendar
    df['Month_Year'] = df['Admission_Date'].dt.to_period('M').astype(str)
    max_date = df['Admission_Date'].max()
    last_day_of_max_month = calendar.monthrange(max_date.year, max_date.month)[1]
    is_final_month_complete = (max_date.day == last_day_of_max_month)
    if not is_final_month_complete:
        incomplete_month_str = max_date.strftime('%Y-%m')
        trend_df = df[df['Month_Year'] != incomplete_month_str]
    else:
        trend_df = df
    monthly_trend = trend_df.groupby('Month_Year').agg(
        admissions=('Admission_ID', 'count'),
        revenue=('Total_Amount', 'sum')
    ).reset_index().to_dict(orient='records')
    
    insights = {
        "kpis": {
            "total_patients": total_patients,
            "total_admissions": total_admissions,
            "total_revenue_inr": total_revenue,
            "total_insurance_inr": total_insurance,
            "total_patient_paid_inr": total_patient_paid,
            "total_outstanding_inr": total_outstanding,
            "estimated_collected_inr": estimated_collected,
            "collection_rate_pct": collection_rate,
            "avg_age": avg_age,
            "avg_los_days": avg_los,
            "emergency_admissions": emergency_admissions,
            "emergency_rate_pct": emergency_rate,
            "incomplete_final_month_excluded": None if is_final_month_complete else incomplete_month_str
        },
        "department_kpis": dept_kpis,
        "payment_status": payment_status,
        "ward_occupancy": ward_occupancy,
        "room_types": room_types,
        "top_diagnoses": top_diagnoses,
        "top_labs": top_labs,
        "top_medicines": top_medicines,
        "monthly_trend": monthly_trend
    }
    
    with open(output_json, "w") as f:
        json.dump(insights, f, indent=4)
        
    print(f"Comprehensive EDA Insights written to {output_json}")

if __name__ == "__main__":
    run_comprehensive_eda()
