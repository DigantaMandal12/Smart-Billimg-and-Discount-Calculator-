import unittest
from decimal import Decimal
from app import app, calculate_bill, get_discount_rate


class BillingLogicTests(unittest.TestCase):
    """Unit tests for core Decimal calculation, discount slabs, and server-side validation."""

    def test_01_normal_bill_calculates_correctly(self):
        """Test 2 & 3: A normal bill below ₹2,500 calculates line total, 0% discount, 5% tax, and final total."""
        bill = calculate_bill([{"name": "Pen", "price": "100", "quantity": 2}])
        self.assertEqual(bill["subtotal"], Decimal("200.00"))
        self.assertEqual(bill["discount_rate"], Decimal("0.00"))
        self.assertEqual(bill["discount"], Decimal("0.00"))
        self.assertEqual(bill["tax"], Decimal("10.00"))
        self.assertEqual(bill["total"], Decimal("210.00"))

    def test_02_subtotal_below_2500_receives_no_discount(self):
        """Test 3: Subtotal just below ₹2,500 (₹2,499.99) receives 0% discount."""
        bill = calculate_bill([{"name": "Keyboard", "price": "2499.99", "quantity": 1}])
        self.assertEqual(bill["subtotal"], Decimal("2499.99"))
        self.assertEqual(bill["discount_rate"], Decimal("0.00"))
        self.assertEqual(bill["discount"], Decimal("0.00"))
        self.assertEqual(bill["tax"], Decimal("125.00"))
        self.assertEqual(bill["total"], Decimal("2624.99"))

    def test_03_subtotal_exactly_2500_receives_five_percent_discount(self):
        """Test 4: Subtotal of exactly ₹2,500 receives 5% discount."""
        bill = calculate_bill([{"name": "Book Set", "price": "2500", "quantity": 1}])
        self.assertEqual(bill["subtotal"], Decimal("2500.00"))
        self.assertEqual(bill["discount_rate"], Decimal("0.05"))
        self.assertEqual(bill["discount"], Decimal("125.00"))
        self.assertEqual(bill["tax"], Decimal("118.75"))
        self.assertEqual(bill["total"], Decimal("2493.75"))

    def test_04_subtotal_just_below_5000_receives_five_percent_discount(self):
        """Test 5: Subtotal just below ₹5,000 (₹4,999.99) receives 5% discount."""
        bill = calculate_bill([{"name": "Monitor Stand", "price": "4999.99", "quantity": 1}])
        self.assertEqual(bill["subtotal"], Decimal("4999.99"))
        self.assertEqual(bill["discount_rate"], Decimal("0.05"))
        self.assertEqual(bill["discount"], Decimal("250.00"))
        self.assertEqual(bill["tax"], Decimal("237.50"))
        self.assertEqual(bill["total"], Decimal("4987.49"))

    def test_05_subtotal_exactly_5000_receives_ten_percent_discount(self):
        """Test 6: Subtotal of exactly ₹5,000 receives 10% discount."""
        bill = calculate_bill([{"name": "Lab Kit", "price": "5000", "quantity": 1}])
        self.assertEqual(bill["subtotal"], Decimal("5000.00"))
        self.assertEqual(bill["discount_rate"], Decimal("0.10"))
        self.assertEqual(bill["discount"], Decimal("500.00"))
        self.assertEqual(bill["tax"], Decimal("225.00"))
        self.assertEqual(bill["total"], Decimal("4725.00"))

    def test_06_multiple_products_calculate_correctly(self):
        """Test 7: Multiple products sum line totals accurately."""
        bill = calculate_bill([
            {"name": "Pen", "price": "10", "quantity": 3},
            {"name": "Notebook", "price": "100", "quantity": 2},
            {"name": "Calculator", "price": "1200.50", "quantity": 2},
        ])
        self.assertEqual(bill["subtotal"], Decimal("2631.00"))
        self.assertEqual(len(bill["items"]), 3)
        self.assertEqual(bill["discount_rate"], Decimal("0.05"))
        self.assertEqual(bill["discount"], Decimal("131.55"))
        self.assertEqual(bill["tax"], Decimal("124.97"))
        self.assertEqual(bill["total"], Decimal("2624.42"))

    def test_07_reject_negative_price(self):
        """Test 8: Negative prices are rejected."""
        with self.assertRaises(ValueError):
            calculate_bill([{"name": "Pen", "price": "-1", "quantity": 1}])

    def test_08_reject_empty_name(self):
        """Test 9: Empty or whitespace-only product names are rejected."""
        with self.assertRaises(ValueError):
            calculate_bill([{"name": "   ", "price": "10", "quantity": 1}])

    def test_09_reject_zero_and_negative_quantity(self):
        """Test 10: Zero or negative quantities are rejected."""
        with self.assertRaises(ValueError):
            calculate_bill([{"name": "Pen", "price": "10", "quantity": 0}])
        with self.assertRaises(ValueError):
            calculate_bill([{"name": "Pen", "price": "10", "quantity": -5}])

    def test_10_reject_fractional_quantity(self):
        """Test 11: Fractional quantities are rejected."""
        with self.assertRaises(ValueError):
            calculate_bill([{"name": "Pen", "price": "10", "quantity": "1.5"}])

    def test_11_reject_invalid_numeric_input(self):
        """Test 12: Non-numeric or NaN/Infinity prices are rejected."""
        with self.assertRaises(ValueError):
            calculate_bill([{"name": "Pen", "price": "abc", "quantity": 1}])
        with self.assertRaises(ValueError):
            calculate_bill([{"name": "Pen", "price": "NaN", "quantity": 1}])

    def test_12_reject_empty_and_excessive_items(self):
        """Empty item lists and more than 50 rows are rejected."""
        with self.assertRaises(ValueError):
            calculate_bill([])
        with self.assertRaises(ValueError):
            calculate_bill([{"name": f"Item {i}", "price": "10", "quantity": 1} for i in range(51)])

    def test_13_get_discount_rate_boundaries(self):
        """Verify exact slab boundary helper values."""
        self.assertEqual(get_discount_rate(Decimal("0.00")), Decimal("0.00"))
        self.assertEqual(get_discount_rate(Decimal("2499.99")), Decimal("0.00"))
        self.assertEqual(get_discount_rate(Decimal("2500.00")), Decimal("0.05"))
        self.assertEqual(get_discount_rate(Decimal("4999.99")), Decimal("0.05"))
        self.assertEqual(get_discount_rate(Decimal("5000.00")), Decimal("0.10"))


