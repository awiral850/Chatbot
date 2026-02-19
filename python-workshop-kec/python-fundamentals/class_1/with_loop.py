import json

def get_user_input():
    price = float(input("Enter price: "))
    vat = float(input("Enter VAT percent: "))
    discount = float(input("Enter discount percent: "))
    return price, vat, discount

def calculate_total(price, vat, discount):
    discount_amount = price * (discount / 100)
    price_after_discount = price - discount_amount
    vat_amount = price_after_discount * (vat / 100)
    total = price_after_discount + vat_amount
    return total

def write_to_history(record, filename="history.txt"):
    with open(filename, "a") as f:
        f.write(json.dumps(record) + "\n")

while True:
    try:
        n = int(input("How many transactions do you want to add? "))
    except ValueError:
        print("Please enter a valid number.")
        continue
    for i in range(n):
        print(f"\nTransaction {i+1}")
        price, vat, discount = get_user_input()
        total = calculate_total(price, vat, discount)
        detail = {
            "price": price,
            "vat": vat,
            "discount": discount,
            "total": total,
        }
        if total > 0:
            write_to_history(detail)
            print(f"Saved: {detail}")
        else:
            print("Total must be positive, not saved.")
    again = input("Do you want to add more transactions? (y/n): ").lower()
    if not again.startswith("y"):
        break
