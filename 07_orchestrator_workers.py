# Agentic workflows - Orchestrator-Workers

from typing import List, Dict, Optional
from models.c_openai import openai_client, OpenAIModels
from utils.completions import get_completion
from utils.display import c_print
from utils.xml_helper import extract_xml


# Set the client and model
model = OpenAIModels.GPT_41_NANO
client = openai_client()

# Print the LLM config
# c_print(client)
c_print(f"Current model is {model}")
c_print(client)


# === Helper functions ===

def parse_tasks(xml: str) -> List[Dict]:
    """Parses <task> XML blocks into dictionaries."""
    tasks = []
    current_task = {}

    for line in xml.splitlines():
        line = line.strip()
        if line.startswith("<task>"):
            current_task = {}
        elif line.startswith("<type>"):
            current_task["type"] = line[6:-7].strip()
        elif line.startswith("<description>"):
            current_task["description"] = line[12:-13].strip()
        elif line.startswith("</task>"):
            if "description" in current_task:
                if "type" not in current_task:
                    current_task["type"] = "default"
                tasks.append(current_task)
    return tasks


# === Worker Agents ===

class WorkerAgent:
    """Abstract base class for all specialized worker agents."""
    def __init__(self, task_type: str):
        self.task_type = task_type

    def run(self, original_task: str, task_description: str) -> str:
        raise NotImplementedError("The 'run' method must be implemented in a subclass.")
    

class HematologyAgent(WorkerAgent):
    """Worker Agent that analyzes blood cell counts (Complete Blood Count)."""
    def run(self, original_task: str, task_description: str) -> str:
        prompt = f"""
You are a hematology analysis expert. Your task is to interpret the blood count section of a lab report.

Main Task: {original_task}
Your Subtask: {task_description}

<response>
- Explain the purpose of analyzing these blood values.
- Identify any out-of-range values (e.g., high/low RBC, WBC, Platelets).
- Briefly note the potential clinical significance of any abnormalities.
</response>
"""
        response, _ = get_completion(client, model, prompt)
        return extract_xml(response, "response")


class RenalFunctionAgent(WorkerAgent):
    """Worker Agent that analyzes kidney function markers."""
    def run(self, original_task: str, task_description: str) -> str:
        prompt = f"""
You are a renal function analysis expert. Your task is to interpret the kidney-related markers from a lab report.

Main Task: {original_task}
Your Subtask: {task_description}

<response>
- Explain the purpose of analyzing these kidney markers.
- Identify any out-of-range values (e.g., Creatinine, BUN, GFR).
- Briefly note the potential clinical significance of any abnormalities.
</response>
"""
        response, _ = get_completion(client, model, prompt)
        return extract_xml(response, "response")


class LiverFunctionAgent(WorkerAgent):
    """Worker Agent that analyzes liver enzyme markers."""
    def run(self, original_task: str, task_description: str) -> str:
        prompt = f"""
You are a liver function analysis expert. Your task is to interpret the liver enzyme section of a lab report.

Main Task: {original_task}
Your Subtask: {task_description}

<response>
- Explain the purpose of analyzing these liver enzymes.
- Identify any out-of-range values (e.g., ALT, AST, ALP).
- Briefly note the potential clinical significance of any abnormalities.
</response>
"""
        response, _ = get_completion(client, model, prompt)
        return extract_xml(response, "response")
    

# === Orchestrator Agent ===

class Orchestrator:
    def __init__(self, orchestrator_prompt: str):
        self.orchestrator_prompt = orchestrator_prompt

    def get_worker(self, task_type: str) -> WorkerAgent:
        """Inspects the task type and returns the correct specialized agent."""
        task_type_lower = task_type.lower()
        
        if task_type_lower == "hematology":
            return HematologyAgent(task_type_lower)
        elif task_type_lower == "renal":
            return RenalFunctionAgent(task_type_lower)
        elif task_type_lower == "liver":
            return LiverFunctionAgent(task_type_lower)
        
        raise ValueError(f"No worker agent configured for task type: {task_type}")

    def process(self, task: str) -> Dict:
        """Runs the full Orchestrator-Workers workflow."""
        orchestrator_input = self.orchestrator_prompt.format(task=task)
        response, _ = get_completion(client, model, orchestrator_input)
        c_print("\n[Raw Orchestrator Output]\n", response)

        analysis = extract_xml(response, "analysis")
        tasks_xml = extract_xml(response, "tasks")
        tasks = parse_tasks(tasks_xml)

        c_print("\n=== ORCHESTRATOR ANALYSIS & PLAN ===")
        c_print("Analysis:", analysis)
        c_print("Parsed Tasks:", tasks)

        results = []
        for task_info in tasks:
            try:
                agent = self.get_worker(task_info["type"])
                result = agent.run(task, task_info["description"])
                c_print(f"\n=== {task_info['type'].upper()} RESULT ===\n{result}")
                results.append({
                    "type": task_info["type"],
                    "description": task_info["description"],
                    "result": result
                })
            except ValueError as e:
                c_print(f"\n--- ERROR --- \n{e}")

        return {"analysis": analysis, "worker_results": results}


# === Prompt Template for Orchestrator ===

orchestrator_prompt = """
You are a clinical lab data analyst. Your job is to analyze a set of patient lab results and create a plan to interpret them systematically.

The plan must be broken down into subtasks, one for each major panel in the lab report.

Return your response in the following format, with an <analysis> section and a <tasks> section.

<analysis>
Provide a high-level summary of the lab panels present and the overall goal of the interpretation.
</analysis>

<tasks>
Provide one <task> entry for each major lab panel found in the data. Each task must have a <type> and a <description>.
Example task format:
<task>
  <type>hematology</type>
  <description>Analyze the Complete Blood Count (CBC) panel, including RBC, WBC, and platelets.</description>
</task>
</tasks>

Here is the high-level task and data:
Task: {task}
"""

# === Main Runner ===

if __name__ == "__main__":
    lab_results_data = """
    Patient Lab Report:
    - Panel: Complete Blood Count (CBC)
      - White Blood Cell (WBC): 11.5 x10^9/L (Normal: 4.5-11.0)
      - Red Blood Cell (RBC): 4.6 x10^12/L (Normal: 4.2-5.4)
      - Platelets: 140 x10^9/L (Normal: 150-450)
    - Panel: Renal Function Panel
      - Creatinine: 1.4 mg/dL (Normal: 0.6-1.2)
      - BUN: 25 mg/dL (Normal: 7-20)
    - Panel: Liver Function Panel
      - ALT: 55 U/L (Normal: 7-56)
      - AST: 60 U/L (Normal: 10-40)
    """
    
    user_prompt = f"Please interpret the following lab results and provide a summary: {lab_results_data}"

    orchestrator = Orchestrator(orchestrator_prompt)
    final_report = orchestrator.process(user_prompt)

    print("\n\n=== FINAL INTERPRETATION REPORT ===")
    print("Overall Analysis:\n", final_report.get("analysis", "N/A"))
    for r in final_report.get("worker_results", []):
        print(f"\n--- {r['type'].upper()} PANEL ---")
        print("Task Description:", r["description"])
        print("Interpretation:\n", r["result"])
