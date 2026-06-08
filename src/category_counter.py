from collections import Counter
from typing import List, Dict, Any


def count_operations_by_categories(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает, сколько раз каждая категория встречается в описании транзакций.
    """
    counter: Counter = Counter()
    for tx in transactions:
        desc = tx.get("description", "").lower()
        for cat in categories:
            if cat.lower() in desc:
                counter[cat] += 1
    return {cat: counter.get(cat, 0) for cat in categories}
