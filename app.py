import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Set Clinical Hospital Theme & Layout
st.set_page_config(
    page_title="MediPulse Enterprise | Hospital Operations Intelligence & Decision Command",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Modern Glassmorphism & High-Contrast Dark Clinical Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #0d1527 0%, #050811 100%);
        color: #f1f5f9;
    }

    /* Glassmorphic Command Header */
    .command-header {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 22px 28px;
        border-radius: 20px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
    }

    .command-title {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }

    .badge-pulse {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(20, 184, 166, 0.15);
        border: 1px solid rgba(45, 212, 191, 0.4);
        color: #2dd4bf;
        padding: 4px 14px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
    }

    /* Executive Glass KPI Cards */
    .glass-kpi {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 20px;
        position: relative;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }

    .glass-kpi:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 20px 30px -10px rgba(14, 165, 233, 0.15);
    }

    .kpi-tag {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
        margin-bottom: 6px;
    }

    .kpi-num {
        font-size: 30px;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.03em;
    }

    .kpi-trend {
        font-size: 12px;
        font-weight: 600;
        margin-top: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Custom Color Accents */
    .cyan-glow { color: #38bdf8; text-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }
    .teal-glow { color: #2dd4bf; text-shadow: 0 0 15px rgba(45, 212, 191, 0.3); }
    .emerald-glow { color: #34d399; text-shadow: 0 0 15px rgba(52, 211, 153, 0.3); }
    .amber-glow { color: #fbbf24; text-shadow: 0 0 15px rgba(251, 191, 36, 0.3); }
    .rose-glow { color: #f43f5e; text-shadow: 0 0 15px rgba(244, 63, 94, 0.3); }

    /* Glass Container Containers */
    .glass-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 22px;
        box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.4);
    }

    .card-heading {
        font-size: 17px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #090e17;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    .stSelectbox, .stMultiSelect {
        background-color: rgba(30, 41, 59, 0.5);
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
    st.error("⚠️ Inpatient Dataset missing! Run scripts/data_cleaning.py first.")
    st.stop()

# --- TOP GLASS CLINICAL HEADER ---
st.markdown("""
    <div class="command-header">
        <div>
            <div class="command-title">🏥 MediPulse Command Center</div>
            <div style="color: #94a3b8; font-size: 13px; font-weight: 500; margin-top: 4px;">
                Enterprise Healthcare Operations Intelligence & Real-Time Decision Analytics | Group 1
            </div>
        </div>
        <div class="badge-pulse">
            <div class="pulse-dot"></div> OPERATIONAL MODE: ACTIVE MONITORING
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION & FILTERS ---
st.sidebar.markdown("### 🎛️ Navigation & Controls")
nav_option = st.sidebar.radio("View Workspace", [
    "📊 Executive Command & Operations",
    "🛏️ Bed Capacity & Ward Heatmap",
    "💳 Financial Revenue & Dues Engine",
    "🧪 Diagnostic Labs & Pharmacy Analytics",
    "⚡ Predictive Length-of-Stay Decision Model"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Global Filters")

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

# Apply global filters
f_df = df.copy()
if dept_filter:
    f_df = f_df[f_df['Department'].isin(dept_filter)]
if ward_filter:
    f_df = f_df[f_df['Ward'].isin(ward_filter)]
if emergency_filter == "Emergency":
    f_df = f_df[f_df['Emergency'] == "Yes"]
elif emergency_filter == "Elective/Regular":
    f_df = f_df[f_df['Emergency'] == "No"]

# Shared Plotly Dark Theme Config
PLOTLY_THEME = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'family': 'Plus Jakarta Sans', 'color': '#94a3b8'},
    'xaxis': {'gridcolor': 'rgba(255,255,255,0.05)', 'zerolinecolor': 'rgba(255,255,255,0.05)'},
    'yaxis': {'gridcolor': 'rgba(255,255,255,0.05)', 'zerolinecolor': 'rgba(255,255,255,0.05)'}
}

# --- PAGE 1: EXECUTIVE COMMAND & OPERATIONS ---
if nav_option == "📊 Executive Command & Operations":
    st.markdown("### ⚡ Live Operational Performance Matrix")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""
            <div class="glass-kpi">
                <div class="kpi-tag">Total Inpatient Volume</div>
                <div class="kpi-num cyan-glow">{len(f_df):,}</div>
                <div class="kpi-trend" style="color:#38bdf8;">👥 {f_df['Patient_ID'].nunique():,} Unique Patients</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="glass-kpi">
                <div class="kpi-tag">Gross Revenue Billed</div>
                <div class="kpi-num teal-glow">₹{f_df['Total_Amount'].sum()/1e6:.1f}M</div>
                <div class="kpi-trend" style="color:#2dd4bf;">💳 Avg ₹{f_df['Total_Amount'].mean():,.0f}/Patient</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="glass-kpi">
                <div class="kpi-tag">Avg Length of Stay</div>
                <div class="kpi-num emerald-glow">{f_df['Length_of_Stay_Days'].mean():.1f} <span style="font-size:16px;">Days</span></div>
                <div class="kpi-trend" style="color:#34d399;">⏱️ Bed Turnaround Ratio</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="glass-kpi">
                <div class="kpi-tag">Emergency Critical Rate</div>
                <div class="kpi-num rose-glow">{(f_df['Emergency'].value_counts().get('Yes', 0)/len(f_df)*100 if len(f_df)>0 else 0):.1f}%</div>
                <div class="kpi-trend" style="color:#f43f5e;">🚨 {f_df['Emergency'].value_counts().get('Yes', 0):,} ER Cases</div>
            </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
            <div class="glass-kpi">
                <div class="kpi-tag">Net Pending Recovery</div>
                <div class="kpi-num amber-glow">₹{f_df['Outstanding_Balance'].sum()/1e6:.1f}M</div>
                <div class="kpi-trend" style="color:#fbbf24;">⚠️ Uncollected Balances</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-heading'><span>🏥 Department Admission Intake Load</span><span style='font-size:12px; color:#64748b;'>20 Clinical Specialties</span></div>", unsafe_allow_html=True)
        dept_counts = f_df['Department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Admissions']
        fig_dept = px.bar(dept_counts.head(10), x='Admissions', y='Department', orientation='h',
                          color='Admissions', color_continuous_scale='Teal', template='plotly_dark',
                          text='Admissions')
        fig_dept.update_traces(textposition='outside')
        fig_dept.update_layout(**PLOTLY_THEME, height=360, margin=dict(l=0,r=20,t=10,b=0))
        st.plotly_chart(fig_dept, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-heading'><span>📈 Inpatient Monthly Flow Trajectory</span><span style='font-size:12px; color:#64748b;'>Historical Volume</span></div>", unsafe_allow_html=True)
        f_df['Month_Year'] = f_df['Admission_Date'].dt.to_period('M').astype(str)
        monthly_df = f_df.groupby('Month_Year')['Admission_ID'].count().reset_index()
        fig_monthly = px.area(monthly_df, x='Month_Year', y='Admission_ID',
                              labels={'Admission_ID': 'Admissions'}, template='plotly_dark',
                              color_discrete_sequence=['#38bdf8'])
        fig_monthly.update_layout(**PLOTLY_THEME, height=360, margin=dict(l=0,r=10,t=10,b=0))
        st.plotly_chart(fig_monthly, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2: BED CAPACITY & WARD HEATMAP ---
elif nav_option == "🛏️ Bed Capacity & Ward Heatmap":
    st.markdown("### 🛏️ Hospital Ward Occupancy & Bed Utilization Matrix")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-heading'><span>🏨 Ward Occupancy Breakdown</span></div>", unsafe_allow_html=True)
        ward_df = f_df['Ward'].value_counts().reset_index()
        ward_df.columns = ['Ward', 'Count']
        fig_ward = px.pie(ward_df, values='Count', names='Ward', hole=0.55,
                          color_discrete_sequence=['#0f766e', '#0284c7', '#d97706', '#818cf8'],
                          template='plotly_dark')
        fig_ward.update_layout(**PLOTLY_THEME, height=340)
        st.plotly_chart(fig_ward, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-heading'><span>🚪 Room Accommodation Split</span></div>", unsafe_allow_html=True)
        room_df = f_df['Room_Type'].value_counts().reset_index()
        room_df.columns = ['Room_Type', 'Count']
        fig_room = px.bar(room_df, x='Room_Type', y='Count', color='Room_Type',
                          color_discrete_sequence=['#2dd4bf', '#38bdf8', '#fbbf24'],
                          template='plotly_dark')
        fig_room.update_layout(**PLOTLY_THEME, height=340)
        st.plotly_chart(fig_room, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-heading'><span>🔥 Department vs. Ward Occupancy Matrix (Heatmap)</span></div>", unsafe_allow_html=True)
    heatmap_data = pd.crosstab(f_df['Department'], f_df['Ward'])
    fig_heat = px.imshow(heatmap_data, text_auto=True, aspect="auto", color_continuous_scale="Viridis", template='plotly_dark')
    fig_heat.update_layout(**PLOTLY_THEME, height=420)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3: FINANCIAL REVENUE & DUES ENGINE ---
elif nav_option == "💳 Financial Revenue & Dues Engine":
    st.markdown("### 💳 Revenue Cycle & Insurance Claim Recovery Analytics")
    
    f1, f2, f3 = st.columns(3)
    with f1:
        st.metric("Total Billed Revenue", f"₹{f_df['Total_Amount'].sum():,.2f}")
    with f2:
        st.metric("Insurance Claim Cover", f"₹{f_df['Insurance_Cover'].sum():,.2f}")
    with f3:
        st.metric("Net Pending Patient Dues", f"₹{f_df['Outstanding_Balance'].sum():,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-heading'><span>📊 Payment Settlement Status</span></div>", unsafe_allow_html=True)
        pay_df = f_df['Payment_Status'].value_counts().reset_index()
        pay_df.columns = ['Status', 'Count']
        fig_pay = px.pie(pay_df, values='Count', names='Status', color='Status',
                         color_discrete_map={'Paid': '#10b981', 'Partial': '#f59e0b', 'Pending': '#ef4444'},
                         template='plotly_dark')
        fig_pay.update_layout(**PLOTLY_THEME, height=350)
        st.plotly_chart(fig_pay, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-heading'><span>💰 Revenue Contribution by Department</span></div>", unsafe_allow_html=True)
        rev_dept = f_df.groupby('Department')['Total_Amount'].sum().reset_index().sort_values('Total_Amount', ascending=False)
        fig_rev = px.bar(rev_dept.head(10), x='Total_Amount', y='Department', orientation='h',
                         color='Total_Amount', color_continuous_scale='Purples', template='plotly_dark')
        fig_rev.update_layout(**PLOTLY_THEME, height=350)
        st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 4: DIAGNOSTIC LABS & PHARMACY ---
elif nav_option == "🧪 Diagnostic Labs & Pharmacy Analytics":
    st.markdown("### 🧪 Pathology Diagnostic Demand & Pharmacy Distribution")
    
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-heading'><span>📋 Top 10 Clinical Diagnoses Load</span></div>", unsafe_allow_html=True)
        diag_df = f_df['Diagnosis'].value_counts().head(10).reset_index()
        diag_df.columns = ['Diagnosis', 'Count']
        fig_diag = px.bar(diag_df, x='Count', y='Diagnosis', orientation='h', color='Count',
                          color_continuous_scale='Blues', template='plotly_dark')
        fig_diag.update_layout(**PLOTLY_THEME, height=360)
        st.plotly_chart(fig_diag, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with d2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-heading'><span>💊 Top Prescribed Medications</span></div>", unsafe_allow_html=True)
        med_df = f_df['Medicine'].value_counts().head(10).reset_index()
        med_df.columns = ['Medicine', 'Count']
        fig_med = px.bar(med_df, x='Count', y='Medicine', orientation='h', color='Count',
                         color_continuous_scale='Greens', template='plotly_dark')
        fig_med.update_layout(**PLOTLY_THEME, height=360)
        st.plotly_chart(fig_med, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 5: PREDICTIVE LOS DECISION MODEL ---
elif nav_option == "⚡ Predictive Length-of-Stay Decision Model":
    st.markdown("### ⚙️ Executive Decision Analytics & Length-of-Stay Simulator")
    st.markdown("Simulate capacity optimization scenarios to project bed-days saved, operational cost reductions, and emergency throughput.")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🎛️ Simulation Parameters")
        target_los_reduction = st.slider("Target Inpatient Length-of-Stay Reduction (%)", 0, 40, 15)
        bed_day_cost = st.number_input("Average Operational Cost per Bed-Day (₹)", 1000, 25000, 5000)
        est_daily_er_turnaround = st.slider("Target ER Discharge Efficiency Gain (%)", 0, 30, 10)
        
    total_days = f_df['Length_of_Stay_Days'].sum()
    bed_days_saved = total_days * (target_los_reduction / 100.0)
    cost_saved = bed_days_saved * bed_day_cost
    extra_capacity = int(bed_days_saved / max(1, f_df['Length_of_Stay_Days'].mean()))

    with c2:
        st.markdown("#### 📈 Projected Executive ROI & Impact")
        st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.9); border-radius: 14px; padding: 22px; border: 1px solid rgba(56, 189, 248, 0.3);">
                <div style="color: #94a3b8; font-size: 12px; font-weight: 700; text-transform: uppercase;">PROJECTED BED-DAYS SAVED</div>
                <div style="color: #38bdf8; font-size: 32px; font-weight: 800; font-family:'JetBrains Mono';">{bed_days_saved:,.0f} Days</div>
                <hr style="border-color: rgba(255,255,255,0.08); margin: 12px 0;">
                <div style="color: #94a3b8; font-size: 12px; font-weight: 700; text-transform: uppercase;">ESTIMATED OPERATIONAL FINANCIAL SAVINGS</div>
                <div style="color: #34d399; font-size: 32px; font-weight: 800; font-family:'JetBrains Mono';">₹{cost_saved:,.2f}</div>
                <hr style="border-color: rgba(255,255,255,0.08); margin: 12px 0;">
                <div style="color: #94a3b8; font-size: 12px; font-weight: 700; text-transform: uppercase;">ADDITIONAL PATIENT INTAKE CAPACITY</div>
                <div style="color: #fbbf24; font-size: 24px; font-weight: 800; font-family:'JetBrains Mono';">+{extra_capacity:,} Patients</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("⚡ MediPulse Enterprise Command | Group 1 Decision Analytics")
