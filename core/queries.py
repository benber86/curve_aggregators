import requests
import json
from typing import Dict
from .constants import PARASWAP_API
from .models import Token


def get_rates(src_token: Token, dest_token: Token, amount: int) -> Dict:
    r = requests.get(PARASWAP_API, params={'srcToken': src_token.address,
                                            'destToken': dest_token.address,
                                            'amount': amount,
                                            'srcDecimals': src_token.decimals,
                                            'destDecimals': dest_token.decimals,
                                            'side': 'SELL',
                                            'network': 1,
                                            'otherExchangePrices': 'true',
                                            'partner': 'paraswap.io'})
    return json.loads(r.content)