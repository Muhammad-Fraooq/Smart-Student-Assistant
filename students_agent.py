from agents import Agent, Runner,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled
from dotenv import load_dotenv
import chainlit as cl
import os

# Load environment variables
load_dotenv()

# Get GEMINI_API_KEY 
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Create Gemini client
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
    )

# Create model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
    )
set_tracing_disabled(True)

# Create Agent
agent = Agent(
    name="Smart Students Assistant",
    instructions="""
You are a highly intelligent and supportive assistant designed to help students with their studies.

You can:
- Answer academic questions clearly and accurately.
- Provide study tips and techniques tailored to different learning styles.
- Summarize short text passages concisely.

Always respond in a friendly and professional tone. Avoid unrelated or off-topic responses.
""",
    model=model
    )

@cl.on_chat_start
async def start():
    await cl.Message(content="""
## 🎓 Smart Student Assistant

Welcome! I'm here to help you succeed in your studies. I can:

- ✅ Answer academic questions  
- ✅ Provide effective study tips  
- ✅ Summarize short text passages  

💬 Type your question below to get started!
""").send()

@cl.on_message
async def main(message:cl.Message):
    query = message.content
    msg = cl.Message(content="Thinking...")
    await msg.send()

    # handle error 
    try:
        result = await Runner.run(agent,query)
        msg.content = result.final_output
        await msg.update()

    except Exception as e:
        msg.content = f"Error running agent: {str(e)}"
        await msg.update()