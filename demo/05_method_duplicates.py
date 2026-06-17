"""Cross-class method duplicates — methods with same pattern in different classes."""

class ShoppingCart:
    def get_subtotal(self):
        total = 0
        for item in self.items:
            total += item.price * item.qty
        return total

    def get_tax(self, rate):
        sub = self.get_subtotal()
        return sub * rate


class Invoice:
    def compute_total(self):
        total = 0
        for line in self.lines:
            total += line.unit_price * line.count
        return total

    def compute_vat(self, percent):
        base = self.compute_total()
        return base * percent
