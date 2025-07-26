import datetime
from typing import Any, Dict, List

def call_promotions_api() -> List[Dict[str, Any]]:
    return [
        {
            "promotion_id": "PROMO001",
            "name": "Weekend Special",
            "discount": "10% off",
            "products": ["P002"],
            "start_date": datetime.date(2024, 1, 12),
            "end_date": datetime.date(2024, 1, 14),
        },
        {
            "promotion_id": "PROMO002",
            "name": "Flash Sale",
            "discount": "15% off",
            "products": ["P001", "P003", "P005"],
            "start_date": datetime.date(2024, 1, 15),
            "end_date": datetime.date(2024, 1, 16),
        },
    ]