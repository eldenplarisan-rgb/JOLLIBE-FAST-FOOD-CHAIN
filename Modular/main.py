import datetime

# ==================== CONFIG ====================
MENU = {
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
BULK_QTY = 5
BULK_RATE = 0.05
SENIOR_RATE = 0.20


# ==================== MENU ====================
def build_item_lookup(menu):
    """
    Flatten the nested MENU dict into a lookup keyed by item number.

    Args:
        menu (dict): {category: {item_name: price}}

    Returns:
        dict: {item_number (int): (item_name (str), price (float))}
    """
    lookup = {}
    number = 1
    for category in menu:
        for item in menu[category]:
            lookup[number] = (item, menu[category][item])
            number += 1
    return lookup


def display_menu(lookup):
    """Print the numbered menu in a bordered layout."""
    print("=" * WIDTH)
    print(STORE_NAME.center(WIDTH))
    print("=" * WIDTH)
    for number in lookup:
        name, price = lookup[number]
        print(f"{number:>2}. {name:<20} PHP {price:>6.2f}")
    print("=" * WIDTH)


# ==================== USER INPUT ====================
def ask_yes_no(prompt):
    """
    Repeat the prompt until the user answers yes or no.

    Returns:
        bool: True for yes, False for no.
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print(" Invalid choices! Please enter 'y' or 'n'.")


def get_item_and_qty(lookup):
    """
    Ask for one item number and quantity, validating both.

    Returns:
        tuple: (item_name, quantity, price)
    """
    while True:
        raw = input("Item number: ").strip()
        if raw.isdigit() and int(raw) in lookup:
            break
        print(" Invalid item number.")
    while True:
        raw_qty = input("Quantity: ").strip()
        if raw_qty.isdigit() and int(raw_qty) > 0:
            break
        print(" Invalid quantity.")
    name, price = lookup[int(raw)]
    return name, int(raw_qty), price


def take_orders(lookup):
    """
    Collect items until the user stops adding.

    Returns:
        list[tuple]: (item_name, qty, price) tuples.
    """
    orders = []
    while True:
        name, qty, price = get_item_and_qty(lookup)
        orders.append((name, qty, price))
        if not ask_yes_no("Order another item? (y/n): "):
            break
    return orders


# ==================== PRICING ====================
def compute_totals(orders, is_senior):
    """
    Calculate subtotal, discount and final total.

    Rules:
        - Senior Citizen/PWD: 20% off (takes priority).
        - Bulk order (5+ items): 5% off.
        - Otherwise no discount.

    Returns:
        tuple: (subtotal, discount, label or None, total)
    """
    subtotal = 0.0
    total_qty = 0
    for item, qty, price in orders:
        subtotal += qty * price
        total_qty += qty
    if is_senior:
        discount, label = subtotal * SENIOR_RATE, "Senior/PWD Discount (20%)"
    elif total_qty >= BULK_QTY:
        discount, label = subtotal * BULK_RATE, "Discount (5%)"
    else:
        discount, label = 0.0, None
    return subtotal, discount, label, subtotal - discount


# ==================== RECEIPT ====================
def print_receipt(orders, subtotal, discount, discount_label, total):
    """Print a formatted receipt with items, subtotal, discount and total."""
    print("\n" + "=" * WIDTH)
    print(STORE_NAME.center(WIDTH))
    print(datetime.datetime.now().strftime("%b %d, %Y %I:%M %p").center(WIDTH))
    print("-" * WIDTH)
    for item, qty, price in orders:
        print(f"{item:<16}{qty:>3} x {price:>6.2f} = {qty * price:>7.2f}")
    print("-" * WIDTH)
    print(f"{'SUBTOTAL':<25}{subtotal:>15.2f}")
    if discount_label:
        print(f"{discount_label:<25}{-discount:>15.2f}")
    print(f"{'TOTAL':<25}{total:>15.2f}")
    print("=" * WIDTH)
    print("Thank you, come again!".center(WIDTH))
    print("=" * WIDTH + "\n")


# ==================== MAIN ====================
def main():
    """Display menu, take orders, apply discounts, print receipt, repeat."""
    lookup = build_item_lookup(MENU)
    while True:
        display_menu(lookup)
        if not ask_yes_no("Order now? (y/n): "):
            print("Goodbye!")
            break
        orders = take_orders(lookup)
        is_senior = ask_yes_no("Senior Citizen/PWD? (y/n): ")
        subtotal, discount, label, total = compute_totals(orders, is_senior)
        print_receipt(orders, subtotal, discount, label, total)
        if not ask_yes_no("Would you like to order again? (y/n): "):
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()