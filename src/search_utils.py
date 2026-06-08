import re
from typing import List, Dict, Any


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Возвращает транзакции, в описании которых есть search_string (регистр не важен)."""
    if not search_string:
        return transactions
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [tx for tx in transactions if pattern.search(tx.get("description", ""))]
