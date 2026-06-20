import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="RetailIQ AI",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# LOAD CSS
# -------------------------
with open("app/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("data/dashboard/dashboard_dataset.csv")

df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("🛒 RetailIQ AI")
st.sidebar.caption("Automated Retail Intelligence")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["category"].unique()),
    default=sorted(df["category"].unique())
)

segments = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df["segment"].unique()),
    default=sorted(df["segment"].unique())
)

filtered_df = df[
    (df["region"].isin(regions)) &
    (df["category"].isin(categories)) &
    (df["segment"].isin(segments))
]

# -------------------------
# KPI CALCULATIONS
# -------------------------
total_revenue = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
profit_margin = (total_profit / total_revenue) * 100 if total_revenue != 0 else 0
total_orders = filtered_df["order_id"].nunique()
units_sold = filtered_df["quantity"].sum()
aov = total_revenue / total_orders if total_orders != 0 else 0

# -------------------------
# KPI CARD FUNCTION
# -------------------------
def metric_card(title, value, emoji, css_class):
    st.markdown(
        f"""
        <div class="metric-card {css_class}">
            <h4>{emoji} {title}</h4>
            <h2>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# HEADER
# -------------------------
st.title("📊 RetailIQ AI Dashboard")
st.caption("Enterprise Retail Sales Analytics Platform")

# -------------------------
# KPI CARDS
# -------------------------
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    metric_card("Revenue", f"${total_revenue:,.0f}", "💰", "blue")

with c2:
    metric_card("Profit", f"${total_profit:,.0f}", "📈", "green")

with c3:
    metric_card("Margin", f"{profit_margin:.2f}%", "🎯", "purple")

with c4:
    metric_card("Orders", f"{total_orders}", "🧾", "orange")

with c5:
    metric_card("AOV", f"${aov:,.0f}", "🛒", "cyan")

# -------------------------
# ROW 1
# -------------------------
left, right = st.columns([2,1])

with left:
    monthly = filtered_df.groupby("order_month")["sales"].sum().reset_index()

    fig = px.area(
        monthly,
        x="order_month",
        y="sales",
        title="Monthly Revenue Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=profit_margin,
        title={"text": "Profit Margin"},
        gauge={
            "axis": {"range": [0, 30]},
            "steps": [
                {"range": [0, 10]},
                {"range": [10, 20]},
                {"range": [20, 30]}
            ]
        }
    ))

    st.plotly_chart(gauge, use_container_width=True)

# -------------------------
# ROW 2
# -------------------------
col1, col2 = st.columns(2)

with col1:
    category_sales = (
        filtered_df.groupby("category")["sales"]
        .sum()
        .reset_index()
    )

    fig = px.treemap(
        category_sales,
        path=["category"],
        values="sales",
        title="Revenue by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    region_sales = (
        filtered_df.groupby("region")["sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        region_sales,
        x="region",
        y="sales",
        title="Regional Revenue"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# ROW 3
# -------------------------
col1, col2 = st.columns(2)

with col1:
    top_products = (
        filtered_df.groupby("product_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="sales",
        y="product_name",
        orientation="h",
        title="Top 10 Products"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    loss_products = (
        filtered_df.groupby("product_name")["profit"]
        .sum()
        .sort_values()
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        loss_products,
        x="product_name",
        y="profit",
        title="Loss-Making Products"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# AI ENGINE
# -------------------------
score = 100
recommendations = []

if profit_margin < 12:
    score -= 20
    recommendations.append(
        "Profit margin is below target. Reduce aggressive discounts."
    )

if filtered_df["discount"].mean() > 0.25:
    score -= 20
    recommendations.append(
        "High discount dependency detected."
    )

loss_orders = len(filtered_df[filtered_df["profit"] < 0])

if loss_orders > 1000:
    score -= 20
    recommendations.append(
        "Large number of loss-making orders."
    )

if score >= 80:
    health = "Healthy"
elif score >= 50:
    health = "Warning"
else:
    health = "Critical"

st.subheader("🧠 AI Business Health")

st.markdown(
    f"""
    <div class='ai-card'>
        <h3>Status: {health}</h3>
        <h4>Business Score: {score}/100</h4>
    </div>
    """,
    unsafe_allow_html=True
)

for rec in recommendations:
    st.info(rec)

# -------------------------
# DOWNLOAD BUTTON
# -------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Report",
    csv,
    "retail_report.csv",
    "text/csv"
)