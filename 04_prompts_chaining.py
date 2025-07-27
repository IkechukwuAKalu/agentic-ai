import json
import pandas as pd

from mock_data.fnols import get_fnols
from models.c_openai import openai_client, OpenAIModels
from pydantic_models.insurance import ClaimInformation, ClaimRouting, SeverityAssessment
from utils.completions import get_completion
from utils.display import c_print


# Set the client and model
client = openai_client()
model = OpenAIModels.GPT_41_NANO

# Print the LLM config
c_print(client)
c_print(f"Current model is {model}")


def gate1_validate_claim_info(claim_info_json: str) -> ClaimInformation:
    try:
        claim_info_dict = json.loads(claim_info_json)
        return ClaimInformation(**claim_info_dict)
    except Exception as e:
        raise ValueError(f"Gate 1 validation check failed: {e}")


def extract_claim_info(system_prompt, fnol_text) -> ClaimInformation | None:
    llm_response = get_completion(client, model, fnol_text, [], system_prompt)
    
    try:
        return gate1_validate_claim_info(llm_response[0])
    except Exception as e:
        print(f"Gate 1 check failed: {e}")
        return None
    

def gate2_validate_cost_range(severity_json: str) -> SeverityAssessment:
    try:
        severity_dict = json.loads(severity_json)
        validated_severity = SeverityAssessment(**severity_dict)

        if (
            validated_severity.severity == "Minor"
            and (validated_severity.est_cost < 100 or validated_severity.est_cost > 1_000)
        ):
            raise ValueError(f"Minor damage should cost between $100-$1000, got ${validated_severity.est_cost}")
        elif (
            validated_severity.severity == "Moderate"
            and (validated_severity.est_cost < 1_000 or validated_severity.est_cost > 5_000)
        ):
            raise ValueError(f"Moderate damage should cost between $1000-$5000, got ${validated_severity.est_cost}")
        elif (
            validated_severity.severity == "Major"
            and (validated_severity.est_cost < 5_000 or validated_severity.est_cost > 50_000)
        ):
            raise ValueError(f"Major damage should cost between $5000-$50000, got ${validated_severity.est_cost}")
        
        return validated_severity
    except Exception as e:
        raise ValueError(f"Gate 2 validation check failed: {e}")


def assess_severity(claim_info: ClaimInformation, system_prompt: str) -> SeverityAssessment | None:
    claim_info_json = claim_info.model_dump_json()

    llm_response = get_completion(client, model, claim_info_json, [], system_prompt)
    
    try:
        return gate2_validate_cost_range(llm_response[0])
    except Exception as e:
        print(f"Gate 2 check failed: {e}")
        return None
    

def gate3_validate_routing(routing_json: str) -> ClaimRouting:
    try:
        routing_dict = json.loads(routing_json)
        return ClaimRouting(**routing_dict)
    except Exception as e:
        raise ValueError(f"Gate 3 validation check failed: {e}")
    

def route_claim(claim_info: ClaimInformation, severity_assessment: SeverityAssessment | None, system_prompt) -> ClaimRouting | None:
    if severity_assessment is None:
        return None
    
    routing_input_dict = {
        "claim_information": claim_info.model_dump(),
        "severity_assessment": severity_assessment.model_dump()
    }

    routing_input_json = json.dumps(routing_input_dict)

    llm_response = get_completion(client, model, routing_input_json, [], system_prompt)
    
    try:
        return gate3_validate_routing(llm_response[0])
    except Exception as e:
        print(f"Gate 3 check failed: {e}")
        return None
    

def visualize_data(claim_items, severity_assessment_items, routed_claim_items) -> pd.DataFrame:
    records = []

    for claim, severity_assessment, routed_claim in zip(
        claim_items, severity_assessment_items, routed_claim_items
    ):
        record = {}
        record.update(claim)
        record.update(severity_assessment)
        record.update(routed_claim)
        records.append(record)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_colwidth", None)

    return pd.DataFrame(records)


info_extraction_system_prompt = """
You are a helpful assistant working in an insurance company.

Your task is to extract key information from First Notice of Loss (FNOL) reports.

Format your response as a valid JSON object with the following keys:
- claim_id (str): The claim ID
- name (str): The customer's name
- vehicle (str): The vehicle model
- loss_desc (str): A description about the incident
- damage_area (list[str]): A list of the damage areas from the following: "windshield", "front", "rear", "side", "roof", "hood", "door", "bumper", "fender", "quarter panel", "trunk", "glass"

Any damage area not listed here will NOT be accepted.

Only respond with the JSON object, nothing else.
"""

severity_assessment_system_prompt = """
You are an expert auto insurance damage assessor.

Your task is to evaluate the severity of vehicle damage and estimate the repair costs.

Format your response as a valid JSON object with the following keys:
- severity (str): The damage severity level and it must be ONLY one of the following: "Minor", "Moderate", "Major"
- est_cost (float): The estimated repair costs

Any severity level not listed here will NOT be accepted.

Only respond with the JSON object, nothing else.
"""

queue_routing_system_prompt = """
You are an auto insurance claim routing specialist.

Your task is to determine the appropriate queue for each claim.

Format your response as a valid JSON object with the following keys:
- claim_id (str): The claim ID
- queue (str): The processing queue and it must be ONLY one of the following: "glass", "fast_track", "material_damage", "total_loss"

Use the following routing rules:
- 'glass' queue: For Minor damages involving ONLY glass (windshield, windows)
- 'fast_track' queue: For other Minor damages
- 'material_damage' queue: For all Moderate damages
- 'total_loss' queue: For all Major damages

Any queue not listed here will NOT be accepted.

Only respond with the JSON object, nothing else.
"""


# EXERCISE 1

c_print(f"Sending prompts to #{model}")

extracted_claim_info_items = [
    extract_claim_info(info_extraction_system_prompt, fnol_text) for fnol_text in get_fnols()
]

c_print(extracted_claim_info_items)

severity_assessment_items = [
    assess_severity(item, severity_assessment_system_prompt) for item in extracted_claim_info_items
]

c_print(severity_assessment_items)

routed_claim_items = [
    route_claim(claim_info, severity_assessment, queue_routing_system_prompt)
    for (claim_info, severity_assessment) in zip(extracted_claim_info_items, severity_assessment_items)
]

c_print(routed_claim_items)

c_print(visualize_data(extracted_claim_info_items, severity_assessment_items, routed_claim_items))