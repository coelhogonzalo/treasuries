import json
import datetime

from urllib.request import urlopen

from BitcoinTreasuries.constants import (
    BTC_DEFAULT_PRICE,
    CATEGORIES_BY_TYPE,
    NAVBAR_LINKS,
)
from treasuries.enums import TreasuryType
from treasuries.models import Treasury


def parse_date(date_string):
    if not date_string:
        return None
    try:
        if len(date_string) == 4:
            return datetime.datetime.strptime(date_string, "%Y")
        elif len(date_string) == 6:
            return datetime.datetime.strptime(date_string, "%Y%m")
        elif len(date_string) == 8:
            return datetime.datetime.strptime(date_string, "%Y%m%d")
        elif len(date_string) == 10:
            return datetime.datetime.strptime(date_string, "%Y%m%d%H")
        elif len(date_string) == 12:
            return datetime.datetime.strptime(date_string, "%Y%m%d%H%M")
        elif len(date_string) == 14:
            return datetime.datetime.strptime(date_string, "%Y%m%d%H%M%S")
        else:
            return "Invalid date format"
    except ValueError:
        return "Invalid date format"


def get_bitcoin_price():
    try:
        url = "https://api.yadio.io/exrates/usd"
        with urlopen(url) as f:
            resp = json.load(f)
            btc_price = resp["BTC"]
            return btc_price
    except Exception as e:
        print("An error occurred while fetching the bitcoin price:", e)
        return BTC_DEFAULT_PRICE


def get_treasury_by_type(type):
    return Treasury.objects.filter(treasury_type=type).order_by("-btc")


def get_miners():
    return Treasury.objects.filter(miner=True).order_by("-btc")


def get_miners_latest_update():
    return (
        Treasury.history.filter(miner=True)
        .order_by("-history_date")
        .first()
        .history_date.date()
    )


def get_treasury_count():
    return Treasury.objects.count()


def get_latest_update_by_type(type=None):
    if type:
        return (
            Treasury.history.filter(treasury_type=type)
            .order_by("-history_date")
            .first()
            .history_date.date()
        )
    return Treasury.history.order_by("-history_date").first().history_date.date()


def get_latest_updates():
    latest_updates = {}
    types = [type.value for type in TreasuryType]
    for type in types:
        latest_updates[CATEGORIES_BY_TYPE[type]] = get_latest_update_by_type(type)
    latest_updates["miners"] = get_miners_latest_update()
    latest_updates["treasuries"] = get_latest_update_by_type()
    return latest_updates
