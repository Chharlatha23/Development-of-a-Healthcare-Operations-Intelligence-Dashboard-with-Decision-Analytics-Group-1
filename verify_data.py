import json, pandas as pd

with open('Processed Dataset/eda_insights.json') as f:
    j = json.load(f)

k = j['kpis']
print('=== EDA JSON KPIs ===')
print('Total Admissions      :', k['total_admissions'])
print('Unique Patients       :', k['total_patients'])
print('Gross Revenue (M)     :', round(k['total_revenue_inr']/1e6, 2))
print('Insurance Covered (M) :', round(k['total_insurance_inr']/1e6, 2))
print('Outstanding Dues (M)  :', round(k['total_outstanding_inr']/1e6, 2))
print('Estimated Collected(M):', round(k['estimated_collected_inr']/1e6, 2))
print('Collection Rate %     :', k['collection_rate_pct'])
print('Avg LOS (days)        :', k['avg_los_days'])
print('Emergency Admissions  :', k['emergency_admissions'])
print('Emergency Rate %      :', k['emergency_rate_pct'])
print('Incomplete month excl :', k['incomplete_final_month_excluded'])

print()
df = pd.read_csv('Processed Dataset/Admissions_cleaned.csv')
total_rev = df['Total_Amount'].sum()
outstanding = df['Outstanding_Balance'].sum()
collected = total_rev - outstanding
print('=== DASHBOARD CSV VERIFICATION ===')
print('Gross Revenue (M)     :', round(total_rev/1e6, 2))
print('Insurance Covered (M) :', round(df['Insurance_Cover'].sum()/1e6, 2))
print('Outstanding Dues (M)  :', round(outstanding/1e6, 2))
print('Estimated Collected(M):', round(collected/1e6, 2))
print('Collection Rate %     :', round(collected/total_rev*100, 1))
valid_los = df['Length_of_Stay_Days'].dropna()
print('Avg LOS valid (days)  :', round(valid_los.mean(), 2), '-- from', len(valid_los), 'valid records')
print('Invalid LOS records   :', df['Length_of_Stay_Days'].isna().sum())
