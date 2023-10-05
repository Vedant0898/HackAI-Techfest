from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from typing import List
from messages.basic import ConvertRequest, ConvertResponse, Error

import requests

ACCESS_TOKEN = "cur_live_aDyyqOV1xkgTPvUSdp3743MvF7d4gPqPe6qw6wTg"
BASE_URL = "https://api.currencyapi.com/v3/latest"

# "https://api.currencyapi.com/v3/latest?apikey=cur_live_aDyyqOV1xkgTPvUSdp3743MvF7d4gPqPe6qw6wTg&currencies=EUR%2CUSD%2CCAD&base_currency=INR"

exchange_agent = Agent(
    name="exchange",
    seed="exchange agent",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(exchange_agent.wallet.address())
print(exchange_agent.address)


async def get_exchange_rates(base_cur: str, symbols: List[str]):
    url = f'{BASE_URL}?apikey={ACCESS_TOKEN}&currencies={"%2C".join(symbols)}&base_currency={base_cur}'

    res = requests.get(url)
    # print(res)
    if res.status_code == 200:
        d = {}
        r = res.json()
        for sym in r["data"].keys():
            d[sym] = r["data"][sym]["value"]
        # print(d)
        return True, d
    else:
        # print(res.json())
        return False, res.json()["errors"]


exchange_agent_protocol = Protocol("Convert")


@exchange_agent_protocol.on_message(
    model=ConvertRequest, replies={ConvertResponse, Error}
)
async def handle_request(ctx: Context, sender: str, msg: ConvertRequest):
    ctx.logger.info(f"Received request from {sender}: {msg}")
    success, data = await get_exchange_rates(msg.base_currency, msg.target_currencies)
    if success:
        await ctx.send(
            sender,
            ConvertResponse(rates=data),
        )
    else:
        await ctx.send(
            sender,
            Error(error=data),
        )


exchange_agent.include(exchange_agent_protocol)

# r = get_exchange_rates("INR", ["USD", "EUR", "CAD"])
# print(r)
