
	import time
	import random
	from dataclasses import dataclass
	from typing import List, Dict, Optional
	from rich.console import Console
	from rich.table import Table
	from rich.panel import Panel
	from rich.text import Text
	from rich.progress import Progress, SpinnerColumn, TextColumn
	
	# --- CONFIGURATION ---
	COMPANY_NAME = "FinTech Corp"
	console = Console()
	
	# --- DATA STRUCTURES ---
	
	@dataclass
	class Ticket:
	    id: str
	    customer_id: str
	    content: str
	    status: str = "NEW"
	
	@dataclass
	class SOP:
	    id: str
	    title: str
	    keywords: List[str]
	    policy_text: str
	
	@dataclass
	class TriageResult:
	    ticket_id: str
	    intent: str
	    risk_level: str  # LOW, MEDIUM, HIGH
	    suggested_action: str
	    draft_response: Optional[str]
	    relevant_sop: str
	
	# --- THE KNOWLEDGE BASE (The "Wise" Brain) ---
	
	SOPS = [
	    SOP(
	        id="SOP-001",
	        title="KYC - Address Verification Failure",
	        keywords=["address", "proof", "utility bill", "verify", "rejected"],
	        policy_text="If address doc is rejected: 1. Check if doc is < 3 months old. 2. Check if name matches. 3. If blurry, request re-upload. 4. Do NOT accept screenshots."
	    ),
	    SOP(
	        id="SOP-002",
	        title="AML - Large Transaction Hold",
	        keywords=["hold", "frozen", "large transfer", "audit", "source of funds"],
	        policy_text="CRITICAL: Do not give specific reasons for AML holds. State: 'Your transfer is under standard review.' Request: Source of Funds (SOF) documents (Payslip, Sale of Property deed)."
	    ),
	    SOP(
	        id="SOP-003",
	        title="General - Transfer Delay",
	        keywords=["where is my money", "late", "delay", "transfer", "waiting"],
	        policy_text="Standard processing time is 1-2 business days. If within timeframe, reassure customer. If > 2 days, check banking partner status."
	    )
	]
	
	# --- THE OPS ENGINE (The Architecture) ---
	
	class OpsEngine:
	    def __init__(self):
	        self.sops = SOPS
	        console.print(Panel.fit(f"[bold cyan]{COMPANY_NAME} OpsEngine Initialized[/bold cyan]", border_style="cyan"))
	        console.print(f"[green]✓[/green] Loaded {len(self.sops)} Compliance SOPs into Vector Memory.")
	        console.print("-" * 60)
	
	    def _retrieve_sop(self, content: str) -> Optional[SOP]:
	        best_sop = None
	        max_score = 0
	        for sop in self.sops:
	            score = sum(1 for word in sop.keywords if word in content.lower())
	            if score > max_score:
	                max_score = score
	                best_sop = sop
	        return best_sop
	
	    def _assess_risk(self, content: str, sop: Optional[SOP]) -> str:
	        high_risk_triggers = ["fraud", "scam", "police", "lawyer", "sue", "frozen", "aml"]
	        for trigger in high_risk_triggers:
	            if trigger in content.lower():
	                return "HIGH"
	        if sop and "AML" in sop.title:
	            return "HIGH"
	        return "LOW"
	
	    def _generate_draft(self, ticket: Ticket, sop: SOP) -> str:
	        if "KYC" in sop.title:
	            return f"Dear Customer,\n\nThank you for contacting {COMPANY_NAME}. I see your address document was rejected. Per our policy, please ensure the document is a utility bill or bank statement dated within the last 3 months. Screenshots are not accepted. Please re-upload a PDF version here: [Link].\n\nBest,\nSupport Team"
	        elif "AML" in sop.title:
	            return f"[INTERNAL NOTE]: This is a High Risk AML interaction. Do not disclose specific triggers. Request Source of Funds documents immediately."
	        else:
	            return f"Dear Customer,\n\nI understand you are waiting for your transfer. Standard processing time is 1-2 business days. Your transfer is currently within this window and should arrive by tomorrow. Thank you for your patience.\n\nBest,\nSupport Team"
	
	    def process_ticket(self, ticket: Ticket) -> TriageResult:
	        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
	            progress.add_task(description=f"Analyzing Ticket {ticket.id}...", total=None)
	            time.sleep(0.8) # Simulate processing
	            
	            sop = self._retrieve_sop(ticket.content)
	            sop_title = sop.title if sop else "NO MATCH FOUND"
	            risk = self._assess_risk(ticket.content, sop)
	            
	            if risk == "HIGH":
	                action = "ROUTE TO SPECIALIST (AML TEAM)"
	                draft = self._generate_draft(ticket, sop) if sop else "Manual Review Required"
	            elif sop:
	                action = "DRAFT REPLY (HUMAN REVIEW)"
	                draft = self._generate_draft(ticket, sop)
	            else:
	                action = "MANUAL TRIAGE"
	                draft = None
	
	            return TriageResult(ticket.id, sop_title, risk, action, draft, sop_title)
	
	# --- THE DEMO ---
	
	def run_demo():
	    engine = OpsEngine()
	    tickets = [
	        Ticket("TKT-101", "CUST-A", "Why was my utility bill rejected? It shows my name clearly."),
	        Ticket("TKT-102", "CUST-B", "Where is my money? I sent it 4 hours ago."),
	        Ticket("TKT-103", "CUST-C", "My account is frozen! This istheft! I will call my lawyer if you don't release my funds.")
	    ]
	
	    for ticket in tickets:
	        console.print(f"\n[bold white]>>> INCOMING TICKET: {ticket.id}[/bold white]")
	        console.print(f"[italic]{ticket.content}[/italic]")
	        
	        result = engine.process_ticket(ticket)
	        
	        # Visual Output
	        table = Table(title=f"OpsEngine Analysis: {ticket.id}", show_header=True, header_style="bold magenta")
	        table.add_column("Metric", style="cyan")
	        table.add_column("Value", style="white")
	        
	        table.add_row("Detected Intent", result.intent)
	        
	        risk_style = "green" if result.risk_level == "LOW" else "red"
	        table.add_row("Risk Level", f"[{risk_style}]{result.risk_level}[/{risk_style}]")
	        
	        table.add_row("Relevant SOP", result.relevant_sop)
	        table.add_row("Action", f"[bold]{result.suggested_action}[/bold]")
	        
	        console.print(table)
	        
	        if result.draft_response:
	            console.print(Panel(result.draft_response, title="Generated Draft", border_style="green"))
	        
	        time.sleep(1)
	
	if __name__ == "__main__":
	    run_demo()
	