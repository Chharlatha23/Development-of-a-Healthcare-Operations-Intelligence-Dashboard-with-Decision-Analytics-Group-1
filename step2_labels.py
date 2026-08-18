"""
Step 2: Terminology-only corrections to app.py.
No calculations, datasets, or chart types are changed.
"""

with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()

original = c  # keep a copy to diff at the end

# ────────────────────────────────────────────────────────────────────────────
# 1. REVENUE PAGE
# ────────────────────────────────────────────────────────────────────────────
# Sub-label under Estimated Collected Amount
c = c.replace(
    '<div class="kpi-card-sub">💵 Out-of-Pocket Payments</div>',
    '<div class="kpi-card-sub">💵 Estimated Amount Collected</div>'
)

# ────────────────────────────────────────────────────────────────────────────
# 2. PAYMENT CHART TITLE
# ────────────────────────────────────────────────────────────────────────────
c = c.replace(
    '💳 Payment Settlement Lifecycle',
    '💳 Payment Status Distribution'
)

# ────────────────────────────────────────────────────────────────────────────
# 3. BED & WARD PAGE
# ────────────────────────────────────────────────────────────────────────────
# "Most Utilized Room" KPI label → "Most Common Room Type"
c = c.replace(
    '<div class="kpi-card-label">Most Utilized Room</div>',
    '<div class="kpi-card-label">Most Common Room Type</div>'
)

# Insight item: "Intensive Care Occupants" → "Intensive Care Admissions"
c = c.replace(
    '🚨 Intensive Care Occupants',
    '🚨 Intensive Care Admissions'
)

# ────────────────────────────────────────────────────────────────────────────
# 4. PATIENT FLOW PAGE — axis labels only (NOT column names)
# ────────────────────────────────────────────────────────────────────────────
# Executive Overview monthly chart labels (px.area)
c = c.replace(
    "labels={'Admission_ID': 'Admissions'}",
    "labels={'Admission_ID': 'Admissions', 'Month_Year': 'Admission Month'}"
)

# Patient Flow monthly line chart (px.line) — add/set labels
# The px.line call does not yet have a labels arg; add it
c = c.replace(
    "fig_flow = px.line(monthly_flow_df, x='Month_Year', y='Admission_ID', markers=True, color_discrete_sequence=['#0284c7'])",
    "fig_flow = px.line(monthly_flow_df, x='Month_Year', y='Admission_ID', markers=True, color_discrete_sequence=['#0284c7'], labels={'Admission_ID': 'Admissions', 'Month_Year': 'Admission Month'})"
)

# ────────────────────────────────────────────────────────────────────────────
# 5. MISLEADING "TURNAROUND" SUBTITLES
# ────────────────────────────────────────────────────────────────────────────
# Executive Overview KPI sub for Avg LOS
c = c.replace(
    '<div class="kpi-card-sub">⏱️ Bed Turnaround Ratio</div>',
    '<div class="kpi-card-sub">⏱️ Average Hospital Stay</div>'
)

# Patient Flow KPI sub
c = c.replace(
    '<div class="kpi-card-sub">⏱️ Turnaround Duration</div>',
    '<div class="kpi-card-sub">⏱️ Average Hospital Stay</div>'
)

# Emergency page: "Inpatient ER Turnaround" KPI sub
c = c.replace(
    '<div class="kpi-card-sub">⏱️ Inpatient ER Turnaround</div>',
    '<div class="kpi-card-sub">⏱️ Avg LOS for Emergency Admissions</div>'
)

# ────────────────────────────────────────────────────────────────────────────
# 6. LOS SIMULATOR
# ────────────────────────────────────────────────────────────────────────────
# "ADDITIONAL PATIENT INTAKE CAPACITY" → "ESTIMATED ADDITIONAL ADMISSION CAPACITY"
c = c.replace(
    'ADDITIONAL PATIENT INTAKE CAPACITY',
    'ESTIMATED ADDITIONAL ADMISSION CAPACITY'
)

# ────────────────────────────────────────────────────────────────────────────
# Write back
# ────────────────────────────────────────────────────────────────────────────
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)

# Report changes
changed_lines = []
orig_lines = original.splitlines()
new_lines  = c.splitlines()
for i, (o, n) in enumerate(zip(orig_lines, new_lines), 1):
    if o != n:
        changed_lines.append(f'  L{i}: {o.strip()!r}')
        changed_lines.append(f'    -> {n.strip()!r}')

print(f'Total lines changed: {len(changed_lines)//2}')
for cl in changed_lines:
    print(cl)
