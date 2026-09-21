from agent import ask_agent


question = input("\nAsk the agent: ")

response = ask_agent(question)

print("\n===== AGENT RESPONSE =====\n")

print(response.content)

print("\n===== TOOL CALLS =====\n")

print(response.tool_calls)
