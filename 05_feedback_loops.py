# A Self-Correcting Code Generation System - Feedback Loops

import io, traceback
from contextlib import redirect_stdout, redirect_stderr
from pprint import pprint

from models.c_openai import openai_client, OpenAIModels
from utils.completions import get_completion
from utils.display import c_print


# Set the client and model
client = openai_client()
model = OpenAIModels.GPT_41_NANO

# Print the LLM config
c_print(client)
c_print(f"Current model is {model}")


def execute_code(code, test_cases):
    """
    Executes python code and returns the results of the provided test cases.

    Args:
        code: string containing the python code
        test_cases: list of dictionaries with inputs and expected outputs

    Returns:
        Dictionary containing execution results and test outcomes.
    """
    results = {"execution_error": None, "test_results": [], "passed": 0, "failed": 0}

    # The execution namespace
    namespace = {}

    # Capture stdout and stderr
    output_buffer = io.StringIO()

    try:
        with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
            exec(code, namespace)

        # Run the test cases
        for i, test in enumerate(test_cases):
            inputs = test["inputs"]
            expected = test["expected"]

            # Execute the code with test inputs
            try:
                if isinstance(inputs, dict):
                    actual = namespace["process_data"](**inputs)
                else:
                    actual = namespace["process_data"](*inputs)

                passed = actual == expected

                if passed:
                    results["passed"] += 1
                else:
                    results["failed"] += 1

                results["test_results"].append({
                    "test_id": i + 1,
                    "inputs": inputs,
                    "expected": expected,
                    "actual": actual,
                    "passed": passed
                })
            except Exception as e:
                # If the error is expected, mark as passed
                passed = isinstance(expected, type) and isinstance(e, expected)

                results["test_results"].append({
                    "test_id": i + 1,
                    "inputs": inputs,
                    "expected": expected,
                    "error": str(e),
                    "passed": passed
                })

                if passed:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
    except Exception as e:
        results["execution_error"] = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }

    results["stdout"] = output_buffer.getvalue()
    return results
    

def format_feedback(results):
    """
    Formats test results into a clear feedback string for the model.

    Args:
        results: dictionary containing execution results

    Returns:
        Formatted feedback string
    """
    feedback = []

    if results["execution_error"]:
        feedback.append(f"ERROR: Code execution failed with {results['execution_error']['error_type']}")
        feedback.append(f"Message: {results['execution_error']['error_message']}")
        feedback.append(f"Traceback:\n{results['execution_error']['traceback']}")
        feedback.append("\nPlease fix the syntax or runtime errors in the code.")

        return "\n".join(feedback)
    
    feedback.append(f"Test results: {results['passed']} passed, {results['failed']} failed")

    if results["stdout"]:
        feedback.append(f"\nStandard output:\n{results['stdout']}")

    if results["failed"] > 0:
        feedback.append("\nFailed Test Cases:")
        
        for test in results["test_results"]:
            if not test.get("passed"):
                feedback.append(f"Test #{test['test_id']}")
                feedback.append(f"  Inputs: {test['inputs']}")
                feedback.append(f"  Expected: {test['expected']}")

                if "actual" in test:
                    feedback.append(f"  Actual: {test['actual']}")

                if "error" in test:
                    feedback.append(f"  Error: {test['error']}")

    return "\n".join(feedback)


def extract_code(code: str):
    lines = code.split("\n")
    start = lines.index("```python") + 1
    end = lines.index("```", start)
    return "\n".join(lines[start:end])

    
task_description = """
Your task is to create a python function called `process_data` that accepts a list of numbers 
and a `mode` (for example: 'sum' or 'average'), but defaulting to 'average', and perform the 
corresponding calculation. If the mode is sum, return the sum of all the numbers. If the mode 
is average, then return the average (mean) of all the numbers. Refer to the examples provided.

Examples:
    - `process_data([10, 20, 30], "sum")` # should return `60`
    - `process_data([10, 20, 30], "average")` # should return `20.0`
    - `process_data([7], "average")` # should return `7.0`
"""

initial_prompt = f"""
You a python programming language expert that writes efficient code.

{task_description}

Write only the function surrounded by ```python and ``` without any additional explanations or examples.

Example:
```python
def hello(name):
    print(name)
```
"""


