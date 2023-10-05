from uagents import Bureau
from agents.exchange import exchange_agent
from agents.user import user_agent

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    bureau.add(exchange_agent)
    bureau.add(user_agent)
    bureau.run()
