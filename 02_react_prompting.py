from ast import literal_eval
import pandas as pd
import re

from models.c_openai import openai_client, OpenAIModels
from mock_data.competitor_pricing import get_competitor_pricing_data
from mock_data.promotions import call_promotions_api
from mock_data.sales import call_sales_api, get_sales_data
from mock_data.weather import call_weather_api, get_weather_data
from utils.calculator import calculate
from utils.completions import get_completion, update_message_history
from utils.display import c_print, configure_panda, print_in_box, plot_competitor_pricing_data, plot_sales_data, plot_weather_data


# Set the client and model
client = openai_client()
model = OpenAIModels.GPT_41_NANO

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


# Plot graphs
def plot_graphs():
    plot_competitor_pricing_data(competitor_pricing_df)
    plot_sales_data(sales_df)
    plot_weather_data(weather_df)

# plot_graphs()


react_system_prompt = """
You are a meticulous Retail Demand Analyst that can solve any task in a multi-step process using tool calls and reasoning.

--

## INSTRUCTIONS
- You will use step-by-step reasoning by
    - THINKING the next logical steps to take to complete the task and what next tool call to make to get one step closer to the final answer
    - ACTING on the single next tool call to make
- You will always respond with a single THINK/ACT message in the following format:
    - THINK:
    [Carry out any reasoning needed to solve the problem not requiring a tool call]
    [Conclusion about what next tool call to make based on what data is needed and what tools are available]
    - ACT:
    [Tool to use and arguments]
- As soon as you know the final answer, call the `final_answer` tool in an `ACT` message.
- ALWAYS provide a tool call after ACT:, else you will fail.
- ALWAYS ensure that the ACT: calls one of the available tools below with the appropriate data, else you will fail.

--

## AVAILABLE TOOLS
- `calculator(expression: str)`
    * Use this to perform an arithmetic calculations
    * Example Input: `ACT: calculator(expression="(11 + 1) / 2")`
    * Example Output: `OBSERVE: 6.0`
- `call_sales_api()`
    * Use this to get the relevant sales data
    * Example Input: `ACT: call_sales_api()`
    * Example Output: `OBSERVE: [{"date": "2024-01-10", "product_id": "P001", "product_name": "Product 1", "quantity": 255, "revenue": 15547.35}, ...]`
- `call_weather_api(date: str)`
    * Use this to fetch the weather details for a specified date
    * Example Input: `ACT: call_weather_api(date="2022-02-14")`
    * Example Output: `OBSERVE: {"date": "2024-01-10", "weather": "Sunny", "temperature": 72}`
- `final_answer(amount_after_spike: str, causes: list[str], date: str, percentage_spike: str)`
    * Use this to return the final answer
    * Example Input: `ACT: final_answer(amount_after_spike="32", causes=["Competitor X offering a 29 discount boosting category interest", ...], date="2020-06-12", percentage_spike="20.00%")`
    * Example Output: `OBSERVE: {"amount_after_spike": "32", "causes": ["Competitor X offering a 29 discount boosting category interest", ...], "date": "2020-06-12", "percentage_spike": "20.00%"}`

You will not use any other tools.

--

EXAMPLE:

```
--USER MESSAGE--
TASK:
Respond to the query "What was the weather one week ago?". Today is "2024-01-17.

--ASSISTANT MESSAGE--
THINK:
* I need to calculate the date oen week ago from 2024-01-17
* If today is 2024-01-17, then 1 days ago is 2024-01-10
* I can call the `call_weather_api` tool to get the weather data for 2024-01-10
* After that, if I have the weather data, I can return the final answer using the `final_answer` tool
* Tool call needed: Call the `call_weather_api` tool for 2024-01-10
ACT:
call_weather_api(date = "2024-01-10")

--USER MESSAGE--
OBSERVE:
{"date": "2024-01-10", "weather": "Sunny"}

--ASSISTANT MESSAGE--
THINK:
* I now have the weather data for 2024-01-10
* I can call the final_answer tool with the weather data
* Tool call needed: Call the `final_answer` tool with the weather data
ACT:
final_answer("The weather on 2024-01-10 was sunny.")

--USER MESSAGE--
OBSERVE:
The weather on 2024-01-10 was sunny.
```
"""

user_prompt_analyze = """
TASK:
Find the single largest sales spike according to the percentage increase with a short explanation for it based on factors such as weather.
"""