c_print(f"Sending prompts to #{model}")

# EXERCISE 1

# test_cases_1 = [
#     {"inputs": ([1, 2, 3, 4, 5], "sum"), "expected": 15},
#     {"inputs": ([1, 2, 3, 4, 5], "average"), "expected": 3.0},
#     {"inputs": ([0], "average"), "expected": 0.0},
#     {"inputs": ([-1, 2], "sum"), "expected": 1}
# ]

# llm_initial_response = get_completion(client, model, initial_prompt)
# extracted_initial_code = extract_code(llm_initial_response[0])

# c_print(f"👉🏾 Initial Generated Code:\n{extracted_initial_code}\n")

# # Execute and test the code
# executed_code_initial_results = execute_code(extracted_initial_code, test_cases_1)
# initial_formatted_feeback = format_feedback(executed_code_initial_results)

# c_print(f"➡️  {initial_formatted_feeback}\n")


# EXERCISE 2 - FEEDBACK LOOP IMPL.

iterations = []
MAX_ITERATIONS = 3

test_cases_2 = [
    {"inputs": ([1, 2, 3, 4, 5], "sum"), "expected": 15},
    {"inputs": ([1, 2, 3, 4, 5], "average"), "expected": 3.0},
    {"inputs": ([11, 12, 13, 14, 15], "sum"), "expected": 65},
    {"inputs": ([11, 12, 13, 14, 15], "average"), "expected": 13.0},
    {"inputs": ([], "sum"), "expected": None},
    {"inputs": ([1, 3, 4], "median"), "expected": 3},
    {"inputs": ([1, 2, 3, 5], "median"), "expected": 2.5},
    {"inputs": ([1, 2, "a", 3], "sum"), "expected": 6},
    {"inputs": ([1, 2, None, 3, "b", 4], "average"), "expected": 2.5},
    {"inputs": ([10], "median"), "expected": 10},
    {"inputs": ([], "median"), "expected": None},
    {"inputs": ([1, 2, 3, 4, 5], "invalid_mode"), "expected": ValueError},
]

# Initial Execution

llm_initial_response = get_completion(client, model, initial_prompt)
extracted_initial_code = extract_code(llm_initial_response[0])

c_print(f"\n👉🏾 Initial Generated Code:\n{extracted_initial_code}\n")

# Execute and test the code
executed_code_initial_results = execute_code(extracted_initial_code, test_cases_2)
initial_formatted_feeback = format_feedback(executed_code_initial_results)

c_print(f"➡️  {initial_formatted_feeback}\n")

iterations.append({
    "iteration": 0,
    "code": extracted_initial_code,
    "test_results": {
        "passed": executed_code_initial_results["passed"],
        "failed": executed_code_initial_results["failed"]
    }
})

# Feedback Loop Execution

current_code = extracted_initial_code
current_feedback = initial_formatted_feeback

for i in range(MAX_ITERATIONS):
    if iterations[-1]["test_results"]["failed"] == 0:
        print("\nSuccess! All tests passed ✅\n")
        break

    feedback_prompt = f"""
    You are an expert python developer. You wrote a function based on these requirements:
    {task_description}

    Here is your current implementation:
    {current_code}

    I've tested your code and here are the results:
    {current_feedback}

    I want you to improve your code based on the results so that all test cases pass.
    Feel free to add any missing `modes`.
    After that, return only the improved code between ```python ``` with no explanations inside.
    """

    llm_feedback_response = get_completion(client, model, feedback_prompt)
    improved_extracted_code = extract_code(llm_feedback_response[0])

    c_print(f"\n👉🏾 Improved Code (Loop #{i + 1}):\n{improved_extracted_code}\n")

    # Execute and test the code
    executed_code_feedback_results = execute_code(improved_extracted_code, test_cases_2)
    improved_formatted_feeback = format_feedback(executed_code_feedback_results)

    c_print(f"➡️  {improved_formatted_feeback}\n")

    iterations.append({
        "iteration": i + 1,
        "code": improved_extracted_code,
        "test_results": {
            "passed": executed_code_feedback_results["passed"],
            "failed": executed_code_feedback_results["failed"]
        }
    })

    current_code = improved_extracted_code
    current_feedback = improved_formatted_feeback



# pprint(iterations, width=200)