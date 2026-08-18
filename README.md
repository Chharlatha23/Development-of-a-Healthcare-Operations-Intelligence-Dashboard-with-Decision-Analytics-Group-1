# Healthcare Operations Intelligence Dashboard with Decision Analytics

Welcome to the official repository for **Development of a Healthcare Operations Intelligence Dashboard with Decision Analytics (Group 1)**.

## 📌 Project Overview
This project presents an end-to-end Healthcare Operations Intelligence & Decision Analytics solution. It processes raw hospital admission logs, performs automated data cleaning and feature engineering, computes key performance metrics, and serves a modern hospital operations and healthcare analytics dashboard built with Streamlit and Plotly.

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

### Step 4 & 5: Interactive 7-Page Dashboard (`app.py`)
A modern hospital operations and healthcare analytics dashboard built with Streamlit and Plotly, featuring a clean, WCAG-accessible light hospital theme:
1. **Executive Overview**: High-level metrics, department loads, and dynamic executive insights.
2. **Bed Capacity & Ward Analytics**: Ward utilization, room types, ICU metrics, and capacity insights.
3. **Patient Flow**: Admission tracking, flow rates, and turnaround metrics.
4. **Revenue & Dues**: Billed revenue, insurance coverage, patient out-of-pocket, and outstanding dues tracking.
5. **Diagnostic Labs & Pharmacy**: Diagnosis records, prescription volumes, and identified conditions.
6. **Emergency Analytics**: Emergency admission rates, critical intake ratios, and ER-specific metrics.
7. **Length-of-Stay Reduction Simulator**: An interactive decision simulator (NOT an ML prediction model) that allows hospital executives to simulate what-if operational scenarios to calculate potential bed-days saved and cost efficiencies.

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

## Data & Analytical Assumptions

* **Emergency Rate**: Based on the Emergency admission status field.
* **Length of Stay (LOS)**: Calculated from admission/discharge dates where available.
* **Incomplete Final Months**: Automatically excluded from monthly trend analysis to prevent skewed flow metrics.
* **Bed & Ward Metrics**: Based on admission records. These are not equivalent to real-time bed occupancy metrics as actual total capacity fields are not present.
* **LOS Simulator**: Represents what-if operational scenarios to estimate capacity impact. It is *not* a machine learning prediction model.
* **Financial Metrics**: Derived directly from available billing/payment fields and evaluated against Payment Status to prevent logical contradictions.

---
*Developed by Group 1 for Infosys Healthcare Operations Intelligence Project.*
