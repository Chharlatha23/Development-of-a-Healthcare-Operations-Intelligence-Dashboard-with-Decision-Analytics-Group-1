import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Set Clinical Hospital Theme & Layout
st.set_page_config(
    page_title="MediPulse Hospital Analytics | Clinical Operations",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Clean Hospital Theme CSS (WCAG Accessible, High Contrast Light Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Base Font & Page Reset */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    /* Reduce Wasted White Space at Top */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Clean Enterprise Hospital Header */
    .hospital-header-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .hospital-header-title {
        color: #0f172a;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .hospital-header-subtitle {
        color: #475569;
        font-size: 13px;
        font-weight: 500;
        margin-top: 4px;
    }

    .status-badge-live {
        background-color: #f0fdf4;
        color: #166534;
        border: 1px solid #bbf7d0;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .status-dot-green {
        width: 8px;
        height: 8px;
        background-color: #16a34a;
        border-radius: 50%;
    }

    /* Clean White KPI Metric Cards */
    .hospital-kpi-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0284c7; /* Primary Medical Blue */
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        height: 100%;
    }

    .hospital-kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.05);
    }

    .hospital-kpi-card-rose {
        border-left-color: #e11d48 !important; /* Critical Emergency Red */
    }

    .hospital-kpi-card-teal {
        border-left-color: #0d9488 !important; /* Medical Teal */
    }

    .hospital-kpi-card-amber {
        border-left-color: #d97706 !important; /* Warning Amber */
    }

    .kpi-card-label {
        font-size: 11px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }

    .kpi-card-value {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
    }

    .kpi-card-value-rose {
        color: #be123c;
    }

    .kpi-card-sub {
        font-size: 12px;
        font-weight: 500;
        color: #64748b;
        margin-top: 4px;
    }

    /* White Section Card Containers for Charts */
    .chart-container-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }

    .chart-card-title {
        font-size: 16px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Clean Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #0f172a !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }

    /* High Contrast Text overrides for Filter elements */
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    
    /* Ensure Streamlit Widgets blend into light medical theme */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
    }
    
    div[data-baseweb="select"] span {
        color: #0f172a !important;
    }

    hr {
        border-color: #e2e8f0 !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    path = "Processed Dataset/Admissions_cleaned.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
        df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])
        return df
    return None

df = load_data()

if df is None:
    st.error("⚠️ Hospital Clinical Dataset Not Found! Please verify data pipeline.")
    st.stop()

