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


price, vat, discount = get_user_input()
total = calculate_total(price, vat, discount)
detail = {
    "price": price,
    "vat": vat,
    "discount": discount,
    "total": total,
}
write_to_history(detail)

