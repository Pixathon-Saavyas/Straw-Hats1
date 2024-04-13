from pydantic import Field
from ai_engine import KeyValue, UAgentResponse, UAgentResponseType
from booking_protocol import booking_proto
from uagents import Agent, Protocol, Context, Model
import requests
import uuid

rocket_chooser_agent = Agent(name="Rocket Agent", seed="60902090")

async def get_rockets(weight):
   url = "https://api.spacexdata.com/v3/rockets"
   response = requests.get(url)
   rockets = response.json()
   return ([rocket for rocket in rockets if rocket['mass']['kg'] > int(weight)])

rocket_chooser_protocol = Protocol("RocketChooser")


class Rocket(Model):
    weight: str = Field(message="total weight of the person")
    
@rocket_chooser_protocol.on_message(model=Rocket, replies={UAgentResponse})
async def on_message(ctx: Context, sender: str, msg: Rocket):
    data = get_rockets(msg.weight)
    options=[]
    ctx_storage = {}
    request_id = str(uuid.uuid4())
    for idx, rocket in enumerate(data):
        option = f"""● {idx+1}. {rocket['rocket_name']}"""
        options.append(KeyValue(key=idx, value=option))
        ctx_storage[idx] = option
    ctx_storage["weight"]=msg.weight
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
                message="No rockets found",
                type=UAgentResponseType.FINAL,
                request_id=request_id
            ),
        )

                   

rocket_chooser_agent.include(rocket_chooser_protocol)
rocket_chooser_agent.include(booking_proto())
rocket_chooser_agent.run()