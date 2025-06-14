import streamlit as st

# App title
st.title("NGS Reimbursement Optimization Tool")

# Section 1: Input Panel Information
st.header("Step 1: Test Information")
test_type = st.selectbox("Select Test Type", [
    "Solid Tumor – DNA Panel",
    "Solid Tumor – RNA Panel",
    "Solid Tumor – DNA + RNA Panel",
    "Hematologic – DNA Panel",
    "Hematologic – RNA Panel",
    "Hematologic – DNA + RNA Panel",
    "Liquid Biopsy – ctDNA",
    "Whole Exome (WES)",
    "Whole Genome (WGS)"
])

gene_count = st.slider("Number of Genes in Panel", 1, 500, 50)
lab_cost = st.number_input("Enter Total Lab Cost per Sample ($)", min_value=0.0, value=350.0)
inpatient_pct = st.slider("% of Inpatient Volume (14-Day Rule Applies)", 0, 100, 30)

toggle_strategy = st.radio("Carve-Out Strategy Source", [
    "Same Genome (multiple CPTs per sample)",
    "Separate Genomes (one CPT per sample)"
])

# Section 2: CPT Code Logic
if gene_count > 50:
    recommended_cpt = "81455"
    reimbursement = 2919.60
    flagged_payers = ["UnitedHealthcare", "Aetna", "Cigna", "Blue Cross Blue Shield", "Humana"]
    warning = "Many private payers restrict reimbursement for panels >50 genes. Often reimbursed at 81450 rate or denied unless clinical justification is strong."
else:
    recommended_cpt = "81450"
    reimbursement = 759.53
    flagged_payers = []
    warning = "Generally covered for hereditary or myeloid panels ≤50 genes."

st.markdown(f"### Recommended CPT Code: **{recommended_cpt}**")
st.markdown(f"Medicare Reimbursement Estimate: **${reimbursement:,.2f}**")

if warning:
    st.warning(warning)
    if flagged_payers:
        st.markdown("**Flagged Payers:**")
        for payer in flagged_payers:
            st.markdown(f"- {payer}")

# Section 3: ROI Simulation
st.header("Step 2: ROI Simulation")
carve_out_panels = st.slider("How many carve-out panels do you report per genome?", 1, 5, 2)
backbone_cpt_reimb = st.number_input("Backbone CPT Reimbursement (if billed) - e.g. 81425 for WGS", value=5500.0)
backbone_cost = st.number_input("Backbone Sequencing Cost (e.g., WES/WGS) per Sample", value=728.0)

# Strategy A: Carve-outs only
panel_profit = reimbursement - lab_cost
revenue_a = reimbursement * carve_out_panels
profit_a = revenue_a - backbone_cost

# Strategy B: Carve-outs + backbone billed
revenue_b = (reimbursement * carve_out_panels) + backbone_cpt_reimb
profit_b = revenue_b - backbone_cost

st.subheader("Scenario A: Only Panel CPTs Billed")
st.markdown(f"**Total Revenue:** ${revenue_a:,.2f}")
st.markdown(f"**Profit:** ${profit_a:,.2f}")

st.subheader("Scenario B: Panel + Backbone CPT Billed")
st.markdown(f"**Total Revenue:** ${revenue_b:,.2f}")
st.markdown(f"**Profit:** ${profit_b:,.2f}")

min_panels = backbone_cost / panel_profit if panel_profit > 0 else float('inf')
st.markdown(f"**Panels needed to break even if backbone is NOT billed:** {min_panels:.2f}")
