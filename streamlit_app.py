
	import streamlit as st
	import time
	import random
	from dataclasses import dataclass
	from typing import List, Optional
	
	# --- CONFIGURATION ---
	st.set_page_config(page_title="OpsEngine | Compliance Core", page_icon="🛡️", layout="wide")
	
	# --- STYLES ---
	st.markdown("""
	    <style>
	    .stApp {
	        background-color: #0E1117;
	        color: #FAFAFA;
	    }
	    .metric-card {
	        background-color: #262730;
	        padding: 20px;
	        border-radius: 10px;
	        border: 1px solid #4B4B4B;
	        text-align: center;
	    }
	    .high-risk {
	        color: #FF4B4B;
	        font-weight: bold;
	    }
	    .low-risk {
	        color: #00CC96;
	        font-weight: bold;
	    }
	    </style>
	""", unsafe_allow_html=True)
	
	# --- DATA STRUCTURES ---
	
	@dataclass
	class SOP:
	    id: str
	    title: str
	    keywords: List[str]
	    policy_text: str
	
	# --- KNOWLEDGE BASE ---
	SOPS = [
	    SOP("SOP-001", "KYC - Address Verification", ["address", "proof", "utility bill", "verify", "rejected"], 
	        "If address doc is rejected: 1. Check date (<3 months). 2. Check name match. 3. No screenshots."),
	    SOP("SOP-002", "AML - Transaction Hold", ["hold", "frozen", "large transfer", "audit", "source of funds"], 
	        "CRITICAL: Do not disclose specific reasons. Request Source of Funds (SOF)."),
	    SOP("SOP-003", "General - Transfer Delay", ["where is my money", "late", "delay", "transfer", "waiting"], 
	        "Standard time: 1-2 business days. If > 2 days, check banking partner.")
	]
	
	# --- ENGINE LOGIC ---
	
	def retrieve_sop(content):
	    best_sop = None
	    max_score = 0
	    for sop in SOPS:
	        score = sum(1 for word in sop.keywords if word in content.lower())
	        if score > max_score:
	            max_score = score
	            best_sop = sop
	    return best_sop
	
	def assess_risk(content, sop):
	    triggers = ["fraud", "scam", "police", "lawyer", "sue", "frozen", "aml"]
	    for t in triggers:
	        if t in content.lower(): return "HIGH"
	    if sop and "AML" in sop.title: return "HIGH"
	    return "LOW"
	
	def generate_draft(ticket_content, sop):
	    if not sop: return "No matching SOP found. Manual review required."
	    
	    if "KYC" in sop.title:
	        return "Dear Customer,\n\nThank you for contacting us. I see your address document was rejected. Please ensure it is a PDF dated within the last 3 months.\n\nBest,\nSupport"
	    elif "AML" in sop.title:
	        return "[INTERNAL NOTE]: High Risk AML. Do not reply. Route to Compliance Team."
	    else:
	        return "Dear Customer,\n\nYour transfer is currently within the standard 1-2 day processing window. It should arrive by tomorrow.\n\nBest,\nSupport"
	
	# --- UI LAYOUT ---
	
	# Sidebar
	with st.sidebar:
	    st.image("https://img.icons8.com/fluency/96/shield.png", width=50)
	    st.title("OpsEngine")
	    st.caption("Compliance-First AI Triage")
	    st.divider()
	    st.subheader("Active SOPs")
	    for sop in SOPS:
	        with st.expander(f"📄 {sop.title}"):
	            st.write(sop.policy_text)
	            st.caption(f"Keywords: {', '.join(sop.keywords)}")
	    st.divider()
	    st.info("System Status: ● ONLINE")
	
	# Main Area
	st.title("🛡️ Triage Command Center")
	
	# Metrics Row
	col1, col2, col3, col4 = st.columns(4)
	col1.metric("Active Tickets", "142", "+12")
	col2.metric("Avg Handling Time", "1.2m", "-45%")
	col3.metric("Automation Rate", "34%", "+5%")
	col4.metric("Compliance Flags", "3", "Alert")
	
	st.divider()
	
	# Input Area
	st.subheader("Live Ticket Simulation")
	ticket_input = st.text_area("Paste Incoming Ticket Content:", height=100, placeholder="e.g., My account is frozen! I will sue you!")
	
	if st.button("Analyze Ticket", type="primary"):
	    if not ticket_input:
	        st.warning("Please enter ticket content.")
	    else:
	        with st.spinner("OpsEngine is thinking..."):
	            time.sleep(1) # Simulate processing
	            
	            # Logic
	            sop = retrieve_sop(ticket_input)
	            risk = assess_risk(ticket_input, sop)
	            draft = generate_draft(ticket_input, sop)
	            
	            # Results Layout
	            r_col1, r_col2 = st.columns([1, 2])
	            
	            with r_col1:
	                st.markdown("### Analysis")
	                
	                # Risk Badge
	                if risk == "HIGH":
	                    st.error("⚠️ HIGH RISK DETECTED")
	                else:
	                    st.success("✅ LOW RISK")
	                
	                st.markdown(f"**Intent:** `{sop.title if sop else 'Unknown'}`")
	                
	                if risk == "HIGH":
	                    st.markdown("**Action:** 🔴 ROUTE TO AML")
	                elif sop:
	                    st.markdown("**Action:** 🟢 DRAFT REPLY")
	                else:
	                    st.markdown("**Action:** 🟡 MANUAL REVIEW")
	
	            with r_col2:
	                st.markdown("### Generated Draft / Internal Note")
	                st.code(draft, language="text")
	                
	                if risk == "LOW" and sop:
	                    st.button("Approve & Send", type="secondary")
	                    st.button("Edit Draft", type="secondary")
	
	