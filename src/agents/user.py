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
