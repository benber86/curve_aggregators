from .models import Route
from typing import List, Dict


def parse_exchanges(swaps: Dict):
    exchanges = {}
    for swap in swaps:
        for swap_exchange in swap['swapExchanges']:
            exchanges[swap_exchange['exchange']] = 0

    return '+'.join(exchanges.keys())


def parse_best_results(data: Dict) -> Route:
    exchange = parse_exchanges(data['priceRoute']['bestRoute'][0]['swaps'])
    amount_out = int(data['priceRoute']['destAmount'])
    return Route(exchange, amount_out)


def parse_other_results(data: Dict) -> List[Route]:
    return [Route(res['exchange'], int(res['destAmount'])) for res in data['priceRoute']['others']]


def parse_all_results(data: Dict) -> List[Route]:
    return [parse_best_results(data)] + parse_other_results(data)