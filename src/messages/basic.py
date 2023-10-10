from uagents import Model
from typing import List, Dict, Tuple


class ConvertRequest(Model):
    """
    Represents a request to convert base currency to target currencies

    Attributes:
        base_currency (str): base currency to convert from
        target_currencies (List[str]): target currencies to convert to
    """

    base_currency: str
    target_currencies: List[str]


class ConvertResponse(Model):
    """
    Response to a ConvertRequest containing the converted rates

    Attributes:
        rates (Dict[str, float]): dictionary of target currency to conversion rate
    """

    rates: Dict[str, float]


class Error(Model):
    """
    Represents an error message

    Attributes:
        error (str): error message
    """

    error: str


class Notification(Model):
    """
    Represents a notification message

    Attributes:
        name (str): name of the user
        email (str): email of the user
        base_cur (str): base currency of the user
        notif (List[Tuple[str, float, float]]): list of tuples containing the
            currency name, current rate, and threshold rate
    """

    name: str
    email: str
    base_cur: str
    notif: List[Tuple[str, float, float]]
