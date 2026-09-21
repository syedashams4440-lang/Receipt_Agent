from llm_config import llm

from tools import (
    lookup_order,
    calculate_return_deadline,
    calculate_warranty_deadline,
    policy_search
)

from langchain_core.messages import ToolMessage


# All tools available to the agent
tools = [
    lookup_order,
    calculate_return_deadline,
    calculate_warranty_deadline,
    policy_search
]


# Connect tools to the LLM
llm_with_tools = llm.bind_tools(tools)


# Create a dictionary so we can find a tool by name
tool_map = {
    "lookup_order": lookup_order,
    "calculate_return_deadline": calculate_return_deadline,
    "calculate_warranty_deadline": calculate_warranty_deadline,
    "policy_search": policy_search
}


SYSTEM_PROMPT = """
You are a helpful Receipt and Order Assistant.

You help users with:
- Order information
- Return deadlines
- Warranty deadlines
- Store return and warranty policies

Rules:

1. When the user provides an Order ID, use lookup_order first.

2. If the user asks for a return deadline:
   - Look up the order if necessary.
   - Get the purchase date.
   - Use calculate_return_deadline.

3. If the user asks for a warranty deadline:
   - Look up the order if necessary.
   - Get the purchase date.
   - Use calculate_warranty_deadline.

4. Use policy_search when the user asks about:
   - return rules
   - return eligibility
   - warranty coverage
   - warranty rules
   - final sale products
   - conditions for return or warranty

5. For return or warranty eligibility questions,
   use policy_search before giving the final answer.

6. Never invent an order.

7. If an order is not found, clearly say that the order
   was not found.

8. Never invent dates.

9. Only use information provided by:
   - the receipt
   - the order database
   - the store policy
   - tool calculations

10. Never invent:
    - store locations
    - online return procedures
    - shipping procedures
    - pickup procedures
    - packaging requirements
    - return instructions
    - acceptance decisions
    - product conditions not stated in the policy

11. Do not assume whether an order is final sale.
    Use the Final sale field returned by lookup_order.

12. Do not say that a return will definitely be accepted.
    Explain eligibility based only on the available policy
    and order information.

13. If the available information does not establish something,
    clearly say that the information is not available.

14. When reporting days remaining, use the exact value returned
    by the deadline calculation tool. Do not recalculate it.

15. Treat the deadline tool's result as authoritative.

16. After using the required tools, give a clear and concise
    final answer.

17. When explaining return eligibility, only state that a product
    appears eligible if all required conditions from the policy
    and order information are satisfied.

18. Do not invent or suggest return procedures.
    The policy only says that original receipt or order information
    is required. Do not mention stores, online portals, shipping,
    pickup, or other procedures unless explicitly provided.

19. Do not say a return "will be accepted".
    Say that the product appears eligible based on the available
    policy and order information.

20. When reporting days remaining, use the exact value returned
    by calculate_return_deadline or calculate_warranty_deadline.
    Do not recalculate it yourself.
"""


def ask_agent(question):

    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", question)
    ]

    # Agent loop
    while True:

        # Ask the LLM what to do
        response = llm_with_tools.invoke(messages)

        # Add the LLM response to conversation history
        messages.append(response)

        # If there are no tool calls,
        # the LLM has produced the final answer
        if not response.tool_calls:
            return response

        # Execute every tool requested by the LLM
        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"\n🔧 Calling tool: {tool_name}")
            print(f"Arguments: {tool_args}")

            # Find the correct tool
            tool = tool_map.get(tool_name)

            if tool is None:
                tool_result = f"Unknown tool: {tool_name}"

            else:
                # Execute the tool
                tool_result = tool.invoke(tool_args)

            print(f"Tool result: {tool_result}")

            # Send the tool result back to the LLM
            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )
