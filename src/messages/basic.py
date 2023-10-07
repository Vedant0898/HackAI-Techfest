from uagents import Model
from typing import List, Dict


class ConvertRequest(Model):
    base_currency: str
    target_currencies: List[str]


class ConvertResponse(Model):
    rates: Dict[str, float]


class Error(Model):
    error: str
