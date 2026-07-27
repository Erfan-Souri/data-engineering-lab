import random
import uuid
from datetime import datetime, timezone


def generate_order_created():
    """
    Generate a fake ORDER_CREATED event.
    """

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "ORDER_CREATED",
        "order_id": random.randint(1000, 9999),
        "customer_id": random.randint(1, 100),
        "amount": round(random.uniform(10, 500), 2),
        "currency": "USD",
        "created_at": datetime.now(timezone.utc).isoformat()
    }