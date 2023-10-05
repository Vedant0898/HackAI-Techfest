from uagents import Agent, Context, Protocol

from uagents.setup import fund_agent_if_low

from messages.basic import ConvertRequest, ConvertResponse, Error
from typing import List


user_agent = Agent(
    name="user",
    seed="user agent",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)

fund_agent_if_low(user_agent.wallet.address())

EXCHANGE_AGENT_ADDRESS = (
    "agent1qt0ad7cync8z7fz35yrmcr0558734fa63jws9xuymmkrkhea67lqykkrfst"
)

user_agent_protocol = Protocol("Convert")


@user_agent_protocol.on_interval(20, messages=ConvertRequest)
async def get_currency_conversion_rates(ctx: Context):
    ctx.logger.info("Sending request to exchange agent")
    await ctx.send(
        EXCHANGE_AGENT_ADDRESS,
        ConvertRequest(base_currency="INR", target_currencies=["USD", "EUR", "CAD"]),
    )


@user_agent_protocol.on_message(model=ConvertResponse)
async def handle_response(ctx: Context, sender: str, msg: ConvertResponse):
    ctx.logger.info(f"Received response from {sender}: {msg}")


@user_agent_protocol.on_message(model=Error)
async def handle_error(ctx: Context, sender: str, msg: Error):
    ctx.logger.info(f"Received error from {sender}: {msg}")


user_agent.include(user_agent_protocol)
