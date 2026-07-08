import streamlit as st
import requests
import uuid
import pandas as pd
import json

# Setup page configurations
st.set_page_config(
    page_title="BNP Paribas Churn Intelligence Dashboard",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import os

# API endpoint URL
API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api")


# Design and style customizations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    .main {
        background-color: #F8FAFC;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', 'Segoe UI', sans-serif;
    }
    
    body, p, span, div, button, label {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #fcfdfd 100%);
        padding: 22px 15px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.02), 0 2px 6px rgba(0,0,0,0.01);
        border: 1px solid #E2E8F0;
        border-top: 5px solid #007A48;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 36px rgba(0, 122, 72, 0.06), 0 6px 16px rgba(0, 0, 0, 0.02);
        border-color: #CBD5E1;
    }
    
    .kpi-card-total { border-top-color: #007A48; }
    .kpi-card-churned { border-top-color: #EF4444; }
    .kpi-card-rate { border-top-color: #F59E0B; }
    .kpi-card-tenure { border-top-color: #3B82F6; }
    
    .kpi-title {
        font-size: 12px;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 32px;
        color: #0F172A;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
    }
    
    .trace-card {
        background-color: #FFFFFF;
        padding: 18px 22px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01), 0 2px 4px -1px rgba(0,0,0,0.01);
        margin-bottom: 14px;
        transition: all 0.2s ease;
    }
    
    .trace-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.02);
    }
    
    .badge {
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-success {
        background-color: #DCFCE7;
        color: #15803D;
    }
    .badge-warning {
        background-color: #FEF3C7;
        color: #B45309;
    }
    .badge-danger {
        background-color: #FEE2E2;
        color: #B91C1C;
    }
    
    /* Premium Streamlit Form Customizations */
    button[kind="primary"] {
        background-color: #007A48 !important;
        border-color: #007A48 !important;
        border-radius: 8px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    div[data-testid="stExpander"] {
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01) !important;
        background-color: #FFFFFF !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stExpander"] p, 
    div[data-testid="stExpander"] span, 
    div[data-testid="stExpander"] b, 
    div[data-testid="stExpander"] strong, 
    div[data-testid="stExpander"] li,
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] div,
    div[data-testid="stExpander"] label {
        color: #1E3A8A !important; /* Premium Deep Blue */
    }
    div[data-testid="stExpander"] code {
        color: #0F172A !important;
        background-color: #F1F5F9 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to query statistics
def get_stats():
    try:
        response = requests.get(f"{API_URL}/statistics")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error connecting to backend API: {e}")
    return None

# State Initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None
if "recent_sessions" not in st.session_state:
    st.session_state.recent_sessions = []


# Fetch Stats for Top Dashboard Bar
stats = get_stats()

# Main Layout
# Header with logo in the top-left
header_col1, header_col2 = st.columns([1, 6])
with header_col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/85/BNP_Paribas_logo.svg", width=110)
with header_col2:
    st.markdown("<h1 style='margin: 0; color: #007A48; line-height: 1.1;'>BNP Paribas | Churn Intelligence Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 16px; margin-top: 4px; margin-bottom: 0;'>AI-driven churn analytics, risk prediction, strategy blueprinting, and factual compliance validations.</p>", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
st.markdown("---")

# Render KPI stats cards if available
if stats:
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"""
            <div class='kpi-card kpi-card-total'>
                <div class='kpi-title'>Total Portfolio Clients</div>
                <div class='kpi-value'>{stats.get('total_customers', 0):,}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
            <div class='kpi-card kpi-card-churned'>
                <div class='kpi-title'>Churned Clients (Historical)</div>
                <div class='kpi-value'>{stats.get('churned_customers', 0):,}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div class='kpi-card kpi-card-rate'>
                <div class='kpi-title'>Identified Churn Rate</div>
                <div class='kpi-value'>{stats.get('churn_rate', 0.0)}%</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
            <div class='kpi-card kpi-card-tenure'>
                <div class='kpi-title'>Average Client Tenure</div>
                <div class='kpi-value'>{stats.get('average_tenure', 0.0)} mo</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Warning: Could not connect to API backend to load statistics. Please ensure the FastAPI backend is running.")

st.markdown("<br>", unsafe_allow_html=True)

# Main Tabbed Interface
tab_exec, tab_analytics, tab_trace, tab_guardrails, tab_report, tab_console = st.tabs([
    "🚀 Execute Analysis Query",
    "📊 Portfolio KPI & Churn Analytics",
    "🔍 Agent Workflow Explainability",
    "🛡️ Guardrails & Compliance Audit",
    "📄 Executive Report & PDF Export",
    "📂 Ingest Custom Dataset"
])

# ================= TAB 1: EXECUTE RUN =================
with tab_exec:
    st.markdown("### Run Agentic Customer Churn Analysis Pipeline")
    st.markdown("Input a question or specify a customer account ID to execute risk scoring and compile a strategic retention report.")
    
    query_input = st.text_input(
        "Enter your query:", 
        value="Identify high-risk month-to-month customers and provide a retention strategy",
        placeholder="e.g. Predict churn risk for customer 14, or Analyze why month-to-month contracts are churning."
    )
    
    if st.button("Kickoff Agent Workflow 🟢"):
        if not query_input.strip():
            st.error("Please enter a valid query.")
        else:
            with st.spinner("Executing query understanding, RAG retrieval, analysis, prediction, validation, and reporting (this might take up to a minute)..."):
                try:
                    payload = {
                        "query": query_input,
                        "session_id": st.session_state.session_id
                    }
                    response = requests.post(f"{API_URL}/run", json=payload)
                    
                    if response.status_code == 200:
                        st.session_state.workflow_result = response.json()
                        st.success("Workflow completed successfully! Review the tabs above for results.")
                        # Add to local session log
                        if st.session_state.session_id not in st.session_state.recent_sessions:
                            st.session_state.recent_sessions.append(st.session_state.session_id)
                    elif response.status_code == 400:
                        st.error(f"Guardrail Input Error: {response.json().get('detail')}")
                    elif response.status_code == 422:
                        st.error(f"Guardrail Output Failure: {response.json().get('detail')}")
                    else:
                        st.error(f"Execution failed. Status: {response.status_code}. Detail: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"An unexpected connection error occurred: {e}")

    # Display basic overview of current session results
    if st.session_state.workflow_result:
        res = st.session_state.workflow_result
        st.markdown("---")
        st.markdown("### Latest Execution Summary")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown(f"**Session UUID:** `{res.get('session_id')}`")
            st.markdown(f"**User Request:** *{res.get('query_plan', {}).get('user_query', '')}*")
            st.markdown(f"**Determined Intent:** `{res.get('query_plan', {}).get('intent', '')}`")
        with col_res2:
            st.markdown(f"**Targeted Client Account:** `{res.get('query_plan', {}).get('customer_id') or 'RAG Cohort (None Specified)'}`")
            st.markdown(f"**Business Goal Identified:** {res.get('query_plan', {}).get('business_goal', 'Analyze and mitigate churn risk')}")

# ================= TAB 2: PORTFOLIO KPI & CHURN ANALYTICS =================
with tab_analytics:
    st.markdown("### Portfolio KPI & Churn Analytics")
    st.markdown("Overview of customer segmentation and risk metrics computed directly from ChromaDB.")
    
    if stats:
        dist_col, charts_col = st.columns([1, 2])
        
        with dist_col:
            st.markdown("#### Risk Level Distributions")
            r_dist = stats.get("risk_distribution", {})
            
            df_dist = pd.DataFrame({
                "Risk Level": list(r_dist.keys()),
                "Client Count": list(r_dist.values())
            })
            st.dataframe(df_dist, hide_index=True, width="stretch")
            
            st.markdown("#### Database Summary Stats")
            st.write(f"- **Avg Age:** {stats.get('average_age')} years")
            st.write(f"- **Avg Tenure:** {stats.get('average_tenure')} months")
            st.write(f"- **Churn Rate:** {stats.get('churn_rate')}%")
            
        with charts_col:
            st.markdown("#### Risk Category Segments")
            st.bar_chart(data=df_dist, x="Risk Level", y="Client Count", color="#007A48", width="stretch")
            
        # Draw all customer metadata lookup
        st.markdown("---")
        st.markdown("#### Client Account Browser (ChromaDB Vector Store)")
        if st.checkbox("Show database customer list"):
            try:
                cust_res = requests.get(f"{API_URL}/customers?limit=100")
                if cust_res.status_code == 200:
                    cust_list = cust_res.json()
                    df_cust = pd.DataFrame(cust_list)
                    # Clean column names
                    df_cust = df_cust.rename(columns={
                        "contract": "Contract Type",
                        "tenure": "Tenure (Months)",
                        "support_tickets": "Support Tickets",
                        "monthly_charges": "Monthly Charges",
                        "churn": "Churn Status"
                    })
                    st.dataframe(df_cust, width="stretch")
            except Exception as e:
                st.error(f"Error fetching customer list: {e}")
    else:
        st.info("No statistics available. Please start the backend database to view analytics.")

# ================= TAB 3: AGENT WORKFLOW EXPLAINABILITY =================
with tab_trace:
    st.markdown("### Agent Workflow Trace & Explainability Logs")
    st.markdown("Inspect the evidence, logical reasoning, and confidence score generated by each individual agent.")

    if not st.session_state.workflow_result:
        st.info("No execution trace found. Please run a query in the first tab to inspect agent explainability logs.")
    else:
        res = st.session_state.workflow_result
        stages = [
            ("analysis", "🟢 Stage 1: RAG Data Analyst"),
            ("prediction", "🔮 Stage 2: Churn Prediction Specialist"),
            ("recommendation", "💡 Stage 3: Customer Retention Specialist"),
            ("validation", "🛡️ Stage 4: AI Validation Auditor"),
            ("report", "📝 Stage 5: Executive Business Reporter")
        ]
        
        for key, title in stages:
            stage_data = res.get(key)
            if not stage_data:
                st.markdown(f"#### {title} (SKIPPED / NOT EXECUTED)")
                continue
                
            with st.expander(f"{title} (Confidence: {stage_data.get('confidence') or stage_data.get('overall_confidence') or 'N/A'}%)", expanded=True):
                # Core output summary
                if key == "analysis":
                    st.markdown(f"**Analysis Question:** {stage_data.get('question')}")
                    st.markdown(f"**Business Summary:** {stage_data.get('summary')}")
                    st.write("**Calculated Run Statistics:**", stage_data.get("statistics", {}))
                elif key == "prediction":
                    st.markdown(f"**Customer ID:** `{stage_data.get('customer_id')}`")
                    st.markdown(f"**Predicted Risk Level:** `{stage_data.get('risk_level')}`")
                    st.write("**Identified Risk Factors:**")
                    for r in stage_data.get("reasons", []):
                        st.write(f"- {r}")
                elif key == "recommendation":
                    st.markdown(f"**Customer ID:** `{stage_data.get('customer_id')}`")
                    st.markdown(f"**Strategy Execution Priority:** `{stage_data.get('priority')}`")
                    col_rec1, col_rec2 = st.columns(2)
                    with col_rec1:
                        st.write("**Retention Actions:**")
                        for a in stage_data.get("retention_actions", []):
                            st.write(f"- {a}")
                    with col_rec2:
                        st.write("**Upsell Opportunities:**")
                        for u in stage_data.get("upsell_opportunities", []):
                            st.write(f"- {u}")
                elif key == "validation":
                    is_val = stage_data.get("is_valid")
                    badge_cls = "badge-success" if is_val else "badge-danger"
                    st.markdown(f"**Validation Status:** <span class='badge {badge_cls}'>{'PASSED' if is_val else 'FLAGGED'}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Audit Remarks:** *{stage_data.get('remarks')}*")
                elif key == "report":
                    st.markdown(f"**Executive Summary:** {stage_data.get('executive_summary')}")
                    st.markdown(f"**Overall Portfolio Risk Assessment:** {stage_data.get('risk_assessment')}")
                    st.write("**Core Findings:**")
                    for f in stage_data.get("key_findings", []):
                        st.write(f"- {f}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Logical reasoning
                st.markdown(f"**🧠 Agent Logical Reasoning:**")
                st.info(stage_data.get("reasoning", "No reasoning details returned by agent."))
                
                # Factual evidence list
                st.markdown(f"**📎 Supporting Evidence & Context Citations:**")
                evidence_list = stage_data.get("evidence", [])
                if not evidence_list:
                    st.write("*No explicit evidence logged.*")
                else:
                    for ev in evidence_list:
                        st.write(f"- `{ev}`")

# ================= TAB 4: GUARDRAILS & COMPLIANCE AUDIT =================
with tab_guardrails:
    st.markdown("### Guardrails & Compliance Audit")
    st.markdown("Review system-level input and output safety checks, hallucination checks, and mathematical validation status.")

    if not st.session_state.workflow_result:
        st.info("No audit logs found. Run a query to inspect compliance and guardrail checks.")
    else:
        res = st.session_state.workflow_result
        val = res.get("validation", {})
        
        if not val:
            st.warning("⚠️ The validation audit was not run for this query execution plan.")
        else:
            is_valid = val.get("is_valid", False)
            
            if is_valid:
                st.success("✅ SYSTEM COMPLIANCE STATUS: PASSED. All input and output parameters are certified.")
            else:
                st.error("🚨 SYSTEM COMPLIANCE STATUS: FLAGGED. Inconsistencies or discrepancies were detected in the workflow outputs.")
                
            st.markdown("---")
            st.markdown("#### Audit Verification Checklist")
            
            checklists = [
                ("Input Query Guardrail", "PASSED", "Verified safe, relevant, and clean of injections."),
                ("Hallucination Checker", "PASSED" if not val.get("hallucination_detected") else "FAILED", "Checks for factually fabricated accounts, values, or names."),
                ("Confidence Score Verification", "PASSED" if val.get("confidence_verified") else "FAILED", "Verifies confidence metrics correspond to reasoning guidelines."),
                ("Numerical Validation", "PASSED" if val.get("numerical_validation") else "FAILED", "Checks calculations for sum of churns, churn rates, and averages."),
                ("Supporting Evidence Verification", "PASSED" if val.get("evidence_available") else "FAILED", "Validates that recommendations are tied to specific citations.")
            ]
            
            for check, status, description in checklists:
                col_c1, col_c2, col_c3 = st.columns([2, 1, 3])
                with col_c1:
                    st.markdown(f"**{check}**")
                with col_c2:
                    badge_color = "badge-success" if status == "PASSED" else "badge-danger"
                    st.markdown(f"<span class='badge {badge_color}'>{status}</span>", unsafe_allow_html=True)
                with col_c3:
                    st.write(description)
                    
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Auditor Summary Remarks")
            st.info(val.get("remarks", "No validation remarks available."))

# ================= TAB 5: EXECUTIVE REPORT & PDF EXPORT =================
with tab_report:
    st.markdown("### Executive Report & PDF Export")
    st.markdown("Read the synthesized executive report and download the official BNP Paribas Customer Churn PDF report.")

    if not st.session_state.workflow_result:
        st.info("No report generated. Run a query in the first tab to compile an executive report.")
    else:
        res = st.session_state.workflow_result
        rep = res.get("report", {})
        
        if not rep:
            st.warning("⚠️ Executive Report generation was skipped in the execution plan.")
        else:
            st.markdown(f"## {rep.get('risk_assessment', 'Overall Assessment')}")
            st.markdown(f"**Overall System Confidence:** `{rep.get('overall_confidence')}%`")
            st.markdown("---")
            
            st.markdown("#### 1. Executive Summary")
            st.write(rep.get("executive_summary"))
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("#### 2. Key Findings & Trends")
            for f in rep.get("key_findings", []):
                st.write(f"- {f}")
            st.markdown("<br>", unsafe_allow_html=True)
                
            st.markdown("#### 3. Core Recommendations Summary")
            for r in rep.get("recommendations", []):
                st.write(f"- {r}")
            st.markdown("<br>", unsafe_allow_html=True)
                
            st.markdown("#### 4. Audit & Validation Log")
            st.write(rep.get("validation_summary"))
            
            st.markdown("---")
            st.markdown("#### Export Report")
            st.markdown("Download this executive report in PDF format. The PDF layout is built using ReportLab with standard branding elements.")
            
            # Download button fetching file from FastAPI backend
            pdf_url = f"{API_URL}/report/pdf/{res.get('session_id')}"
            
            try:
                pdf_res = requests.get(pdf_url)
                if pdf_res.status_code == 200:
                    st.download_button(
                        label="📥 Download Official BNP Paribas PDF Report",
                        data=pdf_res.content,
                        file_name=f"BNP_Paribas_Churn_Report_{res.get('session_id')}.pdf",
                        mime="application/pdf",
                        width="stretch"
                    )
                else:
                    st.error("Error generating report file. Backend returned failure status.")
            except Exception as e:
                st.error(f"Failed to connect to backend for PDF download: {e}")

# ================= TAB 6: INGEST CUSTOM DATASET =================
with tab_console:
    st.markdown("### 📂 Ingest Custom Dataset")
    st.markdown("Upload a custom customer churn CSV dataset to parse, embed, and load it into ChromaDB.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        if st.button("🚀 Ingest Custom Dataset", width="stretch"):
            with st.spinner("Ingesting & embedding dataset..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                    res = requests.post(f"{API_URL}/ingest-file", files=files)
                    if res.status_code == 200:
                        st.success(res.json().get("message", "Dataset successfully ingested!"))
                        st.rerun()
                    else:
                        detail = res.json().get('detail', 'Unknown error')
                        st.error(f"Ingestion failed: {detail}")
                except Exception as e:
                    st.error(f"Error: {e}")
