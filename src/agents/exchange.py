import os

import dotenv
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low

from messages.basic import ConvertRequest, ConvertResponse, Error
from utils.api_utils import get_exchange_rates

# Load environment variables
dotenv.load_dotenv()

# Create exchange agent
EXCHANGE_AGENT_SEED = os.getenv("EXCHANGE_AGENT_SEED", "exchange agent secret phrase")

exchange_agent = Agent(
    name="exchange",
    seed=EXCHANGE_AGENT_SEED,
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

# Ensure the agent has enough funds
fund_agent_if_low(exchange_agent.wallet.address())


# Create a protocol for conversion requests
exchange_agent_protocol = Protocol("Convert")


# Function to handle incoming conversion requests
@exchange_agent_protocol.on_message(
    model=ConvertRequest, replies={ConvertResponse, Error}
)
async def handle_request(ctx: Context, sender: str, msg: ConvertRequest):
    success, data = get_exchange_rates(msg.base_currency, msg.target_currencies)
    if success:
        await ctx.send(
            sender,
            ConvertResponse(rates=data),
        )
    else:
        ctx.logger.error(f"Error: {data}")
        await ctx.send(
            sender,
            Error(error=data),
        )


# include protocol with the agent
exchange_agent.include(exchange_agent_protocol)
