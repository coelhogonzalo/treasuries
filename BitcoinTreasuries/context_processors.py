from BitcoinTreasuries.constants import BTC_21M_CAP, NAVBAR_LINKS
from treasuries.domain import (
    get_bitcoin_price,
    get_latest_updates,
    get_miners,
    get_treasury_by_type,
    get_treasury_count,
)
from treasuries.enums import TreasuryType


def calculate_totals(partial_context):
    btc_price = get_bitcoin_price()
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
    context["treasury_count"] = get_treasury_count()
    context["treasuries_total_btc"] = treasuries_total_btc
    context["treasuries_total_usd"] = treasuries_total_usd
    context["treasuries_total_percentage"] = treasuries_total_percentage
    return context


def custom_context(request):
    partial_context = {
        "etfs": get_treasury_by_type(TreasuryType.ETF.value),
        "countries": get_treasury_by_type(TreasuryType.GOVERNMENT.value),
        "public_companies": get_treasury_by_type(TreasuryType.PUBLIC.value),
        "private_companies": get_treasury_by_type(TreasuryType.PRIVATE.value),
        "miners": get_miners(),
        "defi": get_treasury_by_type(TreasuryType.DEFI.value),
    }
    context = calculate_totals(partial_context)
    context["navbar_links"] = NAVBAR_LINKS
    context["latest_updates"] = get_latest_updates()
    context["base_domain"] = request.get_host()
    return context
