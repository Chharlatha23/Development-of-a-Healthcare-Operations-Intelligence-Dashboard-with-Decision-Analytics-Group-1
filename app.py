import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set Clinical Hospital Theme & Layout
st.set_page_config(
    page_title="MediPulse Intelligence | Hospital Operations Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Clinical Healthcare Styling (Clean Slate Teal & Medical Dark Navy Palette)
st.markdown("""
    <style>
    /* Global Font & Theme setup */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background-color: #090d16;
        color: #e2e8f0;
    }

    /* Hospital Header Bar */
    .hospital-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 50%, #0f766e 100%);
        padding: 24px 30px;
        border-radius: 16px;
        border: 1px solid #1e293b;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .hospital-title {
        color: #ffffff;
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hospital-badge {
        background: rgba(20, 184, 166, 0.2);
        color: #2dd4bf;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #14b8a6;
    }

    /* Clinical KPI Cards */
    .kpi-card {
        background: #111827;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #1f2937;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
        position: relative;
        overflow: hidden;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #0d9488;
    }

    .kpi-title {
        font-size: 13px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #38bdf8;
    }

    .kpi-sub {
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
    }
    
    .kpi-card-teal .kpi-value { color: #2dd4bf; }
    .kpi-card-emerald .kpi-value { color: #34d399; }
    .kpi-card-amber .kpi-value { color: #fbbf24; }
    .kpi-card-rose .kpi-value { color: #f43f5e; }

    /* Section Containers */
    .clinical-container {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Status indicators */
    .status-active {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #22c55e;
        border-radius: 50%;
        margin-right: 6px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    path = "Processed Dataset/Admissions_cleaned.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
        return df
    return None

df = load_data()

if df is None:
    st.error("⚠️ Hospital Clinical Dataset Not Found! Please verify data pipeline.")
    st.stop()

# --- TOP CLINICAL HEADER BAR ---
st.markdown("""
    <div class="hospital-header">
        <div>
            <div class="hospital-title">
                🏥 MediPulse Operations Command Center
                <span class="hospital-badge"><span class="status-active"></span>LIVE CLINICAL ANALYTICS</span>
            </div>
            <div style="color: #94a3b8; font-size: 14px; margin-top: 6px;">
                Healthcare Operations & Decision Intelligence System | Group 1
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.markdown("### 🎛️ Clinical Control Panel")
page = st.sidebar.radio("Navigate Command Center View", [
    "📋 Executive Operational Command",
    "🛏️ Bed Occupancy & Capacity",
    "💳 Patient Billing & Revenue Dues",
    "🧪 Diagnostic Labs & Pharmacy",
    "⚙️ Capacity Decision Simulator"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Operational Filters")

selected_departments = st.sidebar.multiselect(
    "Clinical Specialty/Dept",
    options=sorted(df['Department'].dropna().unique().tolist()),
    default=[]
)

selected_wards = st.sidebar.multiselect(
    "Hospital Ward Location",
    options=sorted(df['Ward'].dropna().unique().tolist()),
    default=[]
)

# Apply active filters
filtered_df = df.copy()
if selected_departments:
    filtered_df = filtered_df[filtered_df['Department'].isin(selected_departments)]
if selected_wards:
    filtered_df = filtered_df[filtered_df['Ward'].isin(selected_wards)]

# Color Palettes for Medical Charts
PL_TEAL = ['#0d9488', '#14b8a6', '#2dd4bf', '#5eead4', '#99f6e4']
PL_CLINICAL = ['#38bdf8', '#0284c7', '#0369a1', '#075985', '#0c4a6e']

# --- PAGE 1: EXECUTIVE COMMAND CENTER ---
if page == "📋 Executive Operational Command":
    st.markdown("### 📊 Real-Time Clinical Performance Indicators")
    
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f"""
            <div class="kpi-card kpi-card-teal">
                <div class="kpi-title">Total Active Patients</div>
                <div class="kpi-value">{filtered_df['Patient_ID'].nunique():,}</div>
                <div class="kpi-sub">Registered Records</div>
            </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
            <div class="kpi-card kpi-card-emerald">
                <div class="kpi-title">Total Billed Revenue</div>
                <div class="kpi-value">₹{filtered_df['Total_Amount'].sum()/1e6:.1f}M</div>
                <div class="kpi-sub">Gross Claims & Cash</div>
            </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Avg Length of Stay</div>
                <div class="kpi-value">{filtered_df['Length_of_Stay_Days'].mean():.1f} <span style="font-size:16px;">days</span></div>
                <div class="kpi-sub">Inpatient Turnaround</div>
            </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
            <div class="kpi-card kpi-card-rose">
                <div class="kpi-title">Emergency Admission</div>
                <div class="kpi-value">{(filtered_df['Emergency'].value_counts().get('Yes', 0)/len(filtered_df)*100 if len(filtered_df)>0 else 0):.1f}%</div>
                <div class="kpi-sub">Critical Intake Ratio</div>
            </div>
        """, unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
            <div class="kpi-card kpi-card-amber">
                <div class="kpi-title">Outstanding Recovery</div>
                <div class="kpi-value">₹{filtered_df['Outstanding_Balance'].sum()/1e6:.1f}M</div>
                <div class="kpi-sub">Net Dues Pending</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.markdown("<div class='clinical-container'>", unsafe_allow_html=True)
        st.markdown("#### 🏥 Top Clinical Specialty Load")
        dept_counts = filtered_df['Department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Admissions']
        fig_dept = px.bar(dept_counts.head(10), x='Admissions', y='Department', orientation='h',
                          color='Admissions', color_continuous_scale='Teal', template='plotly_dark')
        fig_dept.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig_dept, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_right:
        st.markdown("<div class='clinical-container'>", unsafe_allow_html=True)
        st.markdown("#### 📈 Hospital Inpatient Admission Flow")
        filtered_df['Month_Year'] = filtered_df['Admission_Date'].dt.to_period('M').astype(str)
        trend = filtered_df.groupby('Month_Year')['Admission_ID'].count().reset_index()
        fig_trend = px.area(trend, x='Month_Year', y='Admission_ID',
                            labels={'Admission_ID': 'Inpatients'}, template='plotly_dark', color_discrete_sequence=['#14b8a6'])
        fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2: BED OCCUPANCY & CAPACITY ---
elif page == "🛏️ Bed Occupancy & Capacity":
    st.markdown("### 🛏️ Hospital Ward & Bed Capacity Management")
    
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("<div class='clinical-container'>", unsafe_allow_html=True)
        st.markdown("#### 🏨 Ward Occupancy Allocation")
        ward_counts = filtered_df['Ward'].value_counts().reset_index()
        ward_counts.columns = ['Ward', 'Count']
        fig_ward = px.pie(ward_counts, values='Count', names='Ward', hole=0.5,
                          color_discrete_sequence=['#0f766e', '#0284c7', '#d97706'], template='plotly_dark')
        fig_ward.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_ward, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with b2:
        st.markdown("<div class='clinical-container'>", unsafe_allow_html=True)
        st.markdown("#### 🚪 Room Type Distribution")
        room_counts = filtered_df['Room_Type'].value_counts().reset_index()
        room_counts.columns = ['Room Type', 'Count']
        fig_room = px.bar(room_counts, x='Room Type', y='Count', color='Room Type',
                          color_discrete_sequence=['#14b8a6', '#38bdf8', '#fbbf24'], template='plotly_dark')
        fig_room.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_room, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<div class='clinical-container'>", unsafe_allow_html=True)
    st.markdown("#### ⏱️ Average Inpatient Length of Stay (LOS) by Specialty")
    los_dept = filtered_df.groupby('Department')['Length_of_Stay_Days'].mean().reset_index().sort_values('Length_of_Stay_Days', ascending=False)
    fig_los = px.bar(los_dept.head(12), x='Department', y='Length_of_Stay_Days', color='Length_of_Stay_Days',
                     color_continuous_scale='Blues', template='plotly_dark')
    fig_los.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_los, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3: PATIENT BILLING & REVENUE ---
elif page == "💳 Patient Billing & Revenue Dues":
    st.markdown("### 💳 Financial & Revenue Cycle Management")
    
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("<div class='clinical-container'>", unsafe_allow_html=True)
        st.markdown("#### 📊 Patient Payment Lifecycle Status")
        pay_status = filtered_df['Payment_Status'].value_counts().reset_index()
        pay_status.columns = ['Status', 'Admissions']
        fig_pay = px.pie(pay_status, values='Admissions', names='Status', color='Status',
                         color_discrete_map={'Paid': '#22c55e', 'Partial': '#eab308', 'Pending': '#ef4444'},
                         template='plotly_dark')
        fig_pay.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pay, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with f2:
        st.markdown("<div class='clinical-container'>", unsafe_allow_html=True)
        st.markdown("#### 💰 Revenue Generation by Department")
        rev_dept = filtered_df.groupby('Department')['Total_Amount'].sum().reset_index().sort_values('Total_Amount', ascending=False)
        fig_rev = px.bar(rev_dept.head(10), x='Total_Amount', y='Department', orientation='h',
                         color='Total_Amount', color_continuous_scale='Teal', template='plotly_dark')
        fig_rev.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 4: DIAGNOSTICS & PHARMACY ---
elif page == "🧪 Diagnostic Labs & Pharmacy":
    st.markdown("### 🧪 Diagnostic Lab Utilization & Pharmacy Demand")
    
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("<div class='clinical-container'>", unsafe_allow_html=True)
        st.markdown("#### 📋 Top 10 Clinical Diagnoses")
        diag_counts = filtered_df['Diagnosis'].value_counts().head(10).reset_index()
        diag_counts.columns = ['Diagnosis', 'Count']
        fig_diag = px.bar(diag_counts, x='Count', y='Diagnosis', orientation='h', color='Count',
                          color_continuous_scale='Purples', template='plotly_dark')
        fig_diag.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_diag, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with d2:
        st.markdown("<div class='clinical-container'>", unsafe_allow_html=True)
        st.markdown("#### 💊 Top Prescribed Medications")
        med_counts = filtered_df['Medicine'].value_counts().head(10).reset_index()
        med_counts.columns = ['Medicine', 'Count']
        fig_med = px.bar(med_counts, x='Count', y='Medicine', orientation='h', color='Count',
                         color_continuous_scale='Emerald', template='plotly_dark')
        fig_med.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_med, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 5: DECISION SIMULATOR ---
elif page == "⚙️ Capacity Decision Simulator":
    st.markdown("### ⚙️ Executive Hospital Decision Analytics Simulator")
    st.markdown("Simulate Length of Stay (LOS) reduction scenarios to optimize bed turnaround and financial cost savings.")
    
    st.markdown("<div class='clinical-container'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        los_reduction_pct = st.slider("Target Inpatient Length of Stay Reduction (%)", 0, 30, 10, help="Simulate discharge efficiency")
        cost_per_bed_day = st.number_input("Average Operational Cost per Bed-Day (₹)", 1000, 20000, 5000)
        
    current_total_los = filtered_df['Length_of_Stay_Days'].sum()
    saved_bed_days = current_total_los * (los_reduction_pct / 100.0)
    estimated_savings = saved_bed_days * cost_per_bed_day
    
    with c2:
        st.markdown(f"""
            <div style="background: #0f172a; border-radius: 12px; padding: 20px; border: 1px solid #14b8a6;">
                <div style="color: #94a3b8; font-weight: 600; font-size: 13px;">ESTIMATED INPATIENT BED-DAYS SAVED</div>
                <div style="color: #2dd4bf; font-size: 32px; font-weight: 700;">{saved_bed_days:,.0f} Days</div>
                <hr style="border-color: #1e293b;">
                <div style="color: #94a3b8; font-weight: 600; font-size: 13px;">POTENTIAL COST EFFICIENCY SAVINGS</div>
                <div style="color: #34d399; font-size: 32px; font-weight: 700;">₹{estimated_savings:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("🏥 MediPulse Command Center | Infosys Project Group 1")
