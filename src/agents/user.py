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


@user_agent.on_event("startup")
async def initialize_storage(ctx: Context):
    ctx.storage.set("base", "INR")
    default_targets = {
        "USD": (1 / 85, 1 / 80),
        "EUR": (1 / 90, 1 / 85),
        "CAD": (1 / 58, 1 / 55),
    }
    ctx.storage.set("target", default_targets)


@user_agent_protocol.on_interval(20, messages=ConvertRequest)
async def get_currency_conversion_rates(ctx: Context):
    ctx.logger.info("Sending request to exchange agent")
    await ctx.send(
        EXCHANGE_AGENT_ADDRESS,
        ConvertRequest(
            base_currency=ctx.storage.get("base"),
            target_currencies=list(ctx.storage.get("target").keys()),
        ),
    )


@user_agent_protocol.on_message(model=ConvertResponse)
async def handle_response(ctx: Context, sender: str, msg: ConvertResponse):
    ctx.logger.info(f"Received response from Exchange({sender[:10]}): {msg}")
    thresholds = ctx.storage.get("target")
    for currency, rate in msg.rates.items():
        if rate <= thresholds[currency][0]:
            ctx.logger.critical(
                f"Rate for {currency} is {rate}. Sending alert to user."
            )
            # send notification to user
        elif rate >= thresholds[currency][1]:
            ctx.logger.critical(
                f"Rate for {currency} is {rate}. Sending alert to user."
            )
            # send notification to user


@user_agent_protocol.on_message(model=Error)
async def handle_error(ctx: Context, sender: str, msg: Error):
    ctx.logger.info(f"Received error from Exchange({sender[:10]}): {msg}")


user_agent.include(user_agent_protocol)
