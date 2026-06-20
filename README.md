# 📊 RetailIQ AI — Automated Retail Analytics Platform

RetailIQ AI is an end-to-end Retail Sales Analytics platform built using **Python, SQL, MySQL, Pandas, Plotly, and Streamlit** to analyze retail business performance and generate actionable business insights.

This project simulates a real-world enterprise analytics workflow involving:

- Data ingestion
- Data cleaning & preprocessing
- Feature engineering
- Data warehouse schema design
- SQL business analysis
- Interactive dashboarding
- AI-driven business recommendations

---

# 🚀 Project Overview

Retail companies generate huge transaction data daily, but raw data alone does not help business leaders make decisions.

RetailIQ AI transforms raw retail sales data into meaningful insights such as:

- Revenue trends
- Profitability analysis
- Product performance
- Customer segmentation
- Regional performance
- Loss-making products
- AI-based recommendations

The dashboard helps management answer critical questions like:

- Which products generate maximum revenue?
- Which categories are loss-making?
- Which regions perform poorly?
- Are discounts hurting profitability?
- What actions improve profit margin?

---

# 🎯 Business Problem

A national retail company is facing:

- Fluctuating sales performance
- Low profit margins in some categories
- High discount dependency
- Regional underperformance
- Increasing loss-making orders

Management needs an analytics solution to monitor KPIs and improve decision-making.

---

# 🛠 Tech Stack

## Programming & Analytics
- Python
- SQL
- MySQL

## Python Libraries
- Pandas
- NumPy
- Plotly
- Streamlit
- SQLAlchemy
- PyMySQL

## Visualization
- Streamlit Dashboard
- Plotly Interactive Charts

## Database
- MySQL Data Warehouse
- Star Schema Modeling

---

# 📂 Project Architecture

```bash
RetailIQ-AI/
│
├── app/
│   ├── dashboard.py
│   └── styles.css
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── processed/
│   ├── final/
│   ├── warehouse/
│   └── dashboard/
│
├── sql/
│   ├── schema.sql
│   └── insert_queries.sql
│
├── src/
│   ├── ingestion.py
│   ├── cleaning.py
│   ├── feature_engineering.py
│   ├── schema_builder.py
│   ├── load_to_mysql.py
│   └── build_dashboard_dataset.py
│
├── reports/
├── requirements.txt
└── README.md
```

---

# 📊 Dataset

Dataset contains retail sales transaction data including:

- Orders
- Products
- Customers
- Geography
- Shipping
- Sales & Profit

### Key Fields
- Order ID
- Customer ID
- Product ID
- Region
- Category
- Sales
- Profit
- Discount
- Quantity
- Order Date
- Ship Date

---

# 🔄 Data Pipeline

## Sprint 1 — Data Ingestion
Loaded raw retail sales data into Python using Pandas.

## Sprint 2 — Data Cleaning
Performed:
- Missing value handling
- Duplicate removal
- Standardization
- Type conversion

## Sprint 3 — Feature Engineering
Created business features:

- profit_margin_pct
- delivery_days
- shipping_speed
- estimated_cost
- discount_bucket
- loss_flag

## Sprint 4 — Data Warehouse Design

Implemented **Star Schema**.

### Dimension Tables
- dim_customer
- dim_product
- dim_region
- dim_date

### Fact Table
- fact_sales

Benefits:
- Faster SQL analytics
- Better BI reporting
- Efficient aggregations

---

# 🧠 Data Warehouse Schema

## Fact Table
### fact_sales
Stores measurable business metrics:

- Sales
- Profit
- Quantity
- Discount

Foreign Keys:
- customer_key
- product_key
- region_key
- date_key

## Dimension Tables
### dim_customer
Customer details & segmentation

### dim_product
Product hierarchy

### dim_region
Location hierarchy

### dim_date
Time intelligence

---

# 📈 Dashboard Features

## Executive KPIs
- Total Revenue
- Total Profit
- Profit Margin
- Total Orders
- Average Order Value

## Analytics Visualizations
- Monthly Revenue Trend
- Profit Margin Gauge
- Revenue by Category
- Regional Revenue
- Top Products
- Loss-Making Products

## Filters
- Region
- Category
- Customer Segment

---

# 🤖 AI Recommendation Engine

RetailIQ AI includes rule-based intelligence to evaluate business health.

### AI Health Score Logic
Business score starts at 100 and reduces based on:

- Low profit margin
- High discount dependency
- Excess loss-making orders

### Business Status
- Healthy
- Warning
- Critical

Sample recommendations:

- Reduce aggressive discounting
- Improve pricing strategy
- Review loss-making products
- Optimize inventory planning

---

# 💡 Key Insights

Example insights extracted:

- Furniture category has low profit margin due to discounts
- Technology drives high revenue
- Some products consistently generate losses
- Certain regions underperform in profitability

---

# ⚡ SQL Analysis Performed

Example business queries:

- Top-selling products
- Monthly sales trend
- Regional profitability
- Category revenue
- Loss-making products
- Customer segment analysis

---

# ▶️ Run Locally

## Clone repository
```bash
git clone https://github.com/khushikharb/RetailIQ-AI-dashboard-.git
```

## Move into project
```bash
cd RetailIQ-AI-dashboard-
```

## Create virtual environment
```bash
python -m venv venv
```

## Activate environment
Mac/Linux:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run dashboard
```bash
streamlit run app/dashboard.py
```

---

# 📌 Business Impact

RetailIQ AI helps businesses:

✅ Improve profitability  
✅ Detect weak product lines  
✅ Reduce losses  
✅ Monitor KPIs in real time  
✅ Support data-driven decisions  

---

# 🔮 Future Improvements

Planned upgrades:

- Machine Learning sales forecasting
- Demand prediction
- Customer churn prediction
- LLM-powered analytics chatbot
- Automated anomaly detection
- Cloud deployment (AWS / Azure)

---

# 👩‍💻 Author

**Khushi Kharb**  
Data Analyst | Business Analyst | AI/ML Enthusiast  

Skills:
- SQL
- Python
- Excel
- Power BI
- Tableau
- Machine Learning

---

