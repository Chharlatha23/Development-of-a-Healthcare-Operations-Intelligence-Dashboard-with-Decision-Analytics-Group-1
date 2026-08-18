import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

targets = [
    'Out-of-Pocket Payments',
    'Intensive Care',
    'Ward Occupancy',
    'Ward Admission',
    'Most Utilized Room',
    'Most Common Room',
    'Admission_ID',
    'Month_Year',
    'Payment Settlement',
    'Payment Status',
    'Emergency Critical',
    'Critical ER',
    'Inpatient ER Turnaround',
    'Turnaround',
    'Critical Intake',
    'Total Pathology',
    'Diagnosis Records',
    'Simulate capacity',
    'Simulate length',
    'Additional Patient Intake',
    'Additional Admission',
    'Predictive',
    'Bed Turnaround',
    'chart_title',
    'Occupancy',
]
for i, line in enumerate(lines, 1):
    for t in targets:
        if t.lower() in line.lower():
            print(f'L{i}: [{t}] -> {line.rstrip()}')
            break
