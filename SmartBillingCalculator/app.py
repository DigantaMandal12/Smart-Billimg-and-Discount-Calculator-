import os
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB request payload limit

# Demonstration rates for this academic project only (PCC-CS393).
# These are configurable sample rules, not official tax guidance.
TAX_RATE = Decimal("0.05")
DISCOUNT_SLABS = (
    (Decimal("5000.00"), Decimal("0.10")),
    (Decimal("2500.00"), Decimal("0.05")),
)

MAX_ITEMS = 50
MAX_NAME_LENGTH = 80
MAX_PRICE = Decimal("100000000.00")
MAX_QUANTITY = 100000


def money(value: Decimal) -> Decimal:
    """Round currency values consistently to two decimal places using ROUND_HALF_UP."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_discount_rate(subtotal: Decimal) -> Decimal:
    """Return the applicable demonstration discount rate based on the subtotal."""
    for minimum, rate in DISCOUNT_SLABS:
        if subtotal >= minimum:
            return rate
    return Decimal("0.00")


def parse_item_row(raw_name: str, raw_price: str, raw_quantity: str, row_number: int | None = None) -> dict:
    """Validate and convert raw form strings for a single product row."""
    prefix = f"Row {row_number}: " if row_number is not None else ""

    if raw_name is None:
        raise ValueError(f"{prefix}Every product needs a name.")
    name = str(raw_name).strip()
    if not name:
        raise ValueError(f"{prefix}Every product needs a name.")
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"{prefix}Product names must be {MAX_NAME_LENGTH} characters or fewer.")

    if raw_price is None or not str(raw_price).strip():
        raise ValueError(f"{prefix}Enter a valid price for every product.")
    try:
        price = Decimal(str(raw_price).strip())
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"{prefix}Enter a valid price for every product.")

    if not price.is_finite() or price < Decimal("0.00"):
        raise ValueError(f"{prefix}Price must be a valid non-negative number.")
    if price > MAX_PRICE:
        raise ValueError(f"{prefix}Price is too large for this demo (maximum ₹10,00,00,000.00).")

    if raw_quantity is None or not str(raw_quantity).strip():
        raise ValueError(f"{prefix}Enter a whole-number quantity for every product.")
    try:
        quantity_decimal = Decimal(str(raw_quantity).strip())
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"{prefix}Enter a whole-number quantity for every product.")

    if not quantity_decimal.is_finite() or quantity_decimal != quantity_decimal.to_integral_value():
        raise ValueError(f"{prefix}Quantity must be a whole number.")

    quantity = int(quantity_decimal)
    if quantity < 1 or quantity > MAX_QUANTITY:
        raise ValueError(f"{prefix}Quantity must be between 1 and {MAX_QUANTITY}.")

    return {
        "name": name,
        "price": price,
        "quantity": quantity,
    }


def calculate_bill(items: list[dict]) -> dict:
    """Calculate line totals, subtotal, discount, sample tax, and final payable amount."""
    if not items:
        raise ValueError("Please add at least one product.")
    if len(items) > MAX_ITEMS:
        raise ValueError(f"You can add up to {MAX_ITEMS} products per bill.")

    normalized_items = []
    subtotal = Decimal("0.00")

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Invalid product record.")

        raw_name = item.get("name", "")
        raw_price = item.get("price", "")
        raw_quantity = item.get("quantity", "")

        name = str(raw_name).strip() if raw_name is not None else ""
        if not name:
            raise ValueError("Product name is required.")
        if len(name) > MAX_NAME_LENGTH:
            raise ValueError(f"Product names must be {MAX_NAME_LENGTH} characters or fewer.")

        try:
            price = Decimal(str(raw_price).strip())
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Price must be a valid non-negative number.")

        if not price.is_finite() or price < Decimal("0.00"):
            raise ValueError("Price must be a valid non-negative number.")
        if price > MAX_PRICE:
            raise ValueError("Price is too large for this demo.")

        try:
            qty_dec = Decimal(str(raw_quantity).strip())
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Quantity must be a whole number.")

        if not qty_dec.is_finite() or qty_dec != qty_dec.to_integral_value():
            raise ValueError("Quantity must be a whole number.")

        quantity = int(qty_dec)
        if quantity < 1 or quantity > MAX_QUANTITY:
            raise ValueError(f"Quantity must be between 1 and {MAX_QUANTITY}.")

        rounded_price = money(price)
        line_total = money(rounded_price * quantity)
        subtotal += line_total

        normalized_items.append({
            "name": name,
            "price": rounded_price,
            "quantity": quantity,
            "line_total": line_total,
        })

    subtotal = money(subtotal)
    discount_rate = get_discount_rate(subtotal)
    discount = money(subtotal * discount_rate)
    taxable_amount = money(subtotal - discount)
    tax = money(taxable_amount * TAX_RATE)
    total = money(taxable_amount + tax)

    return {
        "items": normalized_items,
        "item_count": len(normalized_items),
        "total_units": sum(i["quantity"] for i in normalized_items),
        "subtotal": subtotal,
        "discount_rate": discount_rate,
        "discount_percent": int(discount_rate * 100),
        "discount": discount,
        "taxable_amount": taxable_amount,
        "tax_rate": TAX_RATE,
        "tax_percent": int(TAX_RATE * 100),
        "tax": tax,
        "total": total,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    bill = None
    error = None
    form_items = [{"name": "", "price": "", "quantity": "1"}]

    if request.method == "POST":
        names = request.form.getlist("item_name[]")
        prices = request.form.getlist("price[]")
        quantities = request.form.getlist("quantity[]")

        # Keep whatever the user entered so valid fields are not lost on error
        max_len = max(len(names), len(prices), len(quantities))
        if max_len > 0:
            form_items = [
                {
                    "name": names[i] if i < len(names) else "",
                    "price": prices[i] if i < len(prices) else "",
                    "quantity": quantities[i] if i < len(quantities) else "1",
                }
                for i in range(min(max_len, MAX_ITEMS))
            ]

        if not names or not prices or not quantities or not (len(names) == len(prices) == len(quantities)):
            error = "Please provide at least one complete product row."
        elif len(names) > MAX_ITEMS:
            error = f"You can add up to {MAX_ITEMS} products per bill."
        else:
            try:
                parsed_items = [
                    parse_item_row(n, p, q, idx + 1)
                    for idx, (n, p, q) in enumerate(zip(names, prices, quantities))
                ]
                bill = calculate_bill(parsed_items)
            except (ValueError, InvalidOperation, TypeError, OverflowError) as exc:
                error = str(exc) or "Please check the entered values."

    return render_template(
        "index.html",
        bill=bill,
        error=error,
        form_items=form_items,
        tax_rate_percent=int(TAX_RATE * 100),
    )


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


@app.errorhandler(413)
def request_too_large(_error):
    return (
        render_template(
            "index.html",
            bill=None,
            error="Request too large. Please submit a smaller bill (up to 50 items).",
            form_items=[{"name": "", "price": "", "quantity": "1"}],
            tax_rate_percent=int(TAX_RATE * 100),
        ),
        413,
    )


@app.errorhandler(500)
def internal_server_error(_error):
    return (
        render_template(
            "index.html",
            bill=None,
            error="An unexpected server error occurred. Please verify your inputs and try again.",
            form_items=[{"name": "", "price": "", "quantity": "1"}],
            tax_rate_percent=int(TAX_RATE * 100),
        ),
        500,
    )


if __name__ == "__main__":
    # Enable debug mode only when FLASK_DEBUG=1 is explicitly set in local development.
    # Never enable debug mode in a production deployment.
    debug_mode = os.environ.get("FLASK_DEBUG", "0").strip().lower() in ("1", "true", "yes")
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
