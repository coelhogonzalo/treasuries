import json
import datetime

from urllib.request import urlopen

from BitcoinTreasuries.constants import BTC_21M_CAP, BTC_DEFAULT_PRICE
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


def get_treasury_count():
    return Treasury.objects.count()


def get_latest_update():
    return Treasury.history.order_by("-history_date").first().history_date.date()


def get_context():
    btc_price = get_bitcoin_price()
    partial_context = {
        "etfs": get_treasury_by_type(TreasuryType.ETF.value),
        "countries": get_treasury_by_type(TreasuryType.GOVERNMENT.value),
        "public_companies": get_treasury_by_type(TreasuryType.PUBLIC.value),
        "private_companies": get_treasury_by_type(TreasuryType.PRIVATE.value),
        "miners": get_miners(),
        "defi": get_treasury_by_type(TreasuryType.DEFI.value),
    }
    context = partial_context.copy()
    treasuries_total_btc = 0
    treasuries_total_usd = 0
    treasuries_total_percentage = 0
    for treasury_type, treasuries in partial_context.items():
        total_btc = sum(treasury.btc for treasury in treasuries)
        treasuries_total_btc += total_btc
        treasuries_total_usd += btc_price * total_btc
        treasuries_total_percentage += round(total_btc * 100 / BTC_21M_CAP, 3)
        total_btc_in_usd = "{:,.0f}".format((btc_price * total_btc))
        total_percentage_from_21m = round(total_btc * 100 / BTC_21M_CAP, 3)
        total_btc = "{:,.0f}".format(total_btc)

        context[f"{treasury_type}_total"] = {
            "btc": total_btc,
            "btc_in_usd": total_btc_in_usd,
            "percentage_from_21m": total_percentage_from_21m,
        }
    treasuries_total_btc = "{:,.0f}".format(treasuries_total_btc)
    treasuries_total_usd = "{:,.0f}".format(treasuries_total_usd)
    context["btc_price"] = btc_price
    context["navbar_links"] = {
        "US ETF Tracker & Flows": "/us-etfs/",
        "Countries": "/countries/",
        "Latest Changes": "https://alerts.bitcointreasuries.com/",
        "Email Updates": "https://alerts.bitcointreasuries.com/subscribe",
        "Telegram": "https://t.me/BTCTreasuries",
    }
    context["treasury_count"] = get_treasury_count()
    context["treasuries_total_btc"] = treasuries_total_btc
    context["treasuries_total_usd"] = treasuries_total_usd
    context["treasuries_total_percentage"] = treasuries_total_percentage
    context["latest_update"] = get_latest_update()
    context["title"] = "Bitcoin Treasuries"
    return context
