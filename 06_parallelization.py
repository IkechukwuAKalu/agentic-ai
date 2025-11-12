# Agentic workflows - Parallelization

import threading

from models.c_openai import openai_client, OpenAIModels
from utils.completions import get_completion
from utils.display import c_print


# Set the client and model
model = OpenAIModels.GPT_41_NANO

# Print the LLM config
# c_print(client)
c_print(f"Current model is {model}")


# Shared dict for thread-safe collection of agent outputs
agent_outputs = {}

# Example contract text (in a real application, this would be loaded from a file)
contract_text = """
CONSULTING AGREEMENT

This Consulting Agreement (the "Agreement") is made effective as of January 1, 2025 (the "Effective Date"), by and between ABC Corporation, a Delaware corporation ("Client"), and XYZ Consulting LLC, a California limited liability company ("Consultant").

1. SERVICES. Consultant shall provide Client with the following services: strategic business consulting, market analysis, and technology implementation advice (the "Services").

2. TERM. This Agreement shall commence on the Effective Date and shall continue for a period of 12 months, unless earlier terminated.

3. COMPENSATION. Client shall pay Consultant a fee of $10,000 per month for Services rendered. Payment shall be made within 30 days of receipt of Consultant's invoice.

4. CONFIDENTIALITY. Consultant acknowledges that during the engagement, Consultant may have access to confidential information. Consultant agrees to maintain the confidentiality of all such information.

5. INTELLECTUAL PROPERTY. All materials developed by Consultant shall be the property of Client. Consultant assigns all right, title, and interest in such materials to Client.

6. TERMINATION. Either party may terminate this Agreement with 30 days' written notice. Client shall pay Consultant for Services performed through the termination date.

7. GOVERNING LAW. This Agreement shall be governed by the laws of the State of Delaware.

8. LIMITATION OF LIABILITY. Consultant's liability shall be limited to the amount of fees paid by Client under this Agreement.

9. INDEMNIFICATION. Client shall indemnify Consultant against all claims arising from use of materials provided by Client.

10. ENTIRE AGREEMENT. This Agreement constitutes the entire understanding between the parties and supersedes all prior agreements.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.
"""

class LegalTermsChecker:
    """Agent that checks for problematic legal terms and clauses in contracts."""
    def __init__(self):
        self.client = openai_client()

    def run(self, contract_text):
        c_print("Legal Terms Checker analyzing contract...")
        system_prompt = "You are a legal expert specializing in contract law. Analyze the contract for potentially problematic legal terms, clauses, or language that could create legal issues or disputes. Focus on liability, rights, obligations, and ambiguous language."
        user_prompt = f"Analyze this contract for problematic legal terms and clauses:\n\n{contract_text}"
        response, _ = get_completion(self.client, model, user_prompt, [], system_prompt)
        agent_outputs["legal"] = response
        c_print("Legal Terms Checker completed analysis.")

class ComplianceValidator:
    """Agent that validates regulatory and industry compliance of contracts."""
    def __init__(self):
        self.client = openai_client()

    def run(self, contract_text):
        c_print("Compliance Validator analyzing contract...")
        system_prompt = "You are a compliance expert specializing in regulatory requirements across industries. Analyze the contract for potential compliance issues related to data privacy, labor laws, industry-specific regulations, and standard business practices."
        user_prompt = f"Analyze this contract for regulatory and industry compliance issues:\n\n{contract_text}"
        response, _ = get_completion(self.client, model, user_prompt, [], system_prompt)
        agent_outputs["compliance"] = response
        c_print("Compliance Validator completed analysis.")

class FinancialRiskAssessor:
    """Agent that assesses financial risks and liabilities in contracts."""
    def __init__(self):
        self.client = openai_client()

    def run(self, contract_text):
        c_print("Financial Risk Assessor analyzing contract...")
        system_prompt = "You are a financial analyst specializing in contract risk assessment. Analyze the contract for financial risks, liability exposure, payment terms issues, and potential financial implications that could negatively impact a business."
        user_prompt = f"Analyze this contract for financial risks and liabilities:\n\n{contract_text}"
        response, _ = get_completion(self.client, model, user_prompt, [], system_prompt)
        agent_outputs["financial"] = response
        c_print("Financial Risk Assessor completed analysis.")

class SummaryAgent:
    """Agent that synthesizes findings from all specialized agents."""
    def __init__(self):
        self.client = openai_client()

    def run(self, contract_text, inputs):
        c_print("Summary Agent synthesizing findings...")
        system_prompt = "You are a senior contract analyst skilled at synthesizing expert insights into clear, actionable business recommendations."

        combined_prompt = (
            f"Contract:\n{contract_text}\n\n"
            f"Here are the expert analyses:\n\n"
            f"LEGAL ANALYSIS:\n{inputs['legal']}\n\n"
            f"COMPLIANCE ANALYSIS:\n{inputs['compliance']}\n\n"
            f"FINANCIAL ANALYSIS:\n{inputs['financial']}\n\n"
            "Please synthesize these analyses into a comprehensive contract assessment report with the following sections:\n"
            "1. Executive Summary\n"
            "2. Key Legal Concerns\n"
            "3. Compliance Issues\n"
            "4. Financial Risks\n"
            "5. Recommended Actions\n\n"
            "The report should be concise, actionable, and highlight the most critical findings."
        )

        response, _ = get_completion(self.client, model, combined_prompt, [], system_prompt)
        return response

# Main function to run all agents in parallel
def analyze_contract(contract_text):
    """Run all agents in parallel and summarize their findings."""
    # Create agent instances
    legal_agent = LegalTermsChecker()
    compliance_agent = ComplianceValidator()
    financial_agent = FinancialRiskAssessor()
    summary_agent = SummaryAgent()
    
    # Run agents in parallel
    threads = [
        threading.Thread(target=legal_agent.run, args=(contract_text,)),
        threading.Thread(target=compliance_agent.run, args=(contract_text,)),
        threading.Thread(target=financial_agent.run, args=(contract_text,))
    ]
    
    # Start all threads
    for t in threads:
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # Generate summary from all agent outputs
    final_analysis = summary_agent.run(contract_text, agent_outputs)
    
    return final_analysis

if __name__ == "__main__":
    c_print("Enterprise Contract Analysis System")
    c_print("Analyzing contract...")
    
    final_analysis = analyze_contract(contract_text)
    c_print("\n=== FINAL CONTRACT ANALYSIS ===\n")
    c_print(final_analysis)