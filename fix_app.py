import pandas as pd
import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Financial Settlement Logic
c = c.replace(
    '''    total_rev = f_df['Total_Amount'].sum() if len(f_df) > 0 else 0\n    ins_cover = f_df['Insurance_Cover'].sum() if len(f_df) > 0 else 0\n    patient_paid = f_df['Patient_Paid'].sum() if len(f_df) > 0 else 0\n    pending_dues = f_df['Outstanding_Balance'].sum() if len(f_df) > 0 else 0\n    settlement_rate = ((ins_cover + patient_paid) / max(1, total_rev) * 100)''',
    '''    total_rev = f_df['Total_Amount'].sum() if len(f_df) > 0 else 0\n    ins_cover = f_df['Insurance_Cover'].sum() if len(f_df) > 0 else 0\n    pending_dues = f_df['Outstanding_Balance'].sum() if len(f_df) > 0 else 0\n    patient_paid = max(0, total_rev - ins_cover - pending_dues) if len(f_df) > 0 else 0\n    settlement_rate = ((ins_cover + patient_paid) / max(1, total_rev)) * 100'''
)

# 2. Fix 'Pending Recovery' -> 'Outstanding Dues'
c = c.replace('<div class="kpi-card-label">Pending Recovery</div>', '<div class="kpi-card-label">Outstanding Dues</div>')

# 3. Emergency Terminology
c = c.replace('<div class="kpi-card-label">Emergency Critical Rate</div>', '<div class="kpi-card-label">Emergency Admission Rate</div>')
c = c.replace('ER Cases</div>', 'Emergency Cases</div>')
c = c.replace('🚑 Critical ER Rate', '🚑 Emergency Admission Rate')
c = c.replace('🚑 Critical Intake Rate', '🚑 Emergency Admission Rate')
c = c.replace('🚨 Critical Inpatient Volume', '🚨 Emergency Inpatient Volume')
c = c.replace('🚑 Critical vs Elective Split', '🚑 Emergency vs Elective Split')

# 4. Bed Occupancy Terminology
c = c.replace('<div class="kpi-card-label">Active Tracked Beds</div>', '<div class="kpi-card-label">Unique Beds in Records</div>')
c = c.replace('<div class="kpi-card-label">Highest Occupancy Ward</div>', '<div class="kpi-card-label">Highest Admission-Volume Ward</div>')
c = c.replace('<div class="kpi-card-label">ICU Ward Cases</div>', '<div class="kpi-card-label">ICU Admissions</div>')
c = c.replace('🔥 Department vs. Ward Occupancy Matrix (Heatmap)', '🔥 Department vs. Ward Admission Volume (Heatmap)')

# 5. Length of Stay Terminology
c = c.replace('Predictive Length-of-Stay Dashboard', 'Length-of-Stay Reduction Simulator')
c = c.replace('Length-of-Stay Prediction', 'Length-of-Stay Reduction Simulator')
c = c.replace('Predictive Analytics', 'Decision Analytics')

# 6. Additional Capacity
c = c.replace('Additional Patient Intake Capacity', 'Estimated Additional Admission Capacity')

# 7. Diagnostic Terminology
c = c.replace('Total Pathology Tests', 'Diagnosis Records')
c = c.replace('Total Pathology Records', 'Diagnosis Records') 

# 8. Incomplete Month & Daily Average Intake logic
# For Executive Overview:
c = c.replace(
    '''        # Exclude incomplete final month (2026-06) for accurate trend representation\n        complete_monthly_df = f_df[f_df['Month_Year'] != '2026-06'].groupby('Month_Year')['Admission_ID'].count().reset_index()''',
    '''        # Exclude incomplete final month dynamically for accurate trend representation\n        max_date = f_df['Admission_Date'].max()\n        import calendar\n        is_complete = (max_date.day == calendar.monthrange(max_date.year, max_date.month)[1]) if pd.notna(max_date) else True\n        complete_monthly_df = f_df[f_df['Month_Year'] != max_date.strftime('%Y-%m')].groupby('Month_Year')['Admission_ID'].count().reset_index() if not is_complete else f_df.groupby('Month_Year')['Admission_ID'].count().reset_index()'''
)
# For Patient Flow:
c = c.replace(
    '''    complete_monthly = f_df[f_df['Month_Year'] != '2026-06']''',
    '''    max_date = f_df['Admission_Date'].max()\n    import calendar\n    is_complete = (max_date.day == calendar.monthrange(max_date.year, max_date.month)[1]) if pd.notna(max_date) else True\n    complete_monthly = f_df[f_df['Month_Year'] != max_date.strftime('%Y-%m')] if not is_complete else f_df'''
)
c = c.replace(
    '''    avg_daily_intake = round(len(complete_monthly) / max(1, complete_monthly['Month_Year'].nunique() * 30), 1)''',
    '''    if len(complete_monthly) > 0:\n        date_range = (complete_monthly['Admission_Date'].max() - complete_monthly['Admission_Date'].min()).days + 1\n        avg_daily_intake = round(len(complete_monthly) / max(1, date_range), 1)\n    else:\n        avg_daily_intake = 0'''
)

# 10. Executive Overview Top Department logic
c = c.replace(
    '''    top_dept_name = dept_counts.iloc[0]['Department'] if len(dept_counts) > 0 else "N/A"''',
    '''    if len(dept_counts) > 0:\n        max_admissions = dept_counts['Admissions'].max()\n        top_depts = dept_counts[dept_counts['Admissions'] == max_admissions]['Department'].tolist()\n        top_dept_name = " & ".join(top_depts)\n    else:\n        top_dept_name = "N/A"'''
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')
