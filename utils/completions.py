
def get_completion(client, model, user_prompt, messages = [], system_prompt = None) -> tuple[str, list[dict[str, str]]]:
    """
    Function to get a completion from an LLM API.

    Args:
        system_prompt: The system prompt
        user_prompt: The user prompt
        model: The model to use
        client: The LLM provider
    """

    try:
        build_messages(messages, user_prompt, system_prompt)

        response = client.chat.completions.create(
            model = model,
            messages = messages,
            temperature = 0.7
        )

        response_message = response.choices[0].message.content

        update_message_history(messages, response_message)

        return response_message, messages
    except Exception as e:
        return f"An error occurred while getting chat completion: {e}", messages


def build_messages(message_history: list, user_prompt: str, system_prompt: str) -> None:
    """
    Function to build messages. This is useful when there is a message history
    """

    if message_history:
        message_history.append({"role": "user", "content": user_prompt})
    else:
        message_history.extend([
            {"role": "system", "content": gen_system_prompt(system_prompt)},
            {"role": "user", "content": user_prompt}
        ])


def gen_system_prompt(prompt = None) -> str:
    return prompt if prompt else "You are a helpful assistant"


def update_message_history(message_history: list, llm_response: str, role = "assistant") -> None:
    message_history.append({"role": role, "content": llm_response})