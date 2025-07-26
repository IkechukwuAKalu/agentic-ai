import json
import pandas as pd

from models.c_openai import openai_client, OpenAIModels
from models.ollama import ollama_client, OllamaModels
from mock_data.competitor_pricing import get_competitor_pricing_data
from mock_data.promotions import call_promotions_api
from mock_data.sales import get_sales_data
from mock_data.weather import get_weather_data
from utils.completions import get_completion
from utils.display import c_print, configure_panda, plot_competitor_pricing_data, plot_sales_data, plot_weather_data


# Set the client and model
client = openai_client()
model = OpenAIModels.GPT_41_NANO

# client = ollama_client()
# model = OllamaModels.LLAMA_32

# Print the LLM config
c_print(client)
c_print(f"Current model is {model}")

# Set panda display options
configure_panda(pd)

# Fetch data from the APIs
competitor_pricing_data = get_competitor_pricing_data()
competitor_pricing_df = pd.DataFrame(competitor_pricing_data)

promotions_data = call_promotions_api()
promotions_df = pd.DataFrame(promotions_data)

sales_data = get_sales_data()
sales_df = pd.DataFrame(sales_data)

weather_data = get_weather_data()
weather_df = pd.DataFrame(weather_data)

sales_df = sales_df.sort_values(by = ["product_id", "date"]).reset_index(drop = True)

# Plot graphs
def plot_graphs():
    plot_competitor_pricing_data(competitor_pricing_df)
    plot_sales_data(sales_df)
    plot_weather_data(weather_df)

# plot_graphs()


system_prompt_no_explicit_cot = """
You are a meticulous Retail Demand Analyst.
Your task is to analyze the provided sales data and promotion schedules to identify and explain the significant sales spikes for specific SKUs.
"""

system_prompt_explicit_cot = """
You are a meticulous Retail Demand Analyst.
Your task is to analyze the provided sales data and promotion schedules to identify and explain the significant sales spikes for specific SKUs.

You are to think step-by-step to analyze the data, provide a hypothesis for the cause, and provide a logical conclusion and recommendation.
"""

user_prompt_basic = f"""
Analyze the data provided below and for provide a hypothesis for the causes of any observed sales spike.

Sales Data: {sales_data}

Weather Data: {weather_data}

Competitor Pricing Data: {competitor_pricing_data}
"""

user_prompt_advanced = f"""
## INSTRUCTIONS:

Analyze the data provided below and for provide a hypothesis for the causes of any observed sales spike.

Do the following:
- Find all sales spike for each product
- For each spike, identify the date, the sales increase, and the possible causes by looking at all the different data sources
- Start your response with the structured analysis and conclude by identifying the single largest spike in the exact JSON format given below

--

## OUTPUT FORMAT

STRUCTURED ANALYSIS:
[Structured Analysis]

LARGEST SPIKE:
```json
{{
    "date": "YYYY-MM-DD",
    "amount_before_increase": "X.XX",
    "amount_after_increase": "X.XX",
    "percentage_increase": "X.XX%",
    "causes": [
        "Cause 1",
        "Cause 2",
        "Cause 3"
    ]
}}
```

--

## CONTEXT

Sales Data: {sales_data}

Weather Data: {weather_data}

Competitor Pricing Data: {competitor_pricing_data}

Promotions Schedule: #{promotions_data}
"""

def parse_analysis_and_largest_spike(response: str):
    if "```json" not in response:
        raise RuntimeError("No ```json found in the response")
    
    # Get all parts before the JSON
    analysis = response.split("```json")[0].strip()
    # Get only the JSON data, excluding the ```json & ``` tags
    json_str = response.split("```json")[1].split("```")[0].strip()
    return analysis, json.loads(json_str)


c_print(f"Sending prompts to #{model}")

# EXERCISE 1

# no_explicit_cot_response = get_completion(client, model, user_prompt_basic, [], system_prompt_no_explicit_cot)
# c_print(no_explicit_cot_response[0])

# EXERCISE 2

# explicit_basic_cot_response = get_completion(client, model, user_prompt_basic, [], system_prompt_explicit_cot)
# c_print(explicit_basic_cot_response[0])

# EXERCISE 3

explicit_advanced_cot_response, message_history = get_completion(client, model, user_prompt_advanced, [], system_prompt_explicit_cot)
c_print(explicit_advanced_cot_response)

final_analysis, largest_spike = parse_analysis_and_largest_spike(explicit_advanced_cot_response)
c_print(final_analysis)
c_print(largest_spike)

followup_response = get_completion(client, model, "In one sentence, What do you think?", message_history)
c_print(followup_response[0])
