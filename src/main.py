# Here we demonstrate how we can create a simple coin toss agent that is compatible with DeltaV.

# After running this agent, it can be registered to DeltaV on Agentverse's Services tab. For registration you will have to use the agent's address. 
#

# third party modules used in this example
from pydantic import Field
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Protocol, Context, Model
from uagents.setup import fund_agent_if_low
import google.generativeai as genai
import requests

AGENT_MAILBOX_KEY = "389cc094-754b-4b99-8c0f-41f5eade99d7"
agent = Agent(name="NASA Agent", seed="10902090", mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai")
fund_agent_if_low(agent.wallet.address())

API_KEY="DEMO_KEY"

class Message(Model):
    message:str

genai.configure(api_key="AIzaSyAKFCjtJJ_vn7h0EwqA9fthrpw859OcTEc")
model=genai.GenerativeModel('gemini-pro')

chat=model.start_chat(history=[])

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

async def get_news(start_date:str, end_date:str):
    """
        Uploads image data to Cloudinary Storage.
        Args:
            start_data (str) (format=YYYY-MM-DD): Date from where you want your news to start
            end_data (str) (format=YYYY-MM-DD): Date from where you want your news to start
        Returns:
            str: News about Space from start date to end date
    """
    url = f"https://api.nasa.gov/DONKI/notifications?startDate={start_date}&endDate={end_date}&type=all&api_key=DEMO_KEY"
    response = requests.get(url)
    body = (response.json()[0]["messageBody"])
    news = await handle_message("Explain this news to me like a 15 year old: "+body)
    print(news)
    return news

class News(Model):
    start_date: str = Field(description="Date from where you want your news to start (allowed dates from 1900 to 2024) (format=YYYY-MM-DD)")
    end_date: str = Field(description="Date from where you want your news to end (allowed dates from 1900 to 2024) (format=YYYY-MM-DD)")

news_protocol = Protocol("News")

@agent.on_event("startup")
async def on_startup(ctx: Context):
    print(agent.address)
    
    #await ctx.send(agent.address, News(start_date="2023-01-02", end_date="2024-01-02"))


@news_protocol.on_message(model=News, replies={UAgentResponse})
async def on_message(ctx: Context, sender: str, msg: News):
    message = await get_news(msg.start_date, msg.end_date)
    await ctx.send(sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
)


agent.include(news_protocol, publish_manifest=True)
agent.run()