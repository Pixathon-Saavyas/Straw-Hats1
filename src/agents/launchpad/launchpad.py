from pydantic import Field
from ai_engine import KeyValue, UAgentResponse, UAgentResponseType
from booking_protocol import booking_proto
from uagents import Agent, Protocol, Context, Model
import requests
import uuid

launchpad_chooser_agent = Agent(name="Launchpad Agent", seed="40902090")

async def get_launchpads():
   url = "https://api.spacexdata.com/v3/landpads"
   response = requests.get(url)
   launchpads = response.json()
   '''full_response = ""
   for i, launchpad in enumerate(launchpads):
       full_response+=f"{i+1}. {launchpad['full_name']} \n   Location: {launchpad['location']['name']},{launchpad['location']['region']}\n"'''
   return launchpads



async def choose_launchpad(index):
    url = f"https://api.spacexdata.com/v3/landpads/{index}"
    response = requests.get(url)
    launchpad = response.json()
    return launchpad['full_name']+"selected!" 


launchpad_chooser_protocol = Protocol("LaunchpadChooser")


class Launchpad(Model):
    query: str = Field(message="random string")



@launchpad_chooser_protocol.on_message(model=Launchpad, replies={UAgentResponse})
async def on_message(ctx: Context, sender: str, msg: Launchpad):
    data = get_launchpads()
    options=[]
    ctx_storage = {}
    request_id = str(uuid.uuid4())
    for idx, launchpad in enumerate(data):
        option = f"""● {idx+1}. {launchpad['full_name']} \n   Location: {launchpad['location']['name']},{launchpad['location']['region']}"""
        options.append(KeyValue(key=idx, value=option))
        ctx_storage[idx] = option
    ctx.storage.set(request_id, ctx_storage)
    if options:
        await ctx.send(
            sender,
            UAgentResponse(
                options=options,
                type=UAgentResponseType.SELECT_FROM_OPTIONS,
                request_id=request_id
            ),
        )
    else:
        await ctx.send(
            sender,
            UAgentResponse(
                message="No launchpads found",
                type=UAgentResponseType.FINAL,
                request_id=request_id
            ),
        )

                   

launchpad_chooser_agent.include(launchpad_chooser_protocol)
launchpad_chooser_agent.include(booking_proto())
launchpad_chooser_agent.run()