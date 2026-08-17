import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as json_go
import os

st.set_page_config(
    page_title="Healthcare Operations Intelligence Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive design aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #475569;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 14px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
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
    st.error("Cleaned dataset not found! Please ensure 'Processed Dataset/Admissions_cleaned.csv' exists.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.title("🏥 Navigation & Filters")
page = st.sidebar.radio("Select Dashboard View", [
    "1. Executive Overview & KPIs",
    "2. Clinical & Bed Capacity",
    "3. Financial & Revenue Analytics",
    "4. Patient & Diagnostic Insights",
    "5. Operational Decision Simulator"
])

st.sidebar.markdown("---")
selected_departments = st.sidebar.multiselect(
    "Filter Department",
    options=sorted(df['Department'].dropna().unique().tolist()),
    default=[]
)

selected_wards = st.sidebar.multiselect(
    "Filter Ward",
    options=sorted(df['Ward'].dropna().unique().tolist()),
    default=[]
)

# Apply filters
filtered_df = df.copy()
if selected_departments:
    filtered_df = filtered_df[filtered_df['Department'].isin(selected_departments)]
if selected_wards:
    filtered_df = filtered_df[filtered_df['Ward'].isin(selected_wards)]

# --- PAGE 1: EXECUTIVE OVERVIEW ---
if page == "1. Executive Overview & KPIs":
    st.title("📊 Executive Summary & Healthcare KPIs")
    st.markdown("Real-time operational dashboard providing high-level visibility across patient volumes, revenue, and hospital performance metrics.")
    
    # KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Patients</div>
                <div class="metric-value">{filtered_df['Patient_ID'].nunique():,}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Revenue</div>
                <div class="metric-value">₹{filtered_df['Total_Amount'].sum()/1e6:.1f}M</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Length of Stay</div>
                <div class="metric-value">{filtered_df['Length_of_Stay_Days'].mean():.1f} days</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Emergency Ratio</div>
                <div class="metric-value">{(filtered_df['Emergency'].value_counts().get('Yes', 0)/len(filtered_df)*100 if len(filtered_df)>0 else 0):.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Patient Age</div>
                <div class="metric-value">{filtered_df['Age'].mean():.1f} yrs</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Department-wise Patient Admissions")
        dept_counts = filtered_df['Department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Admissions']
        fig_dept = px.bar(dept_counts.head(10), x='Admissions', y='Department', orientation='h',
                          color='Admissions', color_continuous_scale='Viridis', template='plotly_dark')
        st.plotly_chart(fig_dept, use_container_width=True)
        
    with c2:
        st.subheader("Admission Trends Over Time")
        filtered_df['Month_Year'] = filtered_df['Admission_Date'].dt.to_period('M').astype(str)
        trend = filtered_df.groupby('Month_Year')['Admission_ID'].count().reset_index()
        fig_trend = px.line(trend, x='Month_Year', y='Admission_ID', markers=True,
                            labels={'Admission_ID': 'Admissions'}, template='plotly_dark')
        st.plotly_chart(fig_trend, use_container_width=True)

# --- PAGE 2: CLINICAL & BED CAPACITY ---
elif page == "2. Clinical & Bed Capacity":
    st.title("🛏️ Clinical Operations & Bed Capacity Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Ward Occupancy Distribution")
        ward_counts = filtered_df['Ward'].value_counts().reset_index()
        ward_counts.columns = ['Ward', 'Count']
        fig_ward = px.pie(ward_counts, values='Count', names='Ward', hole=0.4, template='plotly_dark')
        st.plotly_chart(fig_ward, use_container_width=True)
        
    with col2:
        st.subheader("Room Type Split")
        room_counts = filtered_df['Room_Type'].value_counts().reset_index()
        room_counts.columns = ['Room Type', 'Count']
        fig_room = px.bar(room_counts, x='Room Type', y='Count', color='Room Type', template='plotly_dark')
        st.plotly_chart(fig_room, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Average Length of Stay (LOS) by Clinical Department")
    los_dept = filtered_df.groupby('Department')['Length_of_Stay_Days'].mean().reset_index().sort_values('Length_of_Stay_Days', ascending=False)
    fig_los = px.bar(los_dept.head(12), x='Department', y='Length_of_Stay_Days', color='Length_of_Stay_Days',
                     color_continuous_scale='Oranges', template='plotly_dark')
    st.plotly_chart(fig_los, use_container_width=True)

# --- PAGE 3: FINANCIAL & REVENUE ---
elif page == "3. Financial & Revenue Analytics":
    st.title("💰 Financial & Revenue Decision Analytics")
    
    f1, f2, f3 = st.columns(3)
    with f1:
        st.metric("Total Billed Amount", f"₹{filtered_df['Total_Amount'].sum():,.2f}")
    with f2:
        st.metric("Total Insurance Covered", f"₹{filtered_df['Insurance_Cover'].sum():,.2f}")
    with f3:
        st.metric("Outstanding Balance", f"₹{filtered_df['Outstanding_Balance'].sum():,.2f}")
        
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Payment Status Breakdown")
        pay_status = filtered_df['Payment_Status'].value_counts().reset_index()
        pay_status.columns = ['Status', 'Admissions']
        fig_pay = px.pie(pay_status, values='Admissions', names='Status', color='Status',
                         color_discrete_map={'Paid': '#22c55e', 'Partial': '#eab308', 'Pending': '#ef4444'},
                         template='plotly_dark')
        st.plotly_chart(fig_pay, use_container_width=True)
        
    with c2:
        st.subheader("Revenue Contribution by Department")
        rev_dept = filtered_df.groupby('Department')['Total_Amount'].sum().reset_index().sort_values('Total_Amount', ascending=False)
        fig_rev = px.bar(rev_dept.head(10), x='Total_Amount', y='Department', orientation='h',
                         color='Total_Amount', color_continuous_scale='Purples', template='plotly_dark')
        st.plotly_chart(fig_rev, use_container_width=True)

# --- PAGE 4: PATIENT & DIAGNOSTICS ---
elif page == "4. Patient & Diagnostic Insights":
    st.title("🔬 Patient Demographics & Diagnostic Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Clinical Diagnoses")
        diag_counts = filtered_df['Diagnosis'].value_counts().head(10).reset_index()
        diag_counts.columns = ['Diagnosis', 'Count']
        fig_diag = px.bar(diag_counts, x='Count', y='Diagnosis', orientation='h', template='plotly_dark')
        st.plotly_chart(fig_diag, use_container_width=True)
        
    with col2:
        st.subheader("Top Prescribed Medications")
        med_counts = filtered_df['Medicine'].value_counts().head(10).reset_index()
        med_counts.columns = ['Medicine', 'Count']
        fig_med = px.bar(med_counts, x='Count', y='Medicine', orientation='h', color='Count', template='plotly_dark')
        st.plotly_chart(fig_med, use_container_width=True)

# --- PAGE 5: DECISION SIMULATOR ---
elif page == "5. Operational Decision Simulator":
    st.title("⚙️ Healthcare Operational Decision Analytics Simulator")
    st.markdown("Simulate length of stay reduction and capacity optimization to estimate potential bed-days saved and cost efficiencies.")
    
    col1, col2 = st.columns(2)
    with col1:
        los_reduction_pct = st.slider("Target Length of Stay (LOS) Reduction (%)", 0, 30, 10)
        cost_per_bed_day = st.number_input("Estimated Hospital Cost per Bed-Day (₹)", 1000, 20000, 5000)
        
    current_total_los = filtered_df['Length_of_Stay_Days'].sum()
    saved_bed_days = current_total_los * (los_reduction_pct / 100.0)
    estimated_savings = saved_bed_days * cost_per_bed_day
    
    with col2:
        st.markdown(f"""
            <div class="metric-card" style="border: 2px solid #38bdf8;">
                <div class="metric-label">Estimated Bed-Days Saved</div>
                <div class="metric-value">{saved_bed_days:,.0f} Days</div>
                <br>
                <div class="metric-label">Estimated Financial Efficiency</div>
                <div class="metric-value">₹{estimated_savings:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("Healthcare Operations Intelligence Dashboard | Developed by Group 1")
