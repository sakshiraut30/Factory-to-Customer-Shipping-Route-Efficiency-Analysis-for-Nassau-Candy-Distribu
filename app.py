import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Factory-to-Customer Shipping Dashboard",
    layout="wide"
)

# =========================
# DARK THEME
# =========================
st.markdown("""
<style>
    .block-container { padding-top: 1rem; }

    .stApp {
        background-color: #2b2b2b;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #2b2b2b;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Nassau Candy Distributor.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
df = df.dropna(subset=["Order Date", "Ship Date"])

df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df = df[df["Lead Time"] >= 0]

df["Route"] = df["Country/Region"] + " → " + df["State/Province"]

# =========================
# TITLE
# =========================
st.markdown("""
<h1 style='text-align:center; color:#7ec8ff;'>
Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor
</h1>
<p style='text-align:center; color:white;'>
Logistics Performance Dashboard
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# KPI CALCULATIONS
# =========================
avg_lead = round(df["Lead Time"].mean(), 2)
route_volume = df.groupby("Route").size().mean().round(2)
delay_frequency = round((df["Lead Time"] > df["Lead Time"].mean()).mean() * 100, 1)
route_efficiency = round(100 - (df["Lead Time"].mean() / df["Lead Time"].max()) * 100, 1)

# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

def kpi(title, value):
    return f"""
    <div style="
        background:black;
        padding:16px;
        border-radius:12px;
        text-align:center;
        border:1px solid #333;
        height:120px;
        display:flex;
        flex-direction:column;
        justify-content:center;
    ">
        <h5 style="color:#7ec8ff; margin:0;">{title}</h5>
        <h2 style="color:white; margin:5px 0;">{value}</h2>
    </div>
    """

col1.markdown(kpi("Avg Lead Time", f"{avg_lead} days"), unsafe_allow_html=True)
col2.markdown(kpi("Route Volume", f"{route_volume}"), unsafe_allow_html=True)
col3.markdown(kpi("Delay Frequency", f"{delay_frequency}%"), unsafe_allow_html=True)
col4.markdown(kpi("Efficiency Score", f"{route_efficiency}%"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# CHART STYLE
# =========================
def dark_chart(fig):
    fig.update_layout(
        paper_bgcolor="#2b2b2b",
        plot_bgcolor="#2b2b2b",
        font=dict(color="white"),
        title=dict(font=dict(color="#7ec8ff"), x=0.5)
    )
    return fig

# =========================
# GROUP DATA
# =========================
region_df = df.groupby("Region")["Lead Time"].mean().reset_index()
ship_df = df.groupby("Ship Mode")["Lead Time"].mean().reset_index()
route_df = df.groupby("Route")["Lead Time"].mean().reset_index()

# =========================
# ROW 1 - 3 CHARTS
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    fig1 = px.scatter(df, x="Order Date", y="Lead Time", color="Region",
                      title="Lead Time Trend (Scatter)")
    fig1.update_traces(marker=dict(size=5))
    st.plotly_chart(dark_chart(fig1), use_container_width=True)

with c2:
    fig2 = px.line(region_df, x="Region", y="Lead Time",
                   title="Region Performance (Line)")
    st.plotly_chart(dark_chart(fig2), use_container_width=True)

with c3:
    fig3 = px.bar(ship_df, x="Ship Mode", y="Lead Time",
                  title="Ship Mode Comparison (Bar)")
    st.plotly_chart(dark_chart(fig3), use_container_width=True)

# =========================
# ROW 2 - 3 CHARTS
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    fig4 = px.histogram(df, x="Lead Time", nbins=20,
                        title="Lead Time Distribution")
    st.plotly_chart(dark_chart(fig4), use_container_width=True)

with c2:
    fig5 = px.box(df, x="Region", y="Lead Time", color="Region",
                  title="Lead Time Spread by Region")
    st.plotly_chart(dark_chart(fig5), use_container_width=True)

with c3:
    fig6 = px.violin(df, x="Ship Mode", y="Lead Time", box=True,
                     title="Lead Time Variation (Violin)")
    st.plotly_chart(dark_chart(fig6), use_container_width=True)

# =========================
# TABLE
# =========================
st.markdown("### Data View")

styled_df = df.style.set_properties(
    **{
        "background-color": "#2b2b2b",
        "color": "white"
    }
)

st.dataframe(styled_df, use_container_width=True)