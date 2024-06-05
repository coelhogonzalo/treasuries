from treasuries.enums import TreasuryType


BTC_21M_CAP = 21000000
BTC_DEFAULT_PRICE = 69000
NAVBAR_LINKS = {
    "US ETF Tracker & Flows": "/us-etfs/",
    "Countries": "/countries/",
    "Miners": "/miners/",
    "Latest Changes": "https://alerts.bitcointreasuries.com/",
    "Email Updates": "https://alerts.bitcointreasuries.com/subscribe",
    "Telegram": "https://t.me/BTCTreasuries",
}
CATEGORIES_BY_TYPE = {
    TreasuryType.ETF.value: "etfs",
    TreasuryType.GOVERNMENT.value: "countries",
    TreasuryType.PUBLIC.value: "public_companies",
    TreasuryType.PRIVATE.value: "private_companies",
    TreasuryType.DEFI.value: "defi",
}
