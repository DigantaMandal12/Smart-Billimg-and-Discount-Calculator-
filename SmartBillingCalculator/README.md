# Smart Billing & Discount Calculator

**Live Web Demo:** <https://smartbillingcalculator.vercel.app/>

**Academic Information**

* **Institution:** Budge Budge Institute of Technology, Kolkata

* **Department:** Computer Science & Engineering

* **Course:** IT Workshop (Python Programming) Mini Project (PCC-CS393)

* **Academic Year:** 2026–2027

* **Group Number:** 2

* **Group Members:** Bitan Chowdhury, Ayush Pandey, Diganta Mandal, Surya Kunti

## 1. Live Application & Project Overview

The Smart Billing & Discount Calculator is a Python billing solution designed to generate accurate, itemized customer bills while eliminating manual calculation errors. It accepts product details, calculates individual line amounts and the subtotal, applies tiered discounts according to predefined slabs, calculates GST/tax on the discounted amount, and displays the final payable amount.

This repository supports both execution modes documented for our Group 2 (PCC-CS393) mini-project:

* **Flask Web Application** (`app.py` — Live at smartbillingcalculator.vercel.app): A responsive Python + Flask web dashboard with dynamic multi-product entry (up to 50 items), Decimal (`ROUND_HALF_UP`) currency precision, server-side input validation, and a print-ready invoice layout (`@media print`).

* **Menu-Driven Console Application** (`10_CSE.py` specification): Accepts customer name, multiple product rows, and a user-entered GST percentage (0 to 100), validates inputs, displays a formatted receipt, and saves each bill to `receipts/receipt_<bill_id>.txt` using Python's standard `datetime` and `os` modules.

## 2. Problem Statement

Manual bill calculation can lead to arithmetic mistakes and makes it difficult to apply tiered discounts and taxes consistently across multiple items. This project provides a Python-based billing system that automates product line totals, subtotal, discount slab selection, GST/tax, and final payable amount calculations while validating common input errors.

## 3. Objectives

* Accept customer/order details and one or more product entries.

* Calculate the line amount for each product using unit price and quantity.

* Calculate the subtotal using exact arithmetic operations.

* Apply a tiered discount based on the configured subtotal slabs.

* Calculate GST/sample tax on the discounted amount and compute the final payable amount.

* Validate blank names, non-numeric text, zero/negative values, fractional quantities, and out-of-range inputs.

* Display a clean formatted receipt (print-ready in the web interface and saved to `receipts/receipt_<bill_id>.txt` in the console specification).

* Demonstrate core Python concepts: functions, loops, lists, dictionaries, arithmetic & comparison operators, conditional statements (if/elif/else), Decimal precision, and try/except exception handling.

## 4. Main Features & Discount Calculation Rules

* **Multiple Products:** Add up to 50 product items in a single bill, with interactive row addition and removal.

* **Automatic Line & Subtotal Calculation:** Computes each item's line amount (Unit Price × Quantity) and sums all items into the subtotal.

* **GST / Sample Tax Calculator:** Calculates tax on the taxable amount after discount (Subtotal - Discount). Uses a configurable 5% sample tax rate in `app.py` (or a user-entered GST percentage from 0 to 100 in the console workflow).

* **Strict Input Validation:** Rejects blank product names, non-numeric prices/quantities, negative prices, zero or negative quantities, fractional quantities, and out-of-range inputs while preserving entered values on form errors.

* **Receipt Generation:** Displays an itemized bill summary with a single-click print stylesheet and supports saving text receipts.

**Tiered Discount Calculator (Demonstration Slabs):**

| Subtotal Range | Applicable Discount Rate | 
| ----- | ----- | 
| Rs. 5,000.00 or more (`>= 5000`) | 10% Discount | 
| Rs. 2,500.00 to Rs. 4,999.99 (`>= 2500` and `< 5000`) | 5% Discount | 
| Below Rs. 2,500.00 (`< 2500`) | 0% Discount | 

## 5. Sample Execution Walkthrough

**Example Input (from Group 2 Project Report):**

* **Customer:** Riya Das

* **Product:** Notebook

* **Unit Price:** Rs. 100.00

* **Quantity:** 30

* **GST / Tax Rate:** 5%

**Step-by-Step Calculation:**

1. **Subtotal:** 100 × 30 = Rs. 3,000.00

2. **Eligible Discount Rate:** 5% (since Subtotal is between Rs. 2,500.00 and Rs. 4,999.99)

3. **Discount Amount:** 5% of 3,000.00 = Rs. 150.00

4. **Taxable Amount (After Discount):** 3,000.00 - 150.00 = Rs. 2,850.00

5. **GST / Tax (5% of Rs. 2,850.00):** Rs. 142.50

6. **Final Payable Amount:** 2,850.00 + 142.50 = Rs. 2,992.50

## 6. Data Structures and Python Concepts Used

| Concept | Use in Project | 
| ----- | ----- | 
| **List (`list`)** | Stores all product records (`items` / `form_items`) in a single bill. | 
| **Dictionary (`dict`)** | Stores each product's name, price, quantity, and `line_total`, as well as the overall bill summary. | 
| **Functions (`def`)** | Separates currency rounding (`money`), slab lookup (`get_discount_rate`), row validation (`parse_item_row`), bill calculation (`calculate_bill`), and HTTP route handling (`index`). | 
| **Arithmetic Operators** | Performs multiplication (`price * quantity`), addition, subtraction (`subtotal - discount`), and percentage calculations. | 
| **Comparison Operators** | Checks discount slab eligibility (`>=`, `<`) and valid numeric ranges. | 
| **Conditional Statements (`if`/`elif`/`else`)** | Selects discount slabs and validates form submissions. | 
| **Loops (`for`)** | Iterates through submitted product rows and renders itemized table rows in Jinja2 (`{% for item in bill["items"] %}`). | 
| **Exception Handling (`try`/`except`)** | Catches `InvalidOperation`, `ValueError`, and `TypeError` to handle invalid numeric inputs gracefully without crashing. | 
| **Exact Decimal Math (`decimal.Decimal`)** | Ensures exact base-10 two-decimal rounding (`ROUND_HALF_UP`) for all currency figures. | 

