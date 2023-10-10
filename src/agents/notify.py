import os

import dotenv
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low

from messages.basic import Notification
from utils.email_utils import send_email

# Load environment variables
dotenv.load_dotenv()

# Create notify agent
NOTIFY_AGENT_SEED = os.getenv("NOTIFY_AGENT_SEED", "notify agent secret phrase")

notify_agent = Agent(
    name="notify",
    seed=NOTIFY_AGENT_SEED,
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)

# Ensure the agent has enough funds
fund_agent_if_low(notify_agent.wallet.address())


# Function to generate the mail body from the template
def generate_context(msg: Notification):
    alerts = []
    for n in msg.notif:
        tmp = {}
        tmp["target_cur"] = n[0]
        tmp["current_rate"] = n[1]
        tmp["threshold"] = n[2]
        tmp["type"] = "Max" if n[1] > n[2] else "Min"
        alerts.append(tmp)
    context = {
        "name": msg.name,
        "ismultiple": len(msg.notif) > 1,
        "alerts": alerts,
        "base_cur": msg.base_cur,
    }
    return context


# Create a protocol for notifications
notify_protocol = Protocol("Notify")


# Function to handle incoming notifications requests
@notify_protocol.on_message(model=Notification)
async def send_notification(ctx: Context, sender: str, msg: Notification):
    ctx.logger.info(f"Received notification from user({sender[:20]}):\n{msg}")
    context = generate_context(msg)
    success, data = await send_email(msg.name, msg.email, context)
    if success:
        ctx.logger.info("Email sent successfully")
    else:
        ctx.logger.error(f"Error sending email: {data}")


# include protocol with the agent
notify_agent.include(notify_protocol)
