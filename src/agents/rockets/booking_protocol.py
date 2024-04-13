### Write code for the new module here and import it from agent.py.
from ai_engine import UAgentResponse, UAgentResponseType, BookingRequest
from uagents import Protocol, Context

def booking_proto():
    protocol = Protocol("BookingProtocol")

    @protocol.on_message(model=BookingRequest, replies={UAgentResponse})
    async def booking_handler(ctx: Context, sender: str, msg: BookingRequest):
        ctx.logger.info(f"Received booking request from {sender}")
        try:
            option = ctx.storage.get(msg.request_id)
            ctx.storage.set("choosen_options", option[msg.user_response])
            await ctx.send(
                sender,
                UAgentResponse(
                    message=f"Thanks for choosing an option - {option[msg.user_response]} and weight={option['weight']}",
                    type=UAgentResponseType.FINAL,
                    request_id=msg.request_id
                )
            )
        except Exception as exc:
            ctx.logger.error(exc)
            await ctx.send(
                sender,
                UAgentResponse(
                    message=str(exc),
                    type=UAgentResponseType.ERROR
                )
            )

    return protocol