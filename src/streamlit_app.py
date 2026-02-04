import streamlit as st
import pandas as pd
from tax import compute_net_from_gross


st.set_page_config(page_title="Salary Calculator (Italy 2025)", layout="wide")

st.title("💶 Salary net calculator — Italy (approx. 2025)")
st.markdown(
    "Enter gross annual salary and optional rates. Use the sidebar to adjust values. This is an estimator for quick planning — consult a tax advisor for exact figures."
)

# Sidebar inputs for cleaner layout
with st.sidebar.form(key="inputs"):
    st.header("Inputs")
    gross = st.number_input("Gross annual salary (EUR)", min_value=0.0, value=50000.0, step=500.0, format="%.2f")
    social_rate = st.number_input("Employee social rate (fraction)", min_value=0.0, value=0.0919, step=0.001, format="%.4f")
    regional_rate = st.number_input("Regional surtax (fraction)", min_value=0.0, value=0.01, step=0.001, format="%.4f")
    municipal_rate = st.number_input("Municipal surtax (fraction)", min_value=0.0, value=0.0023, step=0.001, format="%.4f")
    submitted = st.form_submit_button("Calculate")

if submitted:
    result = compute_net_from_gross(gross, social_rate, regional_rate, municipal_rate)
    monthly = {k: (v / 12 if isinstance(v, (int, float)) else v) for k, v in result.items()}

    # Top metrics
    mcol1, mcol2, mcol3 = st.columns([1, 1, 1])
    mcol1.metric("Gross (year)", f"€{result['gross']:,.2f}")
    mcol2.metric("Net (year)", f"€{result['net']:,.2f}")
    mcol3.metric("Net (month)", f"€{monthly['net']:,.2f}")

    # Visual breakdown: bar chart + progress
    left, right = st.columns([2, 1])

    # Prepare data for chart: yearly shares
    shares = {
        'Net': result['net'],
        'Social': result['social'],
        'IRPEF': result['irpef'],
        'Local': result['local'],
    }
    df_shares = pd.DataFrame(list(shares.items()), columns=['Part', 'Amount'])

    left.subheader("Annual distribution")
    left.bar_chart(df_shares.set_index('Part'))

    # show tax rate as a progress bar (percent of gross)
    tax_share = (result['total_tax'] / result['gross']) if result['gross'] > 0 else 0
    right.subheader("Tax burden")
    right.metric("Total tax (yr)", f"€{result['total_tax']:,.2f}", delta=f"{tax_share*100:.1f}% of gross")
    right.progress(min(1.0, tax_share))

    # Detailed table (year + month grouped)
    breakdown = pd.DataFrame([
        ["Gross (year)", result["gross"]],
        ["Gross (month)", monthly["gross"]],
        ["Social (year)", result["social"]],
        ["Social (month)", monthly["social"]],
        ["IRPEF (year)", result["irpef"]],
        ["IRPEF (month)", monthly["irpef"]],
        ["Regional+Municipal (year)", result["local"]],
        ["Regional+Municipal (month)", monthly["local"]],
        ["Total tax (year)", result["total_tax"]],
        ["Total tax (month)", monthly["total_tax"]],
        ["Net (year)", result["net"]],
        ["Net (month)", monthly["net"]],
    ], columns=["Item", "Amount (EUR)"])

    breakdown["Amount (EUR)"] = breakdown["Amount (EUR)"].apply(lambda x: f"€{x:,.2f}")
    st.subheader("Breakdown")
    st.table(breakdown.set_index("Item"))

    with st.expander("Assumptions & notes"):
        st.write(
            "- IRPEF brackets: 23% up to €15k, 25% €15–28k, 35% €28–50k, 43% above €50k."
        )
        st.write("- Employee social rate default: 9.19% (configurable in sidebar).")
        st.write("- Regional & municipal surtaxes are estimated and configurable.")
        st.write("- This is an estimate for quick planning; consult a tax advisor for exact figures.")