def get_observation_message(response: str) -> str:
    """
    Takes a THINK/ACT response, makes the correct tool call, and returns an observation message.

    Uses regex to match the specific tool call and return a valid message that the agent can understand.

    Args:
        - response (str): The THINK/ACT response.

    Returns:
        - str: The observation message.
    """
    observation_message = None

    SALES_API_REGEX = r"ACT:\ncall_sales_api\(\)"
    WEATHER_API_REGEX = r"ACT:\ncall_weather_api\(date=\"(.*)\"\)"
    CALCULATOR_REGEX = r"ACT:\ncalculator\(expression=\"(.*)\"\)"
    FINAL_ANSWER_REGEX = r"ACT:\nfinal_answer\(amount_after_spike=\"(.*)\", causes=(.*), date=\"(.*)\", percentage_spike=\"(.*)\"\)"

    if re.search(SALES_API_REGEX, response):
        observation_message = f"OBSERVE:\n{call_sales_api()}"
    elif weather_regex := re.search(WEATHER_API_REGEX, response):
        date = weather_regex.groups()[0]
        weather_data = call_weather_api(date=date)
        observation_message = f"OBSERVE:\n{weather_data}"
    elif calc_regex := re.search(CALCULATOR_REGEX, response):
        expression = calc_regex.groups()[0]
        observation_message = f"OBSERVE:\n{calculate(expression)}"
    elif final_ans_regex := re.search(FINAL_ANSWER_REGEX, response):
        amount_after_spike, causes, date, percent_spike = final_ans_regex.groups()
        causes = literal_eval(causes)
        observation_message = f"OBSERVE:\namount_after_spike: {amount_after_spike}\ndate: {date}\npercentage_spike: {percent_spike}\ncauses: {causes}"
    else:
        observation_message = f"OBSERVE:\nInvalid tool call or tool not supported. Use the format `ACT:\ntool_name"

    return observation_message

# TEST CASES - get_observation_message/1

assert (
    actual := get_observation_message("\nTHINK:\n[thinking here]\nACT:\ncall_sales_api()")
) == (expected := "OBSERVE:\n" + str(call_sales_api())), (f"{actual} != {expected}")

assert (
    actual := get_observation_message("THINK:\n[thinking here]\nACT:\ncall_weather_api(date=\"2024-01-12\")")
) == (expected := "OBSERVE:\n" + str(call_weather_api("2024-01-12"))), (f"{actual} != {expected}")

assert (
    actual := get_observation_message("THINK:\n[thinking here]\nACT:\nfinal_answer(amount_after_spike=\"10\", causes=[\"cause1\", \"cause2\"], date=\"2024-01-12\", percentage_spike=\"10%\")")
) == (expected := "OBSERVE:\namount_after_spike: 10\ndate: 2024-01-12\npercentage_spike: 10%\ncauses: ['cause1', 'cause2']"), (f"{actual} != {expected}")

assert (
    actual := get_observation_message("THINK:\n[thinking here]\nACT:\ncalculator(expression=\"10 + 7\")")
) == (expected := "OBSERVE:\n17.0"), (f"{actual} != {expected}")

# assert (
#     actual := get_observation_message("THINK:\n[thinking here]\nACT:\ninvalid_tool()")
# ) == (expected := "OBSERVE:\nInvalid tool call or tool not supported."), (f"{actual} != {expected}")

# assert (
#     actual := get_observation_message("THINK:\n[thinking here]\nACT_TYPO:\ncall_sales_api()")
# ) == (expected := "OBSERVE:\nInvalid tool call or tool not supported."), (f"{actual} != {expected}")



c_print(f"Sending prompts to #{model}")

# EXERCISE 1

# react_response, message_history = get_completion(client, model, user_prompt_analyze, [], react_system_prompt)
# for message in message_history:
#     if message["role"] == "system":
#         continue
#     print_in_box(message["content"], title=f"{message['role']}".capitalize())

# assert "ACT:" in message_history[-1]["content"], ("No ACT message found in the response")


# EXERCISE 2

MAX_REACT_STEPS = 15

react_steps_count = 0
message_history = []
observation_message = None

while True:
    react_steps_count += 1
    react_response, message_history = get_completion(client, model, user_prompt_analyze, message_history, react_system_prompt)
    print_in_box(react_response, title=f"Assistant (Think + Act). Step {react_steps_count}")
    
    observation_message = get_observation_message(react_response)
    update_message_history(message_history, observation_message, "user")

    # Check if this is the last tool to be called
    if "ACT:\nfinal_answer" in react_response:
        print_in_box(observation_message, title="Final Answer")
        break

    print_in_box(observation_message, title=f"User (Observe). Step #{react_steps_count}")

    if react_steps_count > MAX_REACT_STEPS:
        c_print("Max number of ReACT steps exceeded. Breaking out from loop")
        break

# TEST CASES - ReACT loop

assert "date: 2024-01-12" in observation_message, "ReACT Loop did not find the spike date"
assert "percentage_spike: 200" in observation_message, "ReACT Loop did not find the spike percentage increase"