
	# OpsEngine: The Compliance-First AI Triage Core
	
	**Architected by Fardan Qureshi | Founder @ EVAAI Labs**
	
	> "Speed is easy. Safety is hard. This engine delivers both."
	
	## The Problem
	FinTech Operations teams are drowning in tickets. 
	- **Generic AI** (Chatbots) cannot be trusted with sensitive flows (KYC/AML) because they hallucinate.
	- **Manual Triage** is slow, expensive, and unscalable.
	
	## The Solution: OpsEngine
	OpsEngine is a deterministic, **Compliance-First AI Architecture** designed specifically for regulated environments. It does not "chat." It follows a strict military protocol:
	
	1.  **Ingest:** Reads the ticket.
	2.  **Retrieve (RAG):** Consults the *exact* Compliance SOP (Standard Operating Procedure).
	3.  **Assess Risk:** Checks for AML/Fraud triggers.
	4.  **Act:** 
	    - **Low Risk:** Drafts a compliant response for human approval.
	    - **High Risk:** Routes to a specialist with a pre-analysis note.
	
	## The Architecture
	- **Language:** Python 3.9+
	- **Core Logic:** Retrieval-Augmented Generation (RAG)
	- **Safety:** Hard-coded Compliance Guardrails (Pre-LLM)
	
	## How to Run the Demo
	1.  Install dependencies:
	    ```bash
	    pip install -r requirements.txt
	    ```
	2.  Run the engine:
	    ```bash
	    python ops_engine.py
	    ```
	
	## License
	Proprietary. All rights reserved.
	