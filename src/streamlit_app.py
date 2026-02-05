import streamlit as st
import pandas as pd
from tax import compute_net_from_gross


st.set_page_config(page_title="Salary Calculator (Italy-2025)", layout="wide", page_icon="💶")

# Custom CSS for a professional dark theme
st.markdown("""
    <style>
    .main {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp {
        background-color: #121212;
    }
    .stTitle {
        color: #ffffff;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
    }
    .stMarkdown {
        color: #e0e0e0;
    }
    .stMetric {
        background: linear-gradient(135deg, #333333 0%, #555555 100%);
        color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
    }
    .stMetric label {
        color: #ffffff !important;
        font-size: 14px;
    }
    .stMetric .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
    }
    .stMetric .metric-delta {
        font-size: 12px;
        color: #90ee90;
    }
    .stButton button {
        background-color: #6200ea;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #3700b3;
    }
    .stExpander {
        background-color: #1e1e1e;
        border: 1px solid #333333;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        color: #ffffff;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .stProgress > div > div > div {
        background-color: #ff6b6b;
    }
    .sidebar .sidebar-content {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .stSelectbox, .stNumberInput {
        border-radius: 8px;
        background-color: #2c2c2c;
        color: #ffffff;
    }
    .stSelectbox div, .stNumberInput input {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💶 Salary Calculator (Italy-2025)")
st.markdown(
    "Estimate your **Net Take-Home Pay** based on current Italian tax brackets and social security rates."
)

# Sidebar inputs for cleaner layout
with st.sidebar.form(key="inputs"):
    st.header("⚙️ Configuration")
    gross = st.number_input("Gross annual salary (EUR)", min_value=0.0, value=50000.0, step=1000.0, format="%.2f")
    months = st.selectbox("Number of payments (months)", options=[12, 13, 14], index=1, help="In Italy, 13 or 14 payments are common (Tredicesima/Quattordicesima).")
    
    with st.expander("Advanced Tax Rates"):
        social_rate = st.number_input("Employee social rate", min_value=0.0, value=0.0919, step=0.001, format="%.4f", help="INPS employee share")
        regional_rate = st.number_input("Regional surtax", min_value=0.0, value=0.0100, step=0.001, format="%.4f")
        municipal_rate = st.number_input("Municipal surtax", min_value=0.0, value=0.0023, step=0.001, format="%.4f")
        
    submitted = st.form_submit_button("Calculate My Salary 🚀", use_container_width=True)

# Calculation logic
if submitted or 'initialized' not in st.session_state:
    st.session_state.initialized = True
    result = compute_net_from_gross(gross, social_rate, regional_rate, municipal_rate)
    monthly = {k: (v / months if isinstance(v, (int, float)) else v) for k, v in result.items()}

    # Top metrics in a nice card-like layout
    st.write("### 📊 Summary")
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("Annual Gross", f"€{result['gross']:,.0f}")
    mcol2.metric("Annual Net", f"€{result['net']:,.0f}")
    mcol3.metric(f"Monthly Net ({months}x)", f"€{monthly['net']:,.0f}")
    mcol4.metric("Total Tax", f"€{result['total_tax']:,.0f}", delta=f"{(result['total_tax']/gross*100):.1f}%", delta_color="inverse")

    st.divider()

    # Detailed table (year + month grouped)
    st.subheader("📋 Detailed Breakdown")
    
    breakdown_data = {
        "Category": ["Gross Salary", "Social Contributions (INPS)", "Taxable Income", "IRPEF (Income Tax)", "Regional/Municipal Tax", "Total Taxes", "Net Salary"],
        "Annual (EUR)": [
            result["gross"], result["social"], result["taxable"], result["irpef"], result["local"], result["total_tax"], result["net"]
        ],
        f"Monthly x{months} (EUR)": [
            monthly["gross"], monthly["social"], monthly["taxable"], monthly["irpef"], monthly["local"], monthly["total_tax"], monthly["net"]
        ]
    }
    
    df_breakdown = pd.DataFrame(breakdown_data)
    
    # Format as currency
    for col in ["Annual (EUR)", f"Monthly x{months} (EUR)"]:
        df_breakdown[col] = df_breakdown[col].apply(lambda x: f"€ {x:,.2f}")

    st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

    with st.expander("ℹ️ Assumptions & Tax Methodology"):
        st.write(
            "- IRPEF brackets: 23% up to €15k, 25% €15–28k, 35% €28–50k, 43% above €50k."
        )
        st.write("- Employee social rate default: 9.19% (configurable in sidebar).")
        st.write("- Regional & municipal surtaxes are estimated and configurable.")
        st.write("- This is an estimate for quick planning; consult a tax advisor for exact figures.")

    # Professional footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #888888; font-size: 12px;">
        © 2025 Italy Salary Calculator | Built with ❤️ using Streamlit | For informational purposes only
        </div>
        """,
        unsafe_allow_html=True
    )