## 7. Project Folder Structure

```
SmartBillingCalculator/
├── app.py                  # Flask backend, Decimal billing engine, validation, and error handlers
├── requirements.txt        # Python package dependencies (Flask>=3.0.0,<4.0.0)
├── vercel.json             # Vercel serverless deployment configuration
├── README.md               # Group 2 (PCC-CS393) project documentation and setup guide
├── .gitignore              # Excludes .venv, __pycache__, and temporary logs
├── templates/
│   ├── base.html           # Shared HTML5 layout shell, header, and footer
│   ├── index.html          # Billing form, itemized bill summary table, and discount rules
│   └── 404.html            # Custom HTTP 404 Page Not Found template
├── static/
│   ├── style.css           # Responsive green-and-white theme and @media print stylesheet
│   └── script.js           # Safe DOM row addition/removal and print button handler
├── tests/
│   └── test_app.py         # 22-test automated unittest suite (logic + HTTP routes)
└── report/
    └── REPORT_DRAFT.md     # Complete college mini-project report draft

```

## 8. How to Upload / Push This Project to GitHub from a Mobile Browser

If you are using a phone (Chrome, Safari, Brave, or Edge on Android/iOS) without a PC or Git CLI installed:

1. **Unzip the archive on your phone:** Download `SmartBillingCalculator.zip` and tap *Extract* in your phone's Files app so all files are extracted.

2. **Switch your mobile browser to Desktop Site:** Open github.com in your mobile browser, tap the browser menu, and enable *Desktop site* (GitHub's file uploader supports folder/multi-file selection much better in Desktop view).

3. **Create or open your repository:** Tap *New*, name it `SmartBillingCalculator`, check *Add a README file*, and tap *Create repository*.

4. **Upload root files first:** Tap *Add file* -> *Upload files* -> choose your files, select `app.py`, `requirements.txt`, `vercel.json`, `README.md`, and `.gitignore`, and tap *Commit changes*.

5. **Create subfolder files on mobile:**

   * Because mobile browsers cannot drag-and-drop folders, tap *Add file* -> *Create new file*.

   * In the filename box at the top, type `templates/base.html` (typing `/` automatically creates the templates folder), paste the code for `base.html`, and tap *Commit changes*.

   * Repeat for all other files inside the `templates/`, `static/`, `tests/`, and `report/` directories.

## 9. Local Setup & Installation (Windows PowerShell)

* **Language:** Python 3.10 or later (compatible with Python 3.11–3.15.x)

* **Web Framework:** Flask 3.x (Flask>=3.0.0,<4.0.0)

**Step 1: Open the Project Folder**

```
cd path\to\SmartBillingCalculator

```

**Step 2: Create and Activate a Virtual Environment**

```
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1

```

*(If PowerShell blocks script execution, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first, then try activating again.)*

**Step 3: Install Dependencies and Run the Flask Web App**

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py

```

Open `http://127.0.0.1:5000` in your browser.

**Step 4: Run Automated Tests**

```
python -m unittest discover -s tests -v

```

## 10. Test Cases Summary

| Test # | Input / Action | Expected Result | 
| ----- | ----- | ----- | 
| 1 | Generate a bill with valid product details (e.g., Notebook, Rs. 100 × 30, 5% tax) | Itemized bill generated (Subtotal: Rs. 3,000.00, Discount: Rs. 150.00, Tax: Rs. 142.50, Final: Rs. 2,992.50) | 
| 2 | Enter letters for price (e.g., "abc") | Validation error message displayed; entered values retained | 
| 3 | Enter quantity as 0, negative (-5), or fractional (1.5) | Quantity rejected with clear validation error message | 
| 4 | Leave product name blank ("   ") | Blank input rejected ("Every product needs a name.") | 
| 5 | Subtotal below Rs. 2,500 (e.g., Rs. 2,000.00 or Rs. 2,499.99) | 0% discount applied | 
| 6 | Subtotal from Rs. 2,500 to Rs. 4,999.99 (e.g., Rs. 2,500.00 or Rs. 3,000.00) | 5% discount applied | 
| 7 | Subtotal of Rs. 5,000 or more (e.g., Rs. 5,000.00) | 10% discount applied | 
| 8 | Render multi-item bill in Jinja2 (`bill["items"]`) | Renders cleanly without `builtin_function_or_method` TypeError | 

## 11. Limitations & Future Enhancements

**Limitations**

* Operates as a stateless academic web/console application without a central product database or inventory system.

* Discount slabs and tax rates are demonstration rules and should be adjusted if the instructor specifies different rates.

* No customer login or role-based administrator authentication is included.

**Future Enhancements**

* Use SQLite to store customer, product, and historical invoice records permanently.

* Add product inventory and stock-level management.

* Add direct PDF/CSV invoice export and sales summary reports.

* Add customer login and an administrator dashboard for configuring discount slabs and tax categories dynamically.
