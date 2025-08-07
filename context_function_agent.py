from llama_index.core.workflow import Context
from llama_index.core.agent import FunctionAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
import asyncio


def multiply(a: float, b: float) -> float:
    return a * b

async def main():
    """
    ReActAgent with tools and context - this should work!
    """
    print("=== ReActAgent with Tools and Context ===")
    
    agent = FunctionAgent(
        tools=[multiply], 
        llm=Ollama(
            model="llama3.1",
            request_timeout=360.0,
            context_window=8000,
        ),
        system_prompt="You are a helpful assistant that can multiply two numbers. You also have the capabilities of remembering previous asked questions and your answer.",
        max_iterations=5,
        verbose=True  # see what the agent is thinking
    )

    ctx = Context(agent)

    print("Question 1: What is 6 * 6?")
    response1 = await agent.run("What is 6 * 6?", ctx=ctx)
    print(f"Response 1: {response1}")
    print()

    print("Question 2: What was the answer to the previous question?")
    response2 = await agent.run("What was the answer to the previous question?", ctx=ctx)
    print(f"Response 2: {response2}")
    print()


if __name__ == "__main__":
    asyncio.run(main())