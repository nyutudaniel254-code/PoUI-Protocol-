def calculate_poui(normalized, weights):
    scores = {}
    for symbol, m in normalized.items():
        on_chain = (m['transactions'] + m['active_wallets']) / 2
        score = (
            on_chain * weights['on_chain_activity']
            + m['value_transferred'] * weights['value_transferred']
            + m['developer_activity'] * weights['developer_activity']
        )
        scores[symbol] = round(score * 100, 2)
    return scores
