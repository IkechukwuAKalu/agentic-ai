# Matching Recipes to Dietary Restrictions - Prompt Refinement

import jinja2

from mock_data.recipes import get_dietary_restrictions, get_recipes
from models.c_openai import openai_client, OpenAIModels
from utils.completions import get_completion
from utils.display import c_print


# Set the client and model
client = openai_client()
model = OpenAIModels.GPT_41_NANO

# Print the LLM config
c_print(client)
c_print(f"Current model is {model}")


# Uses jinja2 to add variables to the template
def format_prompt(recipe, prompt):
    ingredients_str = "\n".join(["- " + ingredient for ingredient in recipe["ingredients"]])
    instructions_str = "\n".join([f"{i + 1}. {instruction}" for i, instruction in enumerate(recipe["instructions"])])
    restrictions_str = ", ".join(get_dietary_restrictions())

    return jinja2.Template(prompt).render(
        recipe_name=recipe["name"],
        recipe_ingredients=ingredients_str,
        recipe_instructions=instructions_str,
        dietary_restrictions=restrictions_str
    )


initial_prompt = """
Analyze the following recipe and determine whether it satisfies each dietary restriction in the list.
For each restriction, classify it as "satisfied", "not satisfied", or "undeterminable" based on the recipe information.

Recipe: {{ recipe_name }}

Ingredients:
{{ recipe_ingredients }}

Instructions:
{{ recipe_instructions }}

Dietary Restrictions to Check:
{{ dietary_restrictions }}

Please provide your response in JSON format.
"""

refined_prompt_1 = """
You are a dietary consultant specializing in food allergies and dietary restrictions.

Analyze the following recipe and determine whether it satisfies each dietary restriction in the list.
For each restriction, classify it as "satisfied", "not satisfied", or "undeterminable" based on the recipe information.

Import context and definitions for dietary restrictions:
- Vegetarian: No meat, poultry, fish, or seafood. May include eggs and dairy products.
- Vegan: No animal products whatsoever, including meat, dairy, eggs, honey.
- Gluten-free: No wheat, barley, rye, or derivatives. Note that regular all-purpose flour contains gluten.
- Dairy-free: No milk, cheese, butter, cream, or other dairy products.
- Nut-free: No tree nuts or peanuts.
- Egg-free: No eggs or products containing eggs.
- Low-sodium: Limited salt and naturally high-sodium ingredients.
- Keto: Very low carbohydrate, high fat, moderate protein.
- Paleo: No grains, legumes, dairy, refined sugar, or processed foods.
- Kosher: Follows Jewish dietary laws (no pork, shellfish, mixing meat and dairy, etc.).

Guidelines for your analysis:
- Mark a restriction as "satisfied" only if you are certain the recipe meets it.
- Mark a restriction as "not satisfied" if any ingredient clearly violates it.
- Mark a restriction as "undeterminable" if you lack sufficient information (e.g., exact type of broth, potential cross-contamination).
- For each classification, briefly explain your reasoning and identify specific ingredients that affect your decision.

Recipe: {{ recipe_name }}

Ingredients:
{{ recipe_ingredients }}

Instructions:
{{ recipe_instructions }}

Dietary Restrictions to Check:
{{ dietary_restrictions }}

Please provide your response in JSON format where:
- Each key is the name of a dietary restriction
- Each value is an object with the following properties:
    - "classification": "satisfied", "not satisfied", or "undeterminable"
    - "explanation": a brief reasoning for your classification
    - "critical_ingredients": an array of ingredients that influenced your classification
"""