# --- PROFESSIONAL CLEAN HOSPITAL HEADER ---
st.markdown("""
    <div class="hospital-header-card">
        <div>
            <div class="hospital-header-title">
                🏥 MediPulse Hospital Analytics
            </div>
            <div class="hospital-header-subtitle">
                Hospital Operations | Patient Flow | Emergency Care | Financial Analytics
            </div>
        </div>
        <div>
            <span class="status-badge-live">
                <span class="status-dot-green"></span> Hospital Operations: Live
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION & HOSPITAL FILTERS ---
st.sidebar.markdown("## 🏥 MediPulse")
st.sidebar.markdown("**Hospital Analytics**")
st.sidebar.markdown("---")

st.sidebar.markdown("### Operations")
op_nav = st.sidebar.radio(
    "Select Operational View",
    [
        "Executive Overview",
        "Bed Capacity & Ward Analytics",
        "Patient Flow"
    ],
    key="op_nav"
)

st.sidebar.markdown("### Finance")
fin_nav = st.sidebar.radio(
    "Select Financial View",
    ["Revenue & Dues"],
    key="fin_nav"
)

st.sidebar.markdown("### Clinical")
clin_nav = st.sidebar.radio(
    "Select Clinical View",
    ["Diagnostic Labs & Pharmacy", "Emergency Analytics"],
    key="clin_nav"
)

st.sidebar.markdown("### Predictive Analytics")
pred_nav = st.sidebar.radio(
    "Select Analytics View",
    ["Length-of-Stay Prediction"],
    key="pred_nav"
)

# Active Page Logic
active_page = op_nav
# Determine active radio by checking user interaction focus
ctx = st.session_state
if "last_clicked" not in ctx:
    ctx.last_clicked = "Executive Overview"

# Combine radio navigation selections cleanly
nav_choice = op_nav

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔎 Hospital Filters")

dept_filter = st.sidebar.multiselect(
    "Clinical Department",
    options=sorted(df['Department'].dropna().unique().tolist()),
    default=[]
)

ward_filter = st.sidebar.multiselect(
    "Hospital Ward",
    options=sorted(df['Ward'].dropna().unique().tolist()),
    default=[]
)

emergency_filter = st.sidebar.selectbox(
    "Admission Emergency Status",
    options=["All Statuses", "Emergency", "Elective/Regular"]
)

# Apply global dataset filters without altering calculations
f_df = df.copy()
if dept_filter:
    f_df = f_df[f_df['Department'].isin(dept_filter)]
if ward_filter:
    f_df = f_df[f_df['Ward'].isin(ward_filter)]
if emergency_filter == "Emergency":
    f_df = f_df[f_df['Emergency'] == "Yes"]
elif emergency_filter == "Elective/Regular":
    f_df = f_df[f_df['Emergency'] == "No"]

# Shared Plotly Light Theme Config for Clear Visual Readability
PLOTLY_LIGHT_THEME = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'family': 'Inter, sans-serif', 'color': '#334155'},
    'xaxis': {'gridcolor': '#f1f5f9', 'zerolinecolor': '#e2e8f0', 'tickfont': {'color': '#475569'}},
    'yaxis': {'gridcolor': '#f1f5f9', 'zerolinecolor': '#e2e8f0', 'tickfont': {'color': '#475569'}}
}

# --- EXECUTIVE OVERVIEW PAGE ---
if op_nav == "Executive Overview":
    # 5 KPI METRIC CARDS ROW
    k1, k2, k3, k4, k5 = st.columns(5)
    
    with k1:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Total Inpatients</div>
                <div class="kpi-card-value">{len(f_df):,}</div>
                <div class="kpi-card-sub">👥 {f_df['Patient_ID'].nunique():,} Unique Patients</div>
            </div>
        """, unsafe_allow_html=True)
        
    with k2:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-teal">
                <div class="kpi-card-label">Gross Revenue</div>
                <div class="kpi-card-value">₹{f_df['Total_Amount'].sum()/1e6:.1f}M</div>
                <div class="kpi-card-sub">💳 Avg ₹{f_df['Total_Amount'].mean():,.0f} / Patient</div>
            </div>
        """, unsafe_allow_html=True)
        
    with k3:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Average Length of Stay</div>
                <div class="kpi-card-value">{f_df['Length_of_Stay_Days'].mean():.1f} <span style="font-size:14px; font-weight:600;">Days</span></div>
                <div class="kpi-card-sub">⏱️ Bed Turnaround Ratio</div>
            </div>
        """, unsafe_allow_html=True)
        
    with k4:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-rose">
                <div class="kpi-card-label">Emergency Critical Rate</div>
                <div class="kpi-card-value kpi-card-value-rose">{(f_df['Emergency'].value_counts().get('Yes', 0)/len(f_df)*100 if len(f_df)>0 else 0):.1f}%</div>
                <div class="kpi-card-sub">🚑 {f_df['Emergency'].value_counts().get('Yes', 0):,} ER Cases</div>
            </div>
        """, unsafe_allow_html=True)
        
    with k5:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-amber">
                <div class="kpi-card-label">Pending Recovery</div>
                <div class="kpi-card-value">₹{f_df['Outstanding_Balance'].sum()/1e6:.1f}M</div>
                <div class="kpi-card-sub">⚠️ Uncollected Balances</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.2, 1])
    with col_left:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>🏥 Department Admission Intake</span><span style='font-size:12px; color:#64748b;'>Top Specialties</span></div>", unsafe_allow_html=True)
        dept_counts = f_df['Department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Admissions']
        fig_dept = px.bar(
            dept_counts.head(10), x='Admissions', y='Department', orientation='h',
            color='Admissions', color_continuous_scale='Blues', text='Admissions'
        )
        fig_dept.update_traces(textposition='outside', marker_line_color='#0284c7', marker_line_width=1)
        fig_dept.update_layout(**PLOTLY_LIGHT_THEME, height=360, margin=dict(l=0, r=20, t=10, b=0))
        st.plotly_chart(fig_dept, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>📈 Inpatient Monthly Flow</span><span style='font-size:12px; color:#64748b;'>Volume Trends</span></div>", unsafe_allow_html=True)
        f_df['Month_Year'] = f_df['Admission_Date'].dt.to_period('M').astype(str)
        monthly_df = f_df.groupby('Month_Year')['Admission_ID'].count().reset_index()
        fig_monthly = px.area(
            monthly_df, x='Month_Year', y='Admission_ID',
            labels={'Admission_ID': 'Admissions'}, color_discrete_sequence=['#0284c7']
        )
        fig_monthly.update_layout(**PLOTLY_LIGHT_THEME, height=360, margin=dict(l=0, r=10, t=10, b=0))
        st.plotly_chart(fig_monthly, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- BED CAPACITY & WARD ANALYTICS PAGE ---
elif op_nav == "Bed Capacity & Ward Analytics":
    st.markdown("### 🛏️ Hospital Ward Capacity & Accommodation Matrix")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>🏨 Ward Occupancy Breakdown</span></div>", unsafe_allow_html=True)
        ward_df = f_df['Ward'].value_counts().reset_index()
        ward_df.columns = ['Ward', 'Count']
        fig_ward = px.pie(
            ward_df, values='Count', names='Ward', hole=0.5,
            color_discrete_sequence=['#0284c7', '#0d9488', '#d97706', '#6366f1']
        )
        fig_ward.update_layout(**PLOTLY_LIGHT_THEME, height=340)
        st.plotly_chart(fig_ward, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>🚪 Room Type Accommodation Split</span></div>", unsafe_allow_html=True)
        room_df = f_df['Room_Type'].value_counts().reset_index()
        room_df.columns = ['Room_Type', 'Count']
        fig_room = px.bar(
            room_df, x='Room_Type', y='Count', color='Room_Type',
            color_discrete_sequence=['#0ea5e9', '#14b8a6', '#f59e0b']
        )
        fig_room.update_layout(**PLOTLY_LIGHT_THEME, height=340)
        st.plotly_chart(fig_room, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-card-title'><span>🔥 Department vs. Ward Occupancy Matrix (Heatmap)</span></div>", unsafe_allow_html=True)
    heatmap_data = pd.crosstab(f_df['Department'], f_df['Ward'])
    fig_heat = px.imshow(heatmap_data, text_auto=True, aspect="auto", color_continuous_scale="Blues")
    fig_heat.update_layout(**PLOTLY_LIGHT_THEME, height=400)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- REVENUE & DUES PAGE ---
elif fin_nav == "Revenue & Dues":
    st.markdown("### 💰 Financial Revenue Cycle & Dues Recovery")
    
    f1, f2, f3 = st.columns(3)
    with f1:
        st.metric("Gross Billed Revenue", f"₹{f_df['Total_Amount'].sum():,.2f}")
    with f2:
        st.metric("Insurance Covered Claims", f"₹{f_df['Insurance_Cover'].sum():,.2f}")
    with f3:
        st.metric("Net Pending Dues", f"₹{f_df['Outstanding_Balance'].sum():,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>💳 Payment Settlement Lifecycle</span></div>", unsafe_allow_html=True)
        pay_df = f_df['Payment_Status'].value_counts().reset_index()
        pay_df.columns = ['Status', 'Count']
        fig_pay = px.pie(
            pay_df, values='Count', names='Status', color='Status',
            color_discrete_map={'Paid': '#16a34a', 'Partial': '#d97706', 'Pending': '#dc2626'}
        )
        fig_pay.update_layout(**PLOTLY_LIGHT_THEME, height=350)
        st.plotly_chart(fig_pay, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>🏛️ Revenue Contribution by Department</span></div>", unsafe_allow_html=True)
        rev_dept = f_df.groupby('Department')['Total_Amount'].sum().reset_index().sort_values('Total_Amount', ascending=False)
        fig_rev = px.bar(
            rev_dept.head(10), x='Total_Amount', y='Department', orientation='h',
            color='Total_Amount', color_continuous_scale='Blues'
        )
        fig_rev.update_layout(**PLOTLY_LIGHT_THEME, height=350)
        st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- DIAGNOSTICS & PHARMACY PAGE ---
elif clin_nav == "Diagnostic Labs & Pharmacy" or clin_nav == "Emergency Analytics":
    st.markdown("### 🧪 Diagnostic Lab Utilization & Pharmacy Demand")
    
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>📋 Top 10 Clinical Diagnoses</span></div>", unsafe_allow_html=True)
        diag_df = f_df['Diagnosis'].value_counts().head(10).reset_index()
        diag_df.columns = ['Diagnosis', 'Count']
        fig_diag = px.bar(
            diag_df, x='Count', y='Diagnosis', orientation='h', color='Count',
            color_continuous_scale='Blues'
        )
        fig_diag.update_layout(**PLOTLY_LIGHT_THEME, height=360)
        st.plotly_chart(fig_diag, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with d2:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>💊 Top Prescribed Medications</span></div>", unsafe_allow_html=True)
        med_df = f_df['Medicine'].value_counts().head(10).reset_index()
        med_df.columns = ['Medicine', 'Count']
        fig_med = px.bar(
            med_df, x='Count', y='Medicine', orientation='h', color='Count',
            color_continuous_scale='Teal'
        )
        fig_med.update_layout(**PLOTLY_LIGHT_THEME, height=360)
        st.plotly_chart(fig_med, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PREDICTIVE DECISION MODEL PAGE ---
elif pred_nav == "Length-of-Stay Prediction":
    st.markdown("### ⚙️ Length-of-Stay Decision Analytics & Simulation")
    st.markdown("Simulate capacity optimization scenarios to project bed-days saved, operational cost reductions, and emergency throughput.")
    
    st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🎛️ Simulation Parameters")
        target_los_reduction = st.slider("Target Inpatient Length-of-Stay Reduction (%)", 0, 40, 15)
        bed_day_cost = st.number_input("Average Operational Cost per Bed-Day (₹)", 1000, 25000, 5000)
        
    total_days = f_df['Length_of_Stay_Days'].sum()
    bed_days_saved = total_days * (target_los_reduction / 100.0)
    cost_saved = bed_days_saved * bed_day_cost
    extra_capacity = int(bed_days_saved / max(1, f_df['Length_of_Stay_Days'].mean()))

    with c2:
        st.markdown("#### 📈 Projected Executive ROI & Impact")
        st.markdown(f"""
            <div style="background: #f8fafc; border-radius: 10px; padding: 20px; border: 1px solid #cbd5e1;">
                <div style="color: #475569; font-size: 11px; font-weight: 700; text-transform: uppercase;">PROJECTED BED-DAYS SAVED</div>
                <div style="color: #0284c7; font-size: 28px; font-weight: 800;">{bed_days_saved:,.0f} Days</div>
                <hr style="border-color: #e2e8f0; margin: 10px 0;">
                <div style="color: #475569; font-size: 11px; font-weight: 700; text-transform: uppercase;">ESTIMATED OPERATIONAL FINANCIAL SAVINGS</div>
                <div style="color: #16a34a; font-size: 28px; font-weight: 800;">₹{cost_saved:,.2f}</div>
                <hr style="border-color: #e2e8f0; margin: 10px 0;">
                <div style="color: #475569; font-size: 11px; font-weight: 700; text-transform: uppercase;">ADDITIONAL PATIENT INTAKE CAPACITY</div>
                <div style="color: #d97706; font-size: 22px; font-weight: 800;">+{extra_capacity:,} Patients</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("🏥 MediPulse Hospital Analytics | Group 1")
