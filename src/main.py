# Import necessary modules and packages
from pydantic import Field  # For defining fields in Pydantic models
from ai_engine import UAgentResponse, UAgentResponseType  # Custom types for agent responses
from uagents import Agent, Protocol, Context, Model  # Classes for defining agents and protocols
from uagents.setup import fund_agent_if_low  # Helper function for funding agents
import google.generativeai as genai  # Importing GenerativeAI module from Google
import requests  # For making HTTP requests
import os  # For working with environment variables
from dotenv import load_dotenv, find_dotenv  # For loading environment variables from .env file
from pathlib import Path  # For working with file paths

# Load environment variables from .env file
load_dotenv(Path("../.env"))

# Define constants
AGENT_MAILBOX_KEY = "389cc094-754b-4b99-8c0f-41f5eade99d7"  # Unique identifier for agent mailbox
API_KEY = os.getenv("API_KEY")  # API key from environment variables
GENAI_KEY = os.getenv("GENAI_KEY")  # GenerativeAI key from environment variables

# Create a new agent instance
agent = Agent(name="NASA Agent", seed="10902090", mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai")

# Fund the agent if its wallet balance is low
fund_agent_if_low(agent.wallet.address())

# Configure GenerativeAI with the provided API key
genai.configure(api_key=GENAI_KEY)

# Create a GenerativeAI model instance
model = genai.GenerativeModel('gemini-pro')

# Start a chat session with the GenerativeAI model
chat = model.start_chat(history=[])

# Define a function to handle user messages in the chat session
async def handle_message(message):
    # Get user input
    user_message = message
        
    # Check if the user wants to quit the conversation
    if user_message.lower() == 'quit':
            return "Exiting chat session."
            
    # Send the message to the chat session and receive a streamed response
    response = chat.send_message(user_message, stream=True)
        
    # Initialize an empty string to accumulate the response text
    full_response_text = ""
        
    # Accumulate the chunks of text
    for chunk in response:
            full_response_text += chunk.text
            
    # Print the accumulated response as a single paragraph
    message = full_response_text
    return message

# Define a function to fetch news from NASA API and process it through the chatbot
async def get_news(start_date: str, end_date: str):
    """
    Uploads image data to Cloudinary Storage.
    Args:
        start_data (str) (format=YYYY-MM-DD): Date from where you want your news to start
        end_data (str) (format=YYYY-MM-DD): Date from where you want your news to start
    Returns:
        str: News about Space from start date to end date
    """
    # Construct URL for fetching news from NASA API
    url = f"https://api.nasa.gov/DONKI/notifications?startDate={start_date}&endDate={end_date}&type=all&api_key=DEMO_KEY"
    
    # Make a GET request to the NASA API
    response = requests.get(url)
    
    # Extract the news content from the API response
    body = (response.json()[0]["messageBody"])
    
    # Process the news content through the chatbot
    news = await handle_message("Explain this news to me like a 15 year old: " + body)
    
    return news

# Define a Pydantic model for representing news query parameters
class News(Model):
    start_date: str = Field(description="Date from where you want your news to start (allowed dates from 1900 to 2024) (format=YYYY-MM-DD)")
    end_date: str = Field(description="Date from where you want your news to end (allowed dates from 1900 to 2024) (format=YYYY-MM-DD)")

# Define a protocol for handling news requests
news_protocol = Protocol("News")

# Define a startup event handler for the agent
@agent.on_event("startup")
async def on_startup(ctx: Context):
    print(agent.address)

# Define a message handler for the news protocol
@news_protocol.on_message(model=News, replies={UAgentResponse})
async def on_message(ctx: Context, sender: str, msg: News):
    # Fetch news based on the provided query parameters
    message = await get_news(msg.start_date, msg.end_date)
    
    # Send the processed news as a response
    await ctx.send(sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL))

# Include the news protocol in the agent and publish its manifest
agent.include(news_protocol, publish_manifest=True)

# Run the agent
agent.run()