class WebRouteTests(unittest.TestCase):
    """Integration tests using Flask's test client for HTTP routes and Jinja template rendering."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_14_homepage_returns_http_200(self):
        """Test 1: Homepage GET request returns HTTP 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Smart Billing", response.data)

    def test_15_post_bill_renders_without_jinja_items_typeerror(self):
        """Test 14: POST renders bill['items'] cleanly without 'builtin_function_or_method' TypeError."""
        response = self.client.post("/", data={
            "item_name[]": ["Engineering Drawing Box", "Scientific Calculator"],
            "price[]": ["1500.00", "1200.00"],
            "quantity[]": ["1", "1"],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Engineering Drawing Box", response.data)
        self.assertIn(b"Scientific Calculator", response.data)
        self.assertIn(b"2700.00", response.data)  # Subtotal
        self.assertIn(b"135.00", response.data)   # 5% Discount
        self.assertIn(b"128.25", response.data)   # 5% Sample Tax
        self.assertIn(b"2693.25", response.data)  # Final Payable Amount

    def test_16_post_rejects_negative_price_and_retains_input(self):
        """Test 8 (HTTP): Negative price shows user-friendly error and retains entered product name."""
        response = self.client.post("/", data={
            "item_name[]": ["Graphing Notebook"],
            "price[]": ["-50"],
            "quantity[]": ["2"],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Price must be a valid non-negative number", response.data)
        self.assertIn(b"Graphing Notebook", response.data)

    def test_17_post_rejects_empty_name(self):
        """Test 9 (HTTP): Empty product name shows user-friendly error."""
        response = self.client.post("/", data={
            "item_name[]": ["   "],
            "price[]": ["100"],
            "quantity[]": ["1"],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Every product needs a name", response.data)

    def test_18_post_rejects_zero_quantity(self):
        """Test 10 (HTTP): Zero quantity shows user-friendly error."""
        response = self.client.post("/", data={
            "item_name[]": ["Pen"],
            "price[]": ["20"],
            "quantity[]": ["0"],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Quantity must be between 1 and 100000", response.data)

    def test_19_post_rejects_fractional_quantity(self):
        """Test 11 (HTTP): Fractional quantity shows user-friendly error."""
        response = self.client.post("/", data={
            "item_name[]": ["Pen"],
            "price[]": ["10"],
            "quantity[]": ["1.5"],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Quantity must be a whole number", response.data)

    def test_20_post_rejects_invalid_numeric_input(self):
        """Test 12 (HTTP): Non-numeric price or quantity shows user-friendly error."""
        response = self.client.post("/", data={
            "item_name[]": ["Pen"],
            "price[]": ["not-a-number"],
            "quantity[]": ["1"],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Enter a valid price", response.data)

    def test_21_post_handles_missing_or_mismatched_form_fields_safely(self):
        """Test 13 (HTTP): Missing or mismatched form fields do not crash the server."""
        response_empty = self.client.post("/", data={})
        self.assertEqual(response_empty.status_code, 200)
        self.assertIn(b"Please provide at least one complete product row", response_empty.data)

        response_mismatch = self.client.post("/", data={
            "item_name[]": ["Pen", "Book"],
            "price[]": ["10"],
            "quantity[]": ["1"],
        })
        self.assertEqual(response_mismatch.status_code, 200)
        self.assertIn(b"Please provide at least one complete product row", response_mismatch.data)

    def test_22_custom_404_page(self):
        """Verify unknown URLs render custom 404.html with HTTP 404."""
        response = self.client.get("/non-existent-route")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Page Not Found", response.data)


if __name__ == "__main__":
    unittest.main()
