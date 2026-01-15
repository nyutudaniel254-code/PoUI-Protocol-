import json
from engine.normalizer import min_max_normalize
from engine.scorer import calculate_poui

with open('config/weights.json') as f:
    weights = json.load(f)['weights']

with open('data/raw_metrics.json') as f:
    raw = json.load(f)['metrics']

tx = {k: v['transactions_24h'] for k, v in raw.items()}
wallets = {k: v['active_wallets_24h'] for k, v in raw.items()}
value = {k: v['value_transferred_usd'] for k, v in raw.items()}
dev = {k: v['github_commits_30d'] for k, v in raw.items()}

tx_n = min_max_normalize(tx)
wallets_n = min_max_normalize(wallets)
value_n = min_max_normalize(value)
dev_n = min_max_normalize(dev)

normalized = {
    k: {
        'transactions': tx_n[k],
        'active_wallets': wallets_n[k],
        'value_transferred': value_n[k],
        'developer_activity': dev_n[k]
    }
    for k in raw
}

scores = calculate_poui(normalized, weights)
ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)

output = {
    'ranking': [
        {'rank': i + 1, 'symbol': s, 'poui_score': sc}
        for i, (s, sc) in enumerate(ranking)
    ],
    'disclaimer': 'Informational only. Not financial advice.'
}

with open('output/daily_ranking.json', 'w') as f:
    json.dump(output, f, indent=2)

print('PoUI MVP ranking generated')
