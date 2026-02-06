import streamlit as st
import pandas as pd
from salary_calculation import calcola_netto_2025
# Note: tax calculations are fixed to the 2025 legislative model implemented in `salary_calculation.py`


st.set_page_config(page_title="Salary Calculator (Italy-2025)", layout="wide", page_icon="💶")

# Custom CSS for a professional dark theme with enhanced gradients
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
        background: linear-gradient(135deg, #424242 0%, #616161 100%);
        color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
        border: 2px solid #ffffff;
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
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #ff4500 0%, #ff8c00 100%);
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
        border: 1px solid #333333;
    }
    .stDataFrame table {
        width: 100%;
        border-collapse: collapse;
    }
    .stDataFrame th {
        background: linear-gradient(135deg, #333333 0%, #555555 100%);
        color: #ffffff;
        padding: 12px;
        text-align: left;
        font-weight: bold;
    }
    .stDataFrame td {
        padding: 12px;
        border-bottom: 1px solid #333333;
    }
    .stDataFrame tr:nth-child(even) {
        background-color: #2a2a2a;
    }
    .stDataFrame tr:hover {
        background-color: #3a3a3a;
    }
    .stContainer {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid #333333;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8c00 100%);
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
col_img, col_sum = st.columns([0.17, 0.83])
with col_img:
    st.image("https://img.icons8.com/color/96/000000/calculator.png", width=80)
with col_sum:
    st.markdown('<div style="font-size: 3em;">📊</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; color: #cccccc; font-size: 16px; margin-bottom: 30px;">
    Estimate your **Net Take-Home Pay** based on current Italian tax brackets and social security rates for 2025.
    </div>
    """,
    unsafe_allow_html=True
)

# Use columns for side-by-side layout with narrower configuration
col1, col2 = st.columns([0.5, 2.5])

with col1:
    gross = st.number_input("Gross annual salary (EUR)", min_value=0.0, value=50000.0, step=1000.0, format="%.2f")
    months = st.selectbox("Number of payments (months)", options=[12, 13, 14], index=1, help="In Italy, 13 or 14 payments are common (Tredicesima/Quattordicesima).")

    with st.expander("Advanced Tax Rates"):
        social_rate = st.number_input("Employee social rate", min_value=0.0, value=0.0919, step=0.001, format="%.4f", help="INPS employee share")
        regional_rate = st.number_input("Regional surtax", min_value=0.0, value=0.0173, step=0.001, format="%.4f", help="Default regional rate per your model")
        municipal_rate = st.number_input("Municipal surtax", min_value=0.0, value=0.008, step=0.001, format="%.4f", help="Default municipal rate per your model")
        # Initialize `last_result` so the UI shows values before any button press
        if 'last_result' not in st.session_state:
            st.session_state['last_result'] = calcola_netto_2025(gross, regione_aliquota=regional_rate, comunale_aliquota=municipal_rate)

    # Persistent Calculate button
    calculate_button = st.button("Calculate My Salary 🚀", use_container_width=True)
    calculate_now = calculate_button

# Calculation logic
# Manual calculate behavior: update stored inputs and result only when the calculate button is pressed
if calculate_now:
    # Store the current input values
    st.session_state['stored_gross'] = gross
    st.session_state['stored_months'] = months
    st.session_state['stored_social_rate'] = social_rate
    st.session_state['stored_regional_rate'] = regional_rate
    st.session_state['stored_municipal_rate'] = municipal_rate
    # Recalculate result
    st.session_state['last_result'] = calcola_netto_2025(st.session_state['stored_gross'], regione_aliquota=st.session_state['stored_regional_rate'], comunale_aliquota=st.session_state['stored_municipal_rate'])

# Use stored values for display, initialize if not set
if 'stored_gross' not in st.session_state:
    st.session_state['stored_gross'] = gross
    st.session_state['stored_months'] = months
    st.session_state['stored_social_rate'] = social_rate
    st.session_state['stored_regional_rate'] = regional_rate
    st.session_state['stored_municipal_rate'] = municipal_rate
    st.session_state['last_result'] = calcola_netto_2025(gross, regione_aliquota=regional_rate, comunale_aliquota=municipal_rate)

# Use the stored last_result for display
dati = st.session_state['last_result']

# Map the detailed fields produced by the model into `result`
result = {
    "gross": dati.get("Gross Annual Salary (RAL)", round(st.session_state['stored_gross'], 2)),
    "social": dati.get("INPS Contributions (contributi INPS)", 0.0),
    "taxable": dati.get("IRPEF Taxable Base (imponibile IRPEF)", 0.0),
    "gross_irpef": dati.get("Gross IRPEF (IRPEF lorda)", 0.0),
    "detrazione_ord": dati.get("Standard Deduction (detrazione ordinaria)", 0.0),
    "detrazione_extra": dati.get("Additional Deduction (ulteriore detrazione)", 0.0),
    "detrazioni_tot": dati.get("Total Deductions (totale detrazioni)", 0.0),
    "irpef": dati.get("Net IRPEF (IRPEF netta)", 0.0),
    "local": dati.get("Surcharges (addizionali reg+com)", 0.0),
    "total_tax": dati.get("Total Taxes (tasse totali IRPEF+addiz)", 0.0),
    "total_withholdings": dati.get("Total Withholdings (totale trattenute)", 0.0),
    "net": dati.get("Annual Net Salary (netto annuo)", 0.0),
}

# Use stored months for monthly calculations
stored_months = st.session_state['stored_months']

with col2:
    # Results container
    with st.container():
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        mcol1.metric("Annual Gross", f"€{result['gross']:,.0f}")
        mcol2.metric("Annual Net", f"€{result['net']:,.0f}")
        # Compute per-payment monthly breakdown using the selected `months`
        monthly = {k: (v / stored_months if isinstance(v, (int, float)) else v) for k, v in result.items()}
        monthly_selected = result.get('net', 0.0) / stored_months if isinstance(result.get('net', 0.0), (int, float)) else result.get('net')
        mcol3.metric("Monthly Net", f"€{monthly_selected:,.0f}")
        mcol4.metric("Total Tax", f"€{result['total_tax']:,.0f}", delta=f"{(result['total_tax']/gross*100):.1f}%", delta_color="inverse")

        st.divider()

        # Detailed table (year + month grouped)
        st.subheader("📋 Detailed Breakdown")
        
        breakdown_data = {
            "Category": [
                "Gross Salary",
                "Social Contributions (INPS)",
                "Taxable Income",
                "Gross IRPEF (IRPEF lorda)",
                "Standard Deduction (detrazione ordinaria)",
                "Additional Deduction (ulteriore detrazione)",
                "Total Deductions (totale detrazioni)",
                "Net IRPEF (IRPEF netta)",
                "Regional/Municipal Tax",
                "Total Taxes",
                "Total Withholdings",
                "Net Salary"
            ],
            "Annual (EUR)": [
                result["gross"],
                result["social"],
                result["taxable"],
                result["gross_irpef"],
                result["detrazione_ord"],
                result["detrazione_extra"],
                result["detrazioni_tot"],
                result["irpef"],
                result["local"],
                result["total_tax"],
                result.get("total_withholdings", result.get("total_tax", 0.0)),
                result["net"]
            ],
            f"Monthly x{stored_months} (EUR)": [
                monthly["gross"], monthly["social"], monthly["taxable"], monthly["gross_irpef"], monthly["detrazione_ord"], monthly["detrazione_extra"], monthly["detrazioni_tot"], monthly["irpef"], monthly["local"], monthly["total_tax"], monthly.get("total_withholdings", monthly.get("total_tax", 0.0)), monthly["net"]
            ]
        }
        
        df_breakdown = pd.DataFrame(breakdown_data)
        
        # Format as currency
        for col in ["Annual (EUR)", f"Monthly x{stored_months} (EUR)"]:
            df_breakdown[col] = df_breakdown[col].apply(lambda x: f"€ {x:,.2f}")

        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
        st.success("✅ Calculation completed! Review your salary breakdown above.")
        with st.expander("ℹ️ Assumptions & Tax Methodology"):
            st.write(
                "- IRPEF brackets: 23% up to €28k, 35% €28–50k, 43% above €50k."
            )
            st.write("- Employee social rate default: 9.19% (configurable in sidebar).")
            st.write("- Standard employee deductions and an additional deduction (Law 207/2024) are applied to calculate net IRPEF.")
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
