"""Jollibee ordering system - classes."""
import datetime


class MenuItem:
    """A single menu item with a name and price."""

    def __init__(self, name, price):
        self.name = name
        self.price = price


class Menu:
    """Holds all menu items and displays them with item numbers."""

    def __init__(self, data, store_name, width):
        self.store_name = store_name
        self.width = width
        self.items = {}  # {item_number: MenuItem}
        self._build(data)

    def _build(self, data):
        number = 1
        for category in data:
            for name, price in data[category].items():
                self.items[number] = MenuItem(name, price)
                number += 1

    def has_item(self, number):
        return number in self.items

    def get_item(self, number):
        return self.items[number]

    def display(self):
        print("=" * self.width)
        print(self.store_name.center(self.width))
        print("=" * self.width)
        for number, item in self.items.items():
            print(f"{number:>2}. {item.name:<20} PHP {item.price:>6.2f}")
        print("=" * self.width)


class OrderLine:
    """One line of an order: a menu item and its quantity."""

    def __init__(self, item, qty):
        self.item = item
        self.qty = qty

    def line_total(self):
        return self.item.price * self.qty


class Order:
    """A customer's order. Computes subtotal, discount and total."""

    BULK_QTY = 5
    BULK_RATE = 0.05
    SENIOR_RATE = 0.20

    def __init__(self):
        self.lines = []
        self.is_senior = False

    def add_line(self, item, qty):
        self.lines.append(OrderLine(item, qty))

    def total_quantity(self):
        return sum(line.qty for line in self.lines)

    def subtotal(self):
        return sum(line.line_total() for line in self.lines)

    def discount_info(self):
        """Return (discount_amount, label or None).
        Senior/PWD (20%) has priority over bulk (5%)."""
        if self.is_senior:
            return self.subtotal() * self.SENIOR_RATE, "Senior/PWD Discount (20%)"
        if self.total_quantity() >= self.BULK_QTY:
            return self.subtotal() * self.BULK_RATE, "Discount (5%)"
        return 0.0, None

    def total(self):
        return self.subtotal() - self.discount_info()[0]


class Receipt:
    """Prints a formatted receipt for an Order."""

    def __init__(self, store_name, width):
        self.store_name = store_name
        self.width = width

    def print(self, order):
        w = self.width
        discount, label = order.discount_info()
        print("\n" + "=" * w)
        print(self.store_name.center(w))
        print(datetime.datetime.now().strftime("%b %d, %Y %I:%M %p").center(w))
        print("-" * w)
        for line in order.lines:
            print(f"{line.item.name:<16}{line.qty:>3} x "
                  f"{line.item.price:>6.2f} = {line.line_total():>7.2f}")
        print("-" * w)
        print(f"{'SUBTOTAL':<25}{order.subtotal():>15.2f}")
        if label:
            print(f"{label:<25}{-discount:>15.2f}")
        print(f"{'TOTAL':<25}{order.total():>15.2f}")
        print("=" * w)
        print("Thank you, come again!".center(w))
        print("=" * w + "\n")


class OrderingApp:
    """Controls the whole program: input handling and the main loop."""

    MENU_DATA = {
        "Burgers": {
            "Aloha Yumburger": 95.00,
            "Big Mac Burger": 149.00,
            "McChicken Sandwich": 119.00
        },
        "Sides": {
            "Jolly Spaghetti": 89.00,
            "Chickenjoy Bucket (1pc)": 105.00
        },
        "Drinks": {
            "Coke Float": 49.00,
            "Pineapple Juice": 55.00,
            "Sundae Cone": 35.00
        },
    }
    STORE_NAME = "JOLLIBEE FAST FOOD CHAIN"
    WIDTH = 40

    def __init__(self):
        self.menu = Menu(self.MENU_DATA, self.STORE_NAME, self.WIDTH)
        self.receipt = Receipt(self.STORE_NAME, self.WIDTH)

    @staticmethod
    def ask_yes_no(prompt):
        while True:
            answer = input(prompt).strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print(" Invalid choices! Please enter 'y' or 'n'.")

    def get_item_and_qty(self):
        while True:
            raw = input("Item number: ").strip()
            if raw.isdigit() and self.menu.has_item(int(raw)):
                break
            print(" Invalid item number.")
        while True:
            raw_qty = input("Quantity: ").strip()
            if raw_qty.isdigit() and int(raw_qty) > 0:
                break
            print(" Invalid quantity.")
        return self.menu.get_item(int(raw)), int(raw_qty)

    def take_order(self):
        order = Order()
        while True:
            item, qty = self.get_item_and_qty()
            order.add_line(item, qty)
            if not self.ask_yes_no("Order another item? (y/n): "):
                break
        order.is_senior = self.ask_yes_no("Senior Citizen/PWD? (y/n): ")
        return order

    def run(self):
        while True:
            self.menu.display()
            if not self.ask_yes_no("Order now? (y/n): "):
                print("Goodbye!")
                break
            order = self.take_order()
            self.receipt.print(order)
            if not self.ask_yes_no("Would you like to order again? (y/n): "):
                print("Goodbye!")
                break