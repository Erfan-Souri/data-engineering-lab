import random
import uuid
from datetime import datetime, timezone

# Active orders currently being processed
orders = {}

# Next order id
next_order_id = 1000

# Order lifecycle
NEXT_STATUS = {
    "ORDER_CREATED": "ORDER_PAID",
    "ORDER_PAID": "ORDER_SHIPPED",
    "ORDER_SHIPPED": "ORDER_DELIVERED",
}


def now():
    return datetime.now(timezone.utc).isoformat()


def create_order():
    global next_order_id

    next_order_id += 1

    order = {
        "order_id": next_order_id,
        "customer_id": random.randint(1, 100),
        "amount": round(random.uniform(10, 500), 2),
        "currency": random.choice(["USD", "EUR", "GBP"]),
        "status": "ORDER_CREATED",
        "version": 1,
    }

    orders[next_order_id] = order

    return build_event(order)


def progress_order():
    if not orders:
        return create_order()

    order_id = random.choice(list(orders.keys()))
    order = orders[order_id]

    current_status = order["status"]

    if current_status == "ORDER_CREATED":

        # 10% chance of cancellation
        if random.random() < 0.10:
            order["status"] = "ORDER_CANCELLED"

        else:
            order["status"] = "ORDER_PAID"

    elif current_status == "ORDER_PAID":
        order["status"] = "ORDER_SHIPPED"

    elif current_status == "ORDER_SHIPPED":
        order["status"] = "ORDER_DELIVERED"

    order["version"] += 1

    event = build_event(order)

    # Remove completed orders from memory
    if order["status"] in ("ORDER_DELIVERED", "ORDER_CANCELLED"):
        del orders[order_id]

    return event


def build_event(order):
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": order["status"],
        "order_id": order["order_id"],
        "customer_id": order["customer_id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "version": order["version"],
        "created_at": now(),
    }


def generate_event():
    """
    Generate the next event produced by the Order Service.
    """

    if not orders:
        return create_order()

    if random.random() < 0.70:
        return create_order()

    return progress_order()