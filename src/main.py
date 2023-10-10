from uagents import Bureau
from agents.exchange import exchange_agent
from agents.user import user_agent
from agents.notify import notify_agent

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    print(f"Adding Exchange agent to Bureau : {exchange_agent.address}")
    bureau.add(exchange_agent)
    print(f"Adding Notify agent to Bureau : {notify_agent.address}")
    bureau.add(notify_agent)
    print(f"Adding User agent to Bureau : {user_agent.address}")
    bureau.add(user_agent)
    bureau.run()
