"""Realistic billing logic — tests precision with structurally different code + a clear duplicate pair."""

class SubscriptionManager:
    def calculate_monthly_charge(self, plan, days_active):
        daily_rate = plan.monthly_price / 30
        charge = daily_rate * days_active
        if plan.has_discount:
            charge *= 1 - plan.discount_rate
        if charge < 0:
            charge = 0
        return round(charge, 2)

    def generate_invoice(self, customer, period_start, period_end):
        lines = []
        for sub in customer.subscriptions:
            days = (period_end - period_start).days
            charge = self.calculate_monthly_charge(sub.plan, days)
            lines.append({
                "description": sub.plan.name,
                "period_start": period_start,
                "period_end": period_end,
                "amount": charge,
            })
        total = sum(line["amount"] for line in lines)
        invoice = {
            "customer": customer.name,
            "lines": lines,
            "total": total,
            "due_date": period_end,
        }
        return invoice


class PaymentProcessor:
    def compute_transaction_fee(self, amount, method):
        if method == "credit_card":
            fee = amount * 0.029 + 0.30
        elif method == "debit_card":
            fee = amount * 0.015 + 0.25
        elif method == "ach":
            fee = 0.50
        else:
            fee = amount * 0.035
        if fee > 10:
            fee = 10
        return round(fee, 2)

    def process_payout(self, vendor, invoice_total, payment_method):
        fee = self.compute_transaction_fee(invoice_total, payment_method)
        net = invoice_total - fee
        payout = {
            "vendor": vendor.name,
            "gross": invoice_total,
            "fee": fee,
            "net": net,
            "status": "pending",
        }
        return payout


class InvoiceManager:
    def compute_credit_note(self, invoice, refund_items):
        total_refund = 0
        for item in refund_items:
            total_refund += item.amount * item.quantity
        credit = min(total_refund, invoice.total)
        if invoice.has_discount:
            credit *= 1 - invoice.discount_rate
        if credit < 0:
            credit = 0
        return round(credit, 2)

    def build_credit_memo(self, customer, credit_total):
        lines = []
        for entry in customer.credit_entries:
            amount = entry.value * entry.ratio
            lines.append({
                "description": entry.reason,
                "credit_date": entry.date,
                "amount": amount,
            })
        total = sum(line["amount"] for line in lines)
        memo = {
            "customer": customer.name,
            "lines": lines,
            "total": total,
            "valid_until": entry.date,
        }
        return memo
