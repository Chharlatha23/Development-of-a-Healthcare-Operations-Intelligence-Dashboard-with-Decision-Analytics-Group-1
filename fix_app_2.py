import re

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 4. FIX REMAINING BED OCCUPANCY TERMINOLOGY
c = c.replace('Intensive Care Occupancy', 'Intensive Care Admissions')
c = c.replace('Ward Occupancy Breakdown', 'Ward Admission Volume')

# 5. FIX LOS SIMULATOR DESCRIPTION
c = c.replace(
    'Simulate capacity optimization scenarios to project bed-days saved, operational cost reductions, and emergency throughput.',
    'Simulate length-of-stay reduction scenarios to estimate bed-days saved, operational cost savings, and additional admission capacity.'
)

# 1. FIX FINANCIAL TERMINOLOGY AND SETTLEMENT LOGIC
c = c.replace(
    '''    total_rev = f_df['Total_Amount'].sum() if len(f_df) > 0 else 0\n    ins_cover = f_df['Insurance_Cover'].sum() if len(f_df) > 0 else 0\n    pending_dues = f_df['Outstanding_Balance'].sum() if len(f_df) > 0 else 0\n    patient_paid = max(0, total_rev - ins_cover - pending_dues) if len(f_df) > 0 else 0\n    settlement_rate = ((ins_cover + patient_paid) / max(1, total_rev)) * 100''',
    '''    total_rev = f_df['Total_Amount'].sum() if len(f_df) > 0 else 0\n    ins_cover = f_df['Insurance_Cover'].sum() if len(f_df) > 0 else 0\n    pending_dues = f_df['Outstanding_Balance'].sum() if len(f_df) > 0 else 0\n    collected_amount = max(0, total_rev - pending_dues) if len(f_df) > 0 else 0\n    settlement_rate = (collected_amount / max(1, total_rev)) * 100'''
)

c = c.replace('patient_paid', 'collected_amount')

c = c.replace('<div class="kpi-card-label">Patient Paid Amount</div>', '<div class="kpi-card-label">Estimated Collected Amount</div>')
c = c.replace('Claim Settlement Rate', 'Collection Rate')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')