refined_prompt_2 = """
You are a dietary consultant specializing in food allergies and dietary restrictions.

Analyze the following recipe and determine whether it satisfies each dietary restriction in the list.
For each restriction, classify it as "satisfied", "not satisfied", or "undeterminable" based on the recipe information.

Import context and definitions for dietary restrictions:
- Vegetarian: No meat, poultry, fish, or seafood. May include eggs and dairy products.
- Vegan: No animal products whatsoever, including meat, dairy, eggs, honey.
- Gluten-free: No wheat, barley, rye, or derivatives. Note that regular all-purpose flour contains gluten.
- Dairy-free: No milk, cheese, butter, cream, or other dairy products.
- Nut-free: No tree nuts or peanuts.
- Egg-free: No eggs or products containing eggs.
- Low-sodium: Limited salt and naturally high-sodium ingredients.
- Keto: Very low carbohydrate, high fat, moderate protein.
- Paleo: No grains, legumes, dairy, refined sugar, or processed foods.
- Kosher: Follows Jewish dietary laws (no pork, shellfish, mixing meat and dairy, etc.).

Guidelines for your analysis:
- Mark a restriction as "satisfied" only if you are certain the recipe meets it.
- Mark a restriction as "not satisfied" if any ingredient clearly violates it.
- Mark a restriction as "undeterminable" if you lack sufficient information (e.g., exact type of broth, potential cross-contamination).
- For each classification, briefly explain your reasoning and identify specific ingredients that affect your decision.

Handling ambiguities:
- For "vegetable oil" or unspecified oil, consider it plant-based unless otherwise noted.
- Assume "broth" or "stock" matches the recipe's main protein unless specified (e.g., chicken recipe implies chicken broth).
- For baked goods, assume standard ingredients unless specified (e.g., all-purpose flour is not gluten-free).
- For ambiguous ingredients, err on the side of "undeterminable" rather than making assumptions.
- Consider potential cross-contamination for severe allergies (nuts, gluten).

Example analysis for a simple recipe:

```
Recipe: Basic Pancakes
Ingredients:
- 1 cup all-purpose flour
- 2 tbsp sugar
- 1 tsp baking powder
- 1/2 tsp salt
- 1 egg
- 1 cup milk
- 2 tbsp butter, melted

Response:
{
  "vegetarian": {
    "classification": "satisfied",
    "explanation": "All ingredients are vegetarian; contains no meat, poultry, fish, or seafood.",
    "critical_ingredients": []
  },
  "vegan": {
    "classification": "not satisfied",
    "explanation": "Contains animal products.",
    "critical_ingredients": ["1 egg", "1 cup milk", "2 tbsp butter, melted"]
  },
  "gluten-free": {
    "classification": "not satisfied",
    "explanation": "Contains all-purpose flour which contains gluten.",
    "critical_ingredients": ["1 cup all-purpose flour"]
  }
}
```

Recipe: {{ recipe_name }}

Ingredients:
{{ recipe_ingredients }}

Instructions:
{{ recipe_instructions }}

Dietary Restrictions to Check:
{{ dietary_restrictions }}

Please provide your response in JSON format where:
- Each key is the name of a dietary restriction
- Each value is an object with the following properties:
    - "classification": "satisfied", "not satisfied", or "undeterminable"
    - "explanation": a brief reasoning for your classification
    - "critical_ingredients": an array of ingredients that influenced your classification
"""


# EXERCISE 1

# recipe_1 = get_recipes()[0]
# formatted_prompt = format_prompt(recipe_1, initial_prompt)

# c_print(f"Sending prompt to {model}")

# initial_response = get_completion(client, model, formatted_prompt)
# c_print(f"Initial prompt response for {recipe_1['name']}:\n{initial_response[0]}\n")


# # EXERCISE 2

# recipe_2 = get_recipes()[0]
# formatted_prompt = format_prompt(recipe_2, refined_prompt_1)

# c_print(f"Sending prompt to {model}")

# refined_response_1 = get_completion(client, model, formatted_prompt)
# c_print(f"Refined prompt response [1] for {recipe_2['name']}:\n{refined_response_1[0]}\n")


# EXERCISE 3

recipe_3 = get_recipes()[0]
formatted_prompt = format_prompt(recipe_3, refined_prompt_2)

c_print(f"Sending prompt to {model}")

refined_response_2 = get_completion(client, model, formatted_prompt)
c_print(f"Refined prompt response [2] for {recipe_3['name']}:\n{refined_response_2[0]}\n")