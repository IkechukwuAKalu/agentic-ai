# agentic_workflow.py

from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec
product_spec = Path("./projects/workflows/starter/phase_2/Product-Spec-Email-Router.txt").read_text()

max_evals = 5

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components. \n"
    "A comprehensive development plan is required at the end."
)
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: 'As a'. "
    "For example: As an engineer, I want my code editor to allow global search so that I can find code faster. "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    f"Product Spec:\n{product_spec}"
)
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_product_manager, knowledge_product_manager)

# Product Manager - Evaluation Agent
persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
product_manager_eval_criteria = "Each item in the answer should be user stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value]."
product_manager_evaluation_agent = EvaluationAgent(openai_api_key, persona_product_manager_eval, product_manager_eval_criteria, product_manager_knowledge_agent, max_evals)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_program_manager, knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
program_manager_eval_criteria = (
    "The answer should be product features that follow the following structure: " \
    "Feature Name: A clear, concise title that identifies the capability\n" \
    "Description: A brief explanation of what the feature does and its purpose\n" \
    "Key Functionality: The specific capabilities or actions the feature provides\n" \
    "User Benefit: How this feature creates value for the user"
)
program_manager_evaluation_agent = EvaluationAgent(openai_api_key, persona_program_manager_eval, program_manager_eval_criteria, program_manager_knowledge_agent, max_evals)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_dev_engineer, knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
development_engineer_eval_criteria = (
    "The answer should be tasks following this exact structure: " \
    "Task ID: A unique identifier for tracking purposes\n" \
    "Task Title: Brief description of the specific development work\n" \
    "Related User Story: Reference to the parent user story\n" \
    "Description: Detailed explanation of the technical work required\n" \
    "Acceptance Criteria: Specific requirements that must be met for completion\n" \
    "Estimated Effort: Time or complexity estimation\n" \
    "Dependencies: Any tasks that must be completed first"
)
development_engineer_evaluation_agent = EvaluationAgent(openai_api_key, persona_dev_engineer_eval, development_engineer_eval_criteria, development_engineer_knowledge_agent, max_evals)

# Routing Agent
agents = [
    {
        'name': "Product Manager",
        'description': "Responsible for defining product personas and user stories only. Does not define features or tasks. Does not group stories",
        'func': None
    },
    {
        'name': "Program Manager",
        'description': "Responsible for coordinating and overseeing the execution of multiple projects within a program. Ensures alignment of teams and stakeholders with business goals. Manages timelines, risks, and dependencies, ensuring smooth delivery of initiatives. Does not define product personas or user stories. Does not design or implement features. Does not manage individual tasks.",
        'func': None
    },
    {
        'name': "Development Engineer",
        'description': "Responsible for the technical design, implementation, and testing of product features. Works closely with product managers and designers to understand requirements but does not define product personas or user stories. Focuses on the development of the technical solution and ensures that the features are built according to specifications. Does not define or manage program-level tasks or project timelines.",
        'func': None
    }
]
routing_agent = RoutingAgent(openai_api_key, agents)

# Job function persona support functions
def product_manager_support_function(query):
    worker_response = product_manager_knowledge_agent.respond(query)
    evaluation = product_manager_evaluation_agent.evaluate(query, worker_response)
    return evaluation['final_response']

def program_manager_support_function(query):
    worker_response = program_manager_knowledge_agent.respond(query)
    evaluation = program_manager_evaluation_agent.evaluate(query, worker_response)
    return evaluation['final_response']

def development_engineer_support_function(query):
    worker_response = development_engineer_knowledge_agent.respond(query)
    evaluation = development_engineer_evaluation_agent.evaluate(query, worker_response)
    return evaluation['final_response']

agents[0]['func'] = product_manager_support_function
agents[1]['func'] = program_manager_support_function
agents[2]['func'] = development_engineer_support_function

# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = "What would the development tasks for this product be?"
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\n=== Defining workflow steps from the workflow prompt ===")

extracted_action_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)

print("\n".join(extracted_action_steps))
print("\n")

result = ""
completed_steps = []

for i, step in enumerate(extracted_action_steps):
    print(f"=== [Workflow] Step {i + 1} ===")
    print(f"[Input] {step}")

    try:
        result = routing_agent.route(step)
        completed_steps.append(result)
    except Exception as e:
        print(f"[Error] Failed to get a response from the agent: {e}")

    print(f"[Output] {result}\n\n")

print(f"=== [Workflow] Final Output ===")
print(result)
