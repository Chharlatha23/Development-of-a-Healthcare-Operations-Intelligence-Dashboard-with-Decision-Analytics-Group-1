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

# Professional Clean Hospital Theme CSS (WCAG Accessible, Compact & High Contrast Light Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    /* Reduce Wasted White Space at Top */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
    }

    /* Clean Enterprise Hospital Header */
    .hospital-header-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 14px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .hospital-header-title {
        color: #0f172a;
        font-size: 22px;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .hospital-header-subtitle {
        color: #475569;
        font-size: 13px;
        font-weight: 500;
        margin-top: 2px;
    }

    .status-badge-active {
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

    /* Compact White KPI Metric Cards */
    .hospital-kpi-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 12px 16px;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0284c7; /* Primary Medical Blue */
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .hospital-kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px 0 rgba(0, 0, 0, 0.05);
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
        margin-bottom: 2px;
    }

    .kpi-card-value {
        font-size: 24px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
    }

    .kpi-card-value-rose {
        color: #be123c;
    }

    .kpi-card-sub {
        font-size: 11px;
        font-weight: 500;
        color: #64748b;
        margin-top: 2px;
    }

    /* White Section Card Containers for Charts */
    .chart-container-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
        margin-bottom: 16px;
    }

    .chart-card-title {
        font-size: 15px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Key Insights Container */
    .insights-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
        margin-top: 5px;
        margin-bottom: 15px;
    }

    .insight-item {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .insight-title {
        font-size: 12px;
        font-weight: 600;
        color: #475569;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .insight-val {
        font-size: 14px;
        font-weight: 700;
        color: #0284c7;
    }

    /* Slightly Reduce Sidebar Width */
    section[data-testid="stSidebar"] {
        width: 275px !important;
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #0f172a !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }

    /* Filter Status Pill */
    .filter-status-pill {
        background-color: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 14px;
        display: inline-block;
    }

    /* High Contrast Text overrides for Filter elements */
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 12px !important;
    }
    
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
        margin: 10px 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Cache busted to load new financial calculations
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

# --- PROFESSIONAL CLEAN HOSPITAL HEADER (NO FAKE REAL-TIME CLAIMS) ---
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
            <span class="status-badge-active">
                <span class="status-dot-green"></span> Analytics Dashboard: Active
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION & ROUTING STATE ---
st.sidebar.markdown("## 🏥 MediPulse")
st.sidebar.markdown("**Hospital Analytics**")
st.sidebar.markdown("---")

NAV_OPTIONS = [
    "Executive Overview",
    "Bed Capacity & Ward Analytics",
    "Patient Flow",
    "Revenue & Dues",
    "Diagnostic Labs & Pharmacy",
    "Emergency Analytics",
    "Length-of-Stay Reduction Simulator"
]

if "selected_view" not in st.session_state:
    st.session_state.selected_view = "Executive Overview"

st.sidebar.markdown("### 📌 Navigation")

def update_nav():
    st.session_state.selected_view = st.session_state.nav_radio

selected_view = st.sidebar.radio(
    "Select Dashboard View",
    options=NAV_OPTIONS,
    index=NAV_OPTIONS.index(st.session_state.selected_view) if st.session_state.selected_view in NAV_OPTIONS else 0,
    key="nav_radio",
    on_change=update_nav
)

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

# --- DYNAMIC ACTIVE FILTER STATUS PILL ---
active_filters_count = len(dept_filter) + len(ward_filter) + (1 if emergency_filter != "All Statuses" else 0)
if active_filters_count > 0:
    st.markdown(f'<div class="filter-status-pill">🔍 Active Filters: {active_filters_count} applied</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="filter-status-pill" style="background-color:#f1f5f9; color:#475569; border-color:#e2e8f0;">Showing All Hospital Data</div>', unsafe_allow_html=True)

# ==========================================
# 1. EXECUTIVE OVERVIEW DASHBOARD
# ==========================================
if selected_view == "Executive Overview":
    st.markdown("### Executive Overview Dashboard")
    
    # 5 KPI METRIC CARDS ROW (Compact Vertical Padding)
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
                <div class="kpi-card-value">{f_df['Length_of_Stay_Days'].mean():.1f} <span style="font-size:13px; font-weight:600;">Days</span></div>
                <div class="kpi-card-sub">⏱️ Average Hospital Stay</div>
            </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-rose">
                <div class="kpi-card-label">Emergency Admission Rate</div>
                <div class="kpi-card-value kpi-card-value-rose">{(f_df['Emergency'].value_counts().get('Yes', 0)/len(f_df)*100 if len(f_df)>0 else 0):.1f}%</div>
                <div class="kpi-card-sub">🚑 {f_df['Emergency'].value_counts().get('Yes', 0):,} Emergency Cases</div>
            </div>
        """, unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-amber">
                <div class="kpi-card-label">Outstanding Dues</div>
                <div class="kpi-card-value">₹{f_df['Outstanding_Balance'].sum()/1e6:.1f}M</div>
                <div class="kpi-card-sub">⚠️ Uncollected Dues</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # CHARTS ROW (No Empty Placeholder Boxes)
    col_left, col_right = st.columns([1.2, 1])
    with col_left:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>🏥 Department-wise Admission Volume</span><span style='font-size:12px; color:#64748b;'>Top Specialties</span></div>", unsafe_allow_html=True)
        dept_counts = f_df['Department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Admissions']
        top_dept = dept_counts.head(10)
        
        max_val = top_dept['Admissions'].max() if len(top_dept) > 0 else 100
        
        fig_dept = px.bar(
            top_dept, x='Admissions', y='Department', orientation='h',
            color='Admissions', color_continuous_scale='Blues', text='Admissions'
        )
        fig_dept.update_traces(
            textposition='outside',
            cliponaxis=False,
            marker_line_color='#0284c7',
            marker_line_width=1
        )
        fig_dept.update_layout(
            **PLOTLY_LIGHT_THEME,
            height=340,
            margin=dict(l=0, r=55, t=10, b=0)
        )
        fig_dept.update_xaxes(range=[0, max_val * 1.15], gridcolor='#f1f5f9', tickfont={'color': '#475569'})
        st.plotly_chart(fig_dept, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>📈 Monthly Inpatient Admission Trend</span><span style='font-size:12px; color:#64748b;'>Volume Trends</span></div>", unsafe_allow_html=True)
        f_df['Month_Year'] = f_df['Admission_Date'].dt.to_period('M').astype(str)
        
        # Exclude incomplete final month dynamically for accurate trend representation
        max_date = f_df['Admission_Date'].max()
        import calendar
        is_complete = (max_date.day == calendar.monthrange(max_date.year, max_date.month)[1]) if pd.notna(max_date) else True
        complete_monthly_df = f_df[f_df['Month_Year'] != max_date.strftime('%Y-%m')].groupby('Month_Year')['Admission_ID'].count().reset_index() if not is_complete else f_df.groupby('Month_Year')['Admission_ID'].count().reset_index()
        
        fig_monthly = px.area(
            complete_monthly_df, x='Month_Year', y='Admission_ID',
            labels={'Admission_ID': 'Admissions', 'Month_Year': 'Admission Month'}, color_discrete_sequence=['#0284c7']
        )
        fig_monthly.update_layout(**PLOTLY_LIGHT_THEME, height=340, margin=dict(l=0, r=10, t=10, b=0))
        st.plotly_chart(fig_monthly, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # DYNAMIC KEY INSIGHTS SECTION
    if len(dept_counts) > 0:
        max_admissions = dept_counts['Admissions'].max()
        top_depts = dept_counts[dept_counts['Admissions'] == max_admissions]['Department'].tolist()
        top_dept_name = " & ".join(top_depts)
    else:
        top_dept_name = "N/A"
    avg_monthly_adm = round(complete_monthly_df['Admission_ID'].mean(), 1) if len(complete_monthly_df) > 0 else 0
    er_rate_val = (f_df['Emergency'].value_counts().get('Yes', 0)/len(f_df)*100 if len(f_df)>0 else 0)
    avg_los_val = f_df['Length_of_Stay_Days'].mean() if len(f_df)>0 else 0
    top_rev_dept = f_df.groupby('Department')['Total_Amount'].sum().idxmax() if len(f_df)>0 else "N/A"

    st.markdown("<div class='insights-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-card-title' style='margin-bottom:10px;'><span>💡 Key Executive Insights</span></div>", unsafe_allow_html=True)
    
    i1, i2, i3, i4, i5 = st.columns(5)
    with i1:
        st.markdown(f"""
            <div class="insight-item">
                <div class="insight-title">🏥 Top Department</div>
                <div class="insight-val">{top_dept_name}</div>
            </div>
        """, unsafe_allow_html=True)
    with i2:
        st.markdown(f"""
            <div class="insight-item">
                <div class="insight-title">📊 Avg Monthly Admissions</div>
                <div class="insight-val">{avg_monthly_adm:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)
    with i3:
        st.markdown(f"""
            <div class="insight-item">
                <div class="insight-title">🚑 Emergency Admission Rate</div>
                <div class="insight-val">{er_rate_val:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with i4:
        st.markdown(f"""
            <div class="insight-item">
                <div class="insight-title">🛏️ Average Stay</div>
                <div class="insight-val">{avg_los_val:.1f} Days</div>
            </div>
        """, unsafe_allow_html=True)
    with i5:
        st.markdown(f"""
            <div class="insight-item">
                <div class="insight-title">🏛️ Top Revenue Dept</div>
                <div class="insight-val">{top_rev_dept}</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 2. BED CAPACITY & WARD ANALYTICS DASHBOARD
# ==========================================
elif selected_view == "Bed Capacity & Ward Analytics":
    st.markdown("### Bed Capacity & Ward Analytics Dashboard")
    
    # Dynamic KPI Summary Row
    total_beds = f_df['Bed_ID'].nunique() if 'Bed_ID' in f_df.columns else len(f_df)
    top_ward = f_df['Ward'].value_counts().idxmax() if len(f_df) > 0 else "N/A"
    icu_count = len(f_df[f_df['Ward'] == 'Icu'])
    top_room = f_df['Room_Type'].value_counts().idxmax() if len(f_df) > 0 else "N/A"
    avg_ward_los = f_df['Length_of_Stay_Days'].mean() if len(f_df) > 0 else 0
    
    b1, b2, b3, b4, b5 = st.columns(5)
    with b1:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Unique Beds in Records</div>
                <div class="kpi-card-value">{total_beds:,}</div>
                <div class="kpi-card-sub">🛏️ Unique Bed IDs</div>
            </div>
        """, unsafe_allow_html=True)
    with b2:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-teal">
                <div class="kpi-card-label">Highest Admission-Volume Ward</div>
                <div class="kpi-card-value">{top_ward}</div>
                <div class="kpi-card-sub">🏨 Peak Patient Load</div>
            </div>
        """, unsafe_allow_html=True)
    with b3:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-rose">
                <div class="kpi-card-label">ICU Admissions</div>
                <div class="kpi-card-value kpi-card-value-rose">{icu_count:,}</div>
                <div class="kpi-card-sub">🚨 Intensive Care Admissions</div>
            </div>
        """, unsafe_allow_html=True)
    with b4:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Most Common Room Type</div>
                <div class="kpi-card-value">{top_room}</div>
                <div class="kpi-card-sub">🚪 Preference Split</div>
            </div>
        """, unsafe_allow_html=True)
    with b5:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-amber">
                <div class="kpi-card-label">Average Bed Stay</div>
                <div class="kpi-card-value">{avg_ward_los:.1f} Days</div>
                <div class="kpi-card-sub">⏱️ Inpatient Duration</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>🏨 Ward Admission Volume</span></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='chart-card-title'><span>🔥 Department vs. Ward Admission Volume (Heatmap)</span></div>", unsafe_allow_html=True)
    heatmap_data = pd.crosstab(f_df['Department'], f_df['Ward'])
    fig_heat = px.imshow(heatmap_data, text_auto=True, aspect="auto", color_continuous_scale="Blues")
    fig_heat.update_layout(**PLOTLY_LIGHT_THEME, height=380)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Dynamic Key Insights Section
    st.markdown("<div class='insights-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-card-title' style='margin-bottom:10px;'><span>💡 Key Capacity Insights</span></div>", unsafe_allow_html=True)
    i1, i2, i3, i4 = st.columns(4)
    with i1:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🏨 Highest Ward Volume</div><div class="insight-val">{top_ward}</div></div>', unsafe_allow_html=True)
    with i2:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🚨 Intensive Care Admissions</div><div class="insight-val">{icu_count:,}</div></div>', unsafe_allow_html=True)
    with i3:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🚪 Primary Accommodation</div><div class="insight-val">{top_room}</div></div>', unsafe_allow_html=True)
    with i4:
        st.markdown(f'<div class="insight-item"><div class="insight-title">⏱️ Average Ward Stay</div><div class="insight-val">{avg_ward_los:.1f} Days</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 3. PATIENT FLOW DASHBOARD
# ==========================================
elif selected_view == "Patient Flow":
    st.markdown("### Patient Flow Dashboard")
    
    f_df['Month_Year'] = f_df['Admission_Date'].dt.to_period('M').astype(str)
    max_date = f_df['Admission_Date'].max()
    import calendar
    is_complete = (max_date.day == calendar.monthrange(max_date.year, max_date.month)[1]) if pd.notna(max_date) else True
    complete_monthly = f_df[f_df['Month_Year'] != max_date.strftime('%Y-%m')] if not is_complete else f_df
    
    avg_monthly = round(complete_monthly.groupby('Month_Year')['Admission_ID'].count().mean(), 1) if len(complete_monthly) > 0 else 0
    top_flow_dept = f_df['Department'].value_counts().idxmax() if len(f_df) > 0 else "N/A"
    if len(complete_monthly) > 0:
        date_range = (complete_monthly['Admission_Date'].max() - complete_monthly['Admission_Date'].min()).days + 1
        avg_daily_intake = round(len(complete_monthly) / max(1, date_range), 1)
    else:
        avg_daily_intake = 0
    
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Total Inpatient Admissions</div>
                <div class="kpi-card-value">{len(f_df):,}</div>
                <div class="kpi-card-sub">👥 Registered Intake</div>
            </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-teal">
                <div class="kpi-card-label">Average Length of Stay</div>
                <div class="kpi-card-value">{f_df['Length_of_Stay_Days'].mean():.1f} Days</div>
                <div class="kpi-card-sub">⏱️ Average Hospital Stay</div>
            </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Daily Average Intake</div>
                <div class="kpi-card-value">{avg_daily_intake} / Day</div>
                <div class="kpi-card-sub">📈 Daily Flow Rate</div>
            </div>
        """, unsafe_allow_html=True)
    with p4:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-amber">
                <div class="kpi-card-label">Average Monthly Intake</div>
                <div class="kpi-card-value">{avg_monthly:,.0f}</div>
                <div class="kpi-card-sub">📊 Monthly Patient Volume</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>📈 Patient Volume Flow Over Time</span><span style='font-size:11px; color:#64748b;'>Complete Months</span></div>", unsafe_allow_html=True)
        monthly_flow_df = complete_monthly.groupby('Month_Year')['Admission_ID'].count().reset_index()
        fig_flow = px.line(monthly_flow_df, x='Month_Year', y='Admission_ID', markers=True, color_discrete_sequence=['#0284c7'], labels={'Admission_ID': 'Admissions', 'Month_Year': 'Admission Month'})
        fig_flow.update_layout(**PLOTLY_LIGHT_THEME, height=340)
        st.plotly_chart(fig_flow, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>🏥 Department Intake Distribution</span></div>", unsafe_allow_html=True)
        dept_counts = f_df['Department'].value_counts().head(10).reset_index()
        dept_counts.columns = ['Department', 'Count']
        fig_dept_flow = px.bar(dept_counts, x='Count', y='Department', orientation='h', color='Count', color_continuous_scale='Teal')
        fig_dept_flow.update_layout(**PLOTLY_LIGHT_THEME, height=340)
        st.plotly_chart(fig_dept_flow, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Dynamic Key Insights
    st.markdown("<div class='insights-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-card-title' style='margin-bottom:10px;'><span>💡 Key Patient Flow Insights</span></div>", unsafe_allow_html=True)
    i1, i2, i3, i4 = st.columns(4)
    with i1:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🏥 Highest Admission Dept</div><div class="insight-val">{top_flow_dept}</div></div>', unsafe_allow_html=True)
    with i2:
        st.markdown(f'<div class="insight-item"><div class="insight-title">📊 Avg Monthly Admissions</div><div class="insight-val">{avg_monthly:,.0f}</div></div>', unsafe_allow_html=True)
    with i3:
        st.markdown(f'<div class="insight-item"><div class="insight-title">📈 Avg Daily Patient Intake</div><div class="insight-val">{avg_daily_intake} / Day</div></div>', unsafe_allow_html=True)
    with i4:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🛏️ Avg Length of Stay</div><div class="insight-val">{f_df["Length_of_Stay_Days"].mean():.1f} Days</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. FINANCIAL REVENUE CYCLE & DUES DASHBOARD
# ==========================================
elif selected_view == "Revenue & Dues":
    st.markdown("### Financial Revenue Cycle & Dues Recovery Dashboard")
    
    total_rev = f_df['Total_Amount'].sum() if len(f_df) > 0 else 0
    ins_cover = f_df['Insurance_Cover'].sum() if len(f_df) > 0 else 0
    pending_dues = f_df['Outstanding_Balance'].sum() if len(f_df) > 0 else 0
    collected_amount = max(0, total_rev - pending_dues) if len(f_df) > 0 else 0
    settlement_rate = (collected_amount / max(1, total_rev)) * 100
    top_rev_dept = f_df.groupby('Department')['Total_Amount'].sum().idxmax() if len(f_df) > 0 else "N/A"
    
    f1, f2, f3, f4, f5 = st.columns(5)
    with f1:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Gross Billed Revenue</div>
                <div class="kpi-card-value">₹{total_rev/1e6:.1f}M</div>
                <div class="kpi-card-sub">💳 Gross Patient Claims</div>
            </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-teal">
                <div class="kpi-card-label">Insurance Covered</div>
                <div class="kpi-card-value">₹{ins_cover/1e6:.1f}M</div>
                <div class="kpi-card-sub">🏛️ Claim Coverage Amount</div>
            </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Estimated Collected Amount</div>
                <div class="kpi-card-value">₹{collected_amount/1e6:.1f}M</div>
                <div class="kpi-card-sub">💵 Estimated Amount Collected</div>
            </div>
        """, unsafe_allow_html=True)
    with f4:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-amber">
                <div class="kpi-card-label">Net Pending Dues</div>
                <div class="kpi-card-value">₹{pending_dues/1e6:.1f}M</div>
                <div class="kpi-card-sub">⚠️ Outstanding Balances</div>
            </div>
        """, unsafe_allow_html=True)
    with f5:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-teal">
                <div class="kpi-card-label">Collection Rate</div>
                <div class="kpi-card-value">{settlement_rate:.1f}%</div>
                <div class="kpi-card-sub">✅ Revenue Recovery Ratio</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>💳 Payment Status Distribution</span></div>", unsafe_allow_html=True)
        pay_df = f_df['Payment_Status'].value_counts().reset_index()
        pay_df.columns = ['Status', 'Count']
        fig_pay = px.pie(
            pay_df, values='Count', names='Status', color='Status',
            color_discrete_map={'Paid': '#16a34a', 'Partial': '#d97706', 'Pending': '#dc2626'}
        )
        fig_pay.update_layout(**PLOTLY_LIGHT_THEME, height=340)
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
        fig_rev.update_layout(**PLOTLY_LIGHT_THEME, height=340)
        st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Key Insights Section
    st.markdown("<div class='insights-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-card-title' style='margin-bottom:10px;'><span>💡 Key Financial Insights</span></div>", unsafe_allow_html=True)
    i1, i2, i3, i4 = st.columns(4)
    with i1:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🏛️ Top Revenue Department</div><div class="insight-val">{top_rev_dept}</div></div>', unsafe_allow_html=True)
    with i2:
        st.markdown(f'<div class="insight-item"><div class="insight-title">💳 Gross Billed Volume</div><div class="insight-val">₹{total_rev/1e6:.1f}M</div></div>', unsafe_allow_html=True)
    with i3:
        st.markdown(f'<div class="insight-item"><div class="insight-title">✅ Revenue Settlement Rate</div><div class="insight-val">{settlement_rate:.1f}%</div></div>', unsafe_allow_html=True)
    with i4:
        st.markdown(f'<div class="insight-item"><div class="insight-title">⚠️ Outstanding Dues</div><div class="insight-val">₹{pending_dues/1e6:.1f}M</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. DIAGNOSTIC LABS & PHARMACY DASHBOARD
# ==========================================
elif selected_view == "Diagnostic Labs & Pharmacy":
    st.markdown("### Diagnostic Labs & Pharmacy Dashboard")
    
    total_diag_records = len(f_df['Diagnosis'].dropna())
    unique_diagnoses = f_df['Diagnosis'].nunique()
    total_prescriptions = len(f_df['Medicine'].dropna())
    top_diag = f_df['Diagnosis'].value_counts().idxmax() if len(f_df) > 0 else "N/A"
    top_med = f_df['Medicine'].value_counts().idxmax() if len(f_df) > 0 else "N/A"
    
    d1, d2, d3, d4, d5 = st.columns(5)
    with d1:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Diagnostic Records</div>
                <div class="kpi-card-value">{total_diag_records:,}</div>
                <div class="kpi-card-sub">📋 Diagnosis Records</div>
            </div>
        """, unsafe_allow_html=True)
    with d2:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-teal">
                <div class="kpi-card-label">Unique Diagnoses</div>
                <div class="kpi-card-value">{unique_diagnoses:,}</div>
                <div class="kpi-card-sub">🧪 Identified Conditions</div>
            </div>
        """, unsafe_allow_html=True)
    with d3:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Prescription Volume</div>
                <div class="kpi-card-value">{total_prescriptions:,}</div>
                <div class="kpi-card-sub">💊 Pharmacy Orders</div>
            </div>
        """, unsafe_allow_html=True)
    with d4:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-amber">
                <div class="kpi-card-label">Top Diagnosis</div>
                <div class="kpi-card-value" style="font-size:20px;">{top_diag}</div>
                <div class="kpi-card-sub">📋 Most Prevalent Condition</div>
            </div>
        """, unsafe_allow_html=True)
    with d5:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-teal">
                <div class="kpi-card-label">Top Medication</div>
                <div class="kpi-card-value" style="font-size:20px;">{top_med}</div>
                <div class="kpi-card-sub">💊 Highest Dispensed Drug</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>📋 Top 10 Clinical Diagnoses</span></div>", unsafe_allow_html=True)
        diag_df = f_df['Diagnosis'].value_counts().head(10).reset_index()
        diag_df.columns = ['Diagnosis', 'Count']
        fig_diag = px.bar(
            diag_df, x='Count', y='Diagnosis', orientation='h', color='Count',
            color_continuous_scale='Blues'
        )
        fig_diag.update_layout(**PLOTLY_LIGHT_THEME, height=340)
        st.plotly_chart(fig_diag, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>💊 Top Prescribed Medications</span></div>", unsafe_allow_html=True)
        med_df = f_df['Medicine'].value_counts().head(10).reset_index()
        med_df.columns = ['Medicine', 'Count']
        fig_med = px.bar(
            med_df, x='Count', y='Medicine', orientation='h', color='Count',
            color_continuous_scale='Teal'
        )
        fig_med.update_layout(**PLOTLY_LIGHT_THEME, height=340)
        st.plotly_chart(fig_med, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Dynamic Insights Section
    st.markdown("<div class='insights-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-card-title' style='margin-bottom:10px;'><span>💡 Clinical & Pharmacy Insights</span></div>", unsafe_allow_html=True)
    i1, i2, i3, i4 = st.columns(4)
    with i1:
        st.markdown(f'<div class="insight-item"><div class="insight-title">📋 Most Common Diagnosis</div><div class="insight-val">{top_diag}</div></div>', unsafe_allow_html=True)
    with i2:
        st.markdown(f'<div class="insight-item"><div class="insight-title">💊 Most Prescribed Drug</div><div class="insight-val">{top_med}</div></div>', unsafe_allow_html=True)
    with i3:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🧪 Unique Diagnoses Count</div><div class="insight-val">{unique_diagnoses:,}</div></div>', unsafe_allow_html=True)
    with i4:
        st.markdown(f'<div class="insight-item"><div class="insight-title">💊 Total Pharmacy Orders</div><div class="insight-val">{total_prescriptions:,}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. EMERGENCY ANALYTICS DASHBOARD
# ==========================================
elif selected_view == "Emergency Analytics":
    st.markdown("### Emergency Analytics Dashboard")
    
    er_df = f_df[f_df['Emergency'] == 'Yes']
    total_er = len(er_df)
    er_ratio = (total_er / max(1, len(f_df)) * 100)
    avg_er_los = er_df['Length_of_Stay_Days'].mean() if total_er > 0 else 0
    er_icu_cases = len(er_df[er_df['Ward'] == 'Icu'])
    top_er_dept = er_df['Department'].value_counts().idxmax() if total_er > 0 else "N/A"
    top_er_ward = er_df['Ward'].value_counts().idxmax() if total_er > 0 else "N/A"
    
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-rose">
                <div class="kpi-card-label">Total Emergency Cases</div>
                <div class="kpi-card-value kpi-card-value-rose">{total_er:,}</div>
                <div class="kpi-card-sub">🚨 Emergency Inpatient Volume</div>
            </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-rose">
                <div class="kpi-card-label">Emergency Intake Ratio</div>
                <div class="kpi-card-value kpi-card-value-rose">{er_ratio:.1f}%</div>
                <div class="kpi-card-sub">🚑 Emergency vs Elective Split</div>
            </div>
        """, unsafe_allow_html=True)
    with e3:
        st.markdown(f"""
            <div class="hospital-kpi-card">
                <div class="kpi-card-label">Average Emergency Stay</div>
                <div class="kpi-card-value">{avg_er_los:.1f} Days</div>
                <div class="kpi-card-sub">⏱️ Avg LOS for Emergency Admissions</div>
            </div>
        """, unsafe_allow_html=True)
    with e4:
        st.markdown(f"""
            <div class="hospital-kpi-card hospital-kpi-card-amber">
                <div class="kpi-card-label">Emergency ICU Cases</div>
                <div class="kpi-card-value">{er_icu_cases:,}</div>
                <div class="kpi-card-sub">🏥 Intensive Care Unit Intake</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>🚨 Emergency Cases by Department</span></div>", unsafe_allow_html=True)
        er_dept = er_df['Department'].value_counts().head(10).reset_index()
        er_dept.columns = ['Department', 'Count']
        fig_er_dept = px.bar(er_dept, x='Count', y='Department', orientation='h', color='Count', color_continuous_scale='Reds')
        fig_er_dept.update_layout(**PLOTLY_LIGHT_THEME, height=340)
        st.plotly_chart(fig_er_dept, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card-title'><span>🏥 Emergency Ward Allocation</span></div>", unsafe_allow_html=True)
        er_ward = er_df['Ward'].value_counts().reset_index()
        er_ward.columns = ['Ward', 'Count']
        fig_er_ward = px.pie(er_ward, values='Count', names='Ward', hole=0.4, color_discrete_sequence=['#be123c', '#e11d48', '#fb7185'])
        fig_er_ward.update_layout(**PLOTLY_LIGHT_THEME, height=340)
        st.plotly_chart(fig_er_ward, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Dynamic Insights Section
    st.markdown("<div class='insights-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-card-title' style='margin-bottom:10px;'><span>💡 Emergency Care Insights</span></div>", unsafe_allow_html=True)
    i1, i2, i3, i4 = st.columns(4)
    with i1:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🚨 Highest ER Department</div><div class="insight-val">{top_er_dept}</div></div>', unsafe_allow_html=True)
    with i2:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🚑 Emergency Admission Rate</div><div class="insight-val">{er_ratio:.1f}%</div></div>', unsafe_allow_html=True)
    with i3:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🏥 Emergency ICU Cases</div><div class="insight-val">{er_icu_cases:,}</div></div>', unsafe_allow_html=True)
    with i4:
        st.markdown(f'<div class="insight-item"><div class="insight-title">🏨 Most Utilized ER Ward</div><div class="insight-val">{top_er_ward}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 7. PREDICTIVE LENGTH-OF-STAY DASHBOARD
# ==========================================
elif selected_view == "Length-of-Stay Reduction Simulator":
    st.markdown("### Length-of-Stay Reduction Simulator")
    st.markdown("<div style='font-size:13px; color:#475569; margin-bottom:15px;'>Simulate length-of-stay reduction scenarios to estimate bed-days saved, operational cost savings, and additional admission capacity.</div>", unsafe_allow_html=True)
    
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
            <div style="background: #f8fafc; border-radius: 10px; padding: 16px 20px; border: 1px solid #cbd5e1;">
                <div style="color: #475569; font-size: 11px; font-weight: 700; text-transform: uppercase;">PROJECTED BED-DAYS SAVED</div>
                <div style="color: #0284c7; font-size: 26px; font-weight: 800;">{bed_days_saved:,.0f} Days</div>
                <hr style="border-color: #e2e8f0; margin: 8px 0;">
                <div style="color: #475569; font-size: 11px; font-weight: 700; text-transform: uppercase;">ESTIMATED OPERATIONAL FINANCIAL SAVINGS</div>
                <div style="color: #16a34a; font-size: 26px; font-weight: 800;">₹{cost_saved:,.2f}</div>
                <hr style="border-color: #e2e8f0; margin: 8px 0;">
                <div style="color: #475569; font-size: 11px; font-weight: 700; text-transform: uppercase;">ESTIMATED ADDITIONAL ADMISSION CAPACITY</div>
                <div style="color: #d97706; font-size: 20px; font-weight: 800;">+{extra_capacity:,} Patients</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Dynamic Scenario Comparison Bar Chart
    st.markdown("<div class='chart-container-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-card-title'><span>📊 Multi-Scenario Length-of-Stay Capacity Impact</span></div>", unsafe_allow_html=True)
    
    scenarios = [5, 10, 15, 20, 25, 30]
    scenario_days = [total_days * (s / 100.0) for s in scenarios]
    scenario_savings = [d * bed_day_cost / 1e6 for d in scenario_days]
    
    scenario_df = pd.DataFrame({
        'Reduction Scenario': [f"{s}% Target" for s in scenarios],
        'Bed Days Saved': scenario_days,
        'Savings (₹ Millions)': scenario_savings
    })
    
    fig_scenario = px.bar(
        scenario_df, x='Reduction Scenario', y='Bed Days Saved',
        color='Savings (₹ Millions)', color_continuous_scale='Blues',
        text_auto='.0f', labels={'Bed Days Saved': 'Bed Days Saved'}
    )
    fig_scenario.update_layout(**PLOTLY_LIGHT_THEME, height=320)
    st.plotly_chart(fig_scenario, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("🏥 MediPulse Hospital Analytics | Group 1")
