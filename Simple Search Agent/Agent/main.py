# main.py
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load environment variables first
load_dotenv()

# Import the compiled application graph from graph.py
from graph import agent

def print_messages(event):
    """Formats terminal outputs cleanly based on message states."""
    messages = event.get("messages", [])
    if messages:
        latest_msg = messages[-1]
        if hasattr(latest_msg, "tool_calls") and latest_msg.tool_calls:
            print(f"🔧 [Agent calling tool]: {[tc['name'] for tc in latest_msg.tool_calls]}")
        elif latest_msg.content and not isinstance(latest_msg, HumanMessage):
            print(f"\nAgent: {latest_msg.content}")

def main():
    print("\n>> Lead Generation Agent Active! (Type 'quit' or 'exit' to stop)")
    print("Agent: Hello, I am ready to assist you. What company or market research can I perform for you?")
    
    state = {"messages": []}
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
            
        if not user_input.strip():
            continue

        # Add user query to context history
        state["messages"].append(HumanMessage(content=user_input))
        
        # Stream the graph state values
        for event in agent.stream(state, stream_mode="values"):
            print_messages(event)

if __name__ == "__main__":
    main()
    
    