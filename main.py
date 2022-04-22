from itertools import permutations
from typing import List

from core.constants import TOKENS
from core.models import Trade, Record, PreRecord, session
from core.parsing import parse_all_results
from core.queries import get_rates

pairs = permutations(TOKENS, 2)
amounts = [1000, 10000, 100000]

if __name__ == "__main__":

    for pair in pairs:
        for amount in amounts:
            pair_label = '/'.join([token.symbol for token in pair])
            print(f"Handling pair: {pair_label} for amount: {amount}")

            current_trade = Trade(pair_label, amount)
            session.add(current_trade)

            api_data = get_rates(pair[0], pair[1], amount * pair[0].decimals)
            routes = parse_all_results(api_data)

            ordered_routes = sorted(routes, key=lambda d: d.amount_out, reverse=True)
            best_amount = ordered_routes[0].amount_out

            records: List[PreRecord] = []
            for i, route in enumerate(ordered_routes):
                records.append(PreRecord(route.exchange,
                                         route.amount_out,
                                         i,
                                         (1 - route.amount_out / best_amount) * 100))
                if 'Curve' in route.exchange and '+' not in route.exchange:
                    feeless_amount = route.amount_out * 1.0003
                    records.append(PreRecord('Curve Feeless',
                                             int(feeless_amount),
                                             -1,
                                             (1 - feeless_amount / best_amount) * 100))

            ordered_records = sorted(records, key=lambda d: d.amount_out, reverse=True)
            for i, record in enumerate(ordered_records):
                db_record = Record(exchange=record.exchange,
                                   amount_out=record.amount_out,
                                   rank=i,
                                   original_rank=record.rank,
                                   loss_pct=record.loss_pct)
                session.add(db_record)

            session.commit()