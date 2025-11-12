
## Common Types of Agents as Building Blocks

- **Direct Prompt Agent**: The simplest; sends a user's query directly to an LLM.
- **Augmented Prompt Agent**: Adds a persona or system instructions to the LLM call to shape the response.
- **Knowledge Augmented Prompt Agent**: Uses a defined persona AND a specific, curated knowledge base to answer, ignoring the LLM's general knowledge.
- **RAG Knowledge Prompt Agent (Retrieval-Augmented Generation)**: Dynamically retrieves relevant information from a large dataset before answering, making it flexible and less prone to making things up.
- **Evaluation Agent**: Acts as a quality controller, assessing the output of other agents against criteria and potentially prompting revisions.
- **Routing Agent**: The "project manager" that directs incoming tasks to the most suitable specialized agent.
- **Action Planning Agent**: Takes a complex goal and breaks it down into a sequence of smaller, executable steps.