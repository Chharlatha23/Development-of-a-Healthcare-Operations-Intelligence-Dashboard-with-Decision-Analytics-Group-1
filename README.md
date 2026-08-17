# Healthcare Operations Intelligence Dashboard with Decision Analytics

Welcome to the official repository for **Development of a Healthcare Operations Intelligence Dashboard with Decision Analytics (Group 1)**.

## 📌 Project Overview
This project presents an end-to-end Healthcare Operations Intelligence & Decision Analytics solution. It processes raw hospital admission logs, performs automated data cleaning and feature engineering, computes key performance metrics, and serves an interactive 5-page decision analytics dashboard built with **Streamlit** and **Plotly**.

---

## 🛠️ Step-by-Step Project Implementation

### Step 1: Understand & Clean the Dataset (`scripts/data_cleaning.py`)
- **Raw File:** `Raw Dataset/Admissions_filled.csv` (13,069 records, 52 columns).
- **Actions Taken:**
  - Removed duplicate/suffix columns (`.1`, `.2`).
  - Standardized textual formatting across departments and wards.
  - Parsed datetime fields (`Admission_Date`, `Discharge_Date`, `Test_Date`).
  - Computed calculated features: `Length_of_Stay_Days`, `Insurance_Coverage_Pct`, and `Outstanding_Balance`.
- **Output File:** `Processed Dataset/Admissions_cleaned.csv`.

### Step 2 & 3: Exploratory Data Analysis & Operational KPIs (`scripts/eda_insights.py`)
Key metrics computed from the dataset:
- **Total Patients:** `13,069` unique patient admissions.
- **Total Revenue Billed:** `₹864,465,918.00` (~₹864.5 Million).
- **Insurance Coverage:** `₹432,894,031.00` (50.08% coverage ratio).
- **Outstanding Dues:** Net pending patient payments analyzed across Payment Statuses (`Paid`, `Partial`, `Pending`).
- **Average Length of Stay (LOS):** `11.96 days`.
- **Emergency Admission Ratio:** `49.87%` emergency vs `50.13%` elective.
- **Department Load:** 20 distinct departments led by Gynecology, Orthopedics, Pediatrics, Nephrology, and Pulmonology.

### Step 4 & 5: Interactive 5-Page Dashboard (`app.py`)
Built an interactive multi-page dashboard featuring Plotly dark-themed visualizations:
1. **Executive Overview & KPIs:** Real-time metrics cards, department load bar chart, monthly admission trends.
2. **Clinical & Bed Capacity:** Ward occupancy doughnut chart, room type distribution, average LOS by specialty.
3. **Financial & Revenue Analytics:** Payment status breakdown, departmental revenue contribution, outstanding recovery.
4. **Patient & Diagnostic Insights:** Top 10 clinical diagnoses, medication prescription demand, demographic age distribution.
5. **Operational Decision Simulator:** Interactive slider tool allowing hospital executives to simulate Length of Stay (LOS) reduction scenarios and calculate potential bed-days saved & cost efficiencies.

---

## 🚀 How to Run the Project Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Chharlatha23/Development-of-a-Healthcare-Operations-Intelligence-Dashboard-with-Decision-Analytics-Group-1.git
   cd "Development-of-a-Healthcare-Operations-Intelligence-Dashboard-with-Decision-Analytics-Group-1"
   ```

2. **Run Data Cleaning & EDA Pipelines:**
   ```bash
   python scripts/data_cleaning.py
   python scripts/eda_insights.py
   ```

3. **Launch the Interactive Dashboard:**
   ```bash
   streamlit run app.py
   ```

---

## 📁 Repository Structure
```
├── Processed Dataset/
│   ├── Admissions_cleaned.csv     # Cleaned & feature-engineered dataset
│   └── eda_insights.json          # Precomputed EDA insights summary
├── Raw Dataset/
│   └── Admissions_filled.csv      # Original raw dataset
├── scripts/
│   ├── data_cleaning.py           # Automated cleaning pipeline
│   └── eda_insights.py            # EDA calculation script
├── app.py                         # Interactive Streamlit & Plotly Dashboard
└── README.md                      # Complete project guide and documentation
```

---
*Developed by Group 1 for Infosys Healthcare Operations Intelligence Project.*
