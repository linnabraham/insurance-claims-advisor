"""Streamlit frontend for the Claims Triage application."""

import requests
import streamlit as st

st.set_page_config(
    page_title="Claims Advisor",
    page_icon="📋",
    layout="wide",
)

st.title("Insurance Claim Triage and Decision Support")
st.write("Upload a claim and a policy document to receive a structured assessment.")

# Upload section
col1, col2 = st.columns(2)
with col1:
    claim_file = st.file_uploader("Upload Claim Document", type=["pdf", "txt"])
with col2:
    policy_file = st.file_uploader("Upload Policy Document", type=["pdf", "txt"])

analyze_button = st.button("Analyze Claim", type="primary")

# Output sections (all placeholders for now)
if analyze_button:
    st.info("Analysis would run here once the backend is connected.")

    st.subheader("Claim Summary")
    st.write("_Placeholder: plain-English summary of the claim._")

    st.subheader("Policy Relevance Analysis")
    st.write("_Placeholder: relevant policy clauses._")

    st.subheader("Coverage Determination")
    st.write("_Placeholder: whether claim falls within coverage._")

    st.subheader("Anomaly and Fraud Signals")
    st.write("_Placeholder: detected anomalies._")

    st.subheader("Recommended Action")
    st.write("_Placeholder: Approve / Reject / Escalate / Request Info._")

    st.subheader("Confidence Indicator")
    st.write("_Placeholder: system confidence level._")

if st.button("Check API Health"):
    response = requests.get("http://localhost:8010/health")
    st.json(response.json())
