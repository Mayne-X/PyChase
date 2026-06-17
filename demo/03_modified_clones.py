"""Modified structure — Type-3. Similar but with extra/missing statements."""

def process_orders_a(orders, rate):
    total = 0
    for order in orders:
        total += order.amount * rate
    discount = total * 0.1
    return total - discount


def process_orders_b(orders, rate, coupon):
    total = 0
    for order in orders:
        total += order.amount * rate
    discount = total * 0.1
    total -= discount
    if coupon:
        total *= 0.95
    return total
