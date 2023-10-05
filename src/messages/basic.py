from uagents import Model
from typing import List, Dict, Tuple


class ConvertRequest(Model):
    base_currency: str
    target_currencies: List[str]


class ConvertResponse(Model):
    rates: Dict[str, float]


class Error(Model):
    error: str


class UserPreference(Model):
    base: str
    thresholds: Dict[str, tuple[float, float]]
    # Dict[Currency, Tuple(lower, upper)]
