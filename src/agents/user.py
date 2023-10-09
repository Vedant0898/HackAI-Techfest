from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
import json

from messages.basic import ConvertRequest, ConvertResponse, Error, Notification


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

NOTIFY_AGENT_ADDRESS = (
    "agent1q2x94ysu3vxzm900g9d7j9j47egagfvd950j3rn09pljqls7ll7z7kyzhj5"
)

user_agent_protocol = Protocol("Convert")
user_agent_protocol2 = Protocol("Notify")


@user_agent.on_event("startup")
async def initialize_storage(ctx: Context):
    # try to get user's preferences from data.json
    status = await update_internal_state(ctx, force=False)
    if status:
        return
    # else set default values
    ctx.storage.set("base", "INR")
    default_targets = {
        "USD": (1 / 85, 1 / 80),
        "EUR": (1 / 90, 1 / 85),
        "CAD": (1 / 58, 1 / 55),
    }
    ctx.storage.set("target", default_targets)


async def update_internal_state(ctx: Context, force=False):
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        ctx.logger.error("data.json not found. Skipping update.")
        return False

    # check if data has been updated
    if data["hasChanged"] or force:
        ctx.logger.info("Updating internal state")
        ctx.storage.set("base", data["base"])
        ctx.storage.set("target", data["target"])
        data["hasChanged"] = False
        with open("data.json", "w") as file:
            json.dump(data, file)
        return True
    return False


@user_agent_protocol.on_interval(600, messages=ConvertRequest)
async def get_currency_conversion_rates(ctx: Context):
    # update internal state
    await update_internal_state(ctx)

    ctx.logger.info(f"Request sent to Exchange agent({EXCHANGE_AGENT_ADDRESS[:15]}...)")
    await ctx.send(
        EXCHANGE_AGENT_ADDRESS,
        ConvertRequest(
            base_currency=ctx.storage.get("base"),
            target_currencies=list(ctx.storage.get("target").keys()),
        ),
    )


@user_agent_protocol.on_message(model=ConvertResponse)
async def handle_response(ctx: Context, sender: str, msg: ConvertResponse):
    ctx.logger.info(f"Received response from Exchange({sender[:15]}...)")
    thresholds = ctx.storage.get("target")
    notification = []
    for currency, rate in msg.rates.items():
        if rate <= thresholds[currency][0]:
            ctx.logger.critical(
                f"Rate for {currency} is {rate}. Sending alert to user."
            )
            notification.append((currency, rate, thresholds[currency][0]))
        elif rate >= thresholds[currency][1]:
            ctx.logger.critical(
                f"Rate for {currency} is {rate}. Sending alert to user."
            )
            notification.append((currency, rate, thresholds[currency][1]))
    if notification:
        await ctx.send(
            NOTIFY_AGENT_ADDRESS,
            Notification(
                name="Vedant",
                email="vedant.tamhane03@gmail.com",
                base_cur=ctx.storage.get("base"),
                notif=notification,
            ),
        )


@user_agent_protocol.on_message(model=Error)
async def handle_error(ctx: Context, sender: str, msg: Error):
    ctx.logger.error(f"Received Error from Exchange({sender[:15]}...): {msg.error}")


user_agent.include(user_agent_protocol)
user_agent.include(user_agent_protocol2)
