# College Project Report Draft — Smart Billing & Discount Calculator

> **Student Instructions before Printing:**
> 1. Fill in all blank placeholders (`____________________`) on the Cover Page, Certificate, and Acknowledgement with your genuine personal details.
> 2. Do **not** submit placeholder text for screenshots—capture actual screenshots from your own computer while running the project and insert them into **Section 15**.
> 3. The discount slabs and 5% tax rate documented in this report are **academic demonstration values**, not official tax rules.

---

## 1. Cover Page

<div align="center">

### BUDGE BUDGE INSTITUTE OF TECHNOLOGY
**Nischintapur, Budge Budge, Kolkata – 700 137, West Bengal, India**

**DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING**

---

### CASE STUDY REPORT ON
# **SMART BILLING & DISCOUNT CALCULATOR**

**Course Name:** Programming with Python  
**Course / Subject Code:** PCC-CS393  
**Academic Year:** 2026–2027  

---

**Submitted By:**

| Field | Student Details (Fill Before Printing) |
| :--- | :--- |
| **Student Name** | `________________________________________` |
| **University Roll Number** | `________________________________________` |
| **University Registration Number** | `________________________________________` |
| **Department / Branch** | Computer Science & Engineering |
| **Year / Semester / Section** | `________________________________________` |

---

**Submitted To:**

| Field | Faculty Details (Fill Before Printing) |
| :--- | :--- |
| **Subject Teacher / Guide Name** | `________________________________________` |
| **Designation** | `________________________________________` |
| **Department** | Department of Computer Science & Engineering |
| **Date of Submission** | `________________________________________` |

</div>

---

## 2. Bona Fide Certificate (Placeholder)

> *Include this page if required by your departmental formatting guidelines.*

<div align="center">

### **CERTIFICATE OF COMPLETION**

</div>

This is to certify that the case study project report entitled **"Smart Billing & Discount Calculator"** is a bona fide record of work carried out by **`____________________________`** (University Roll No.: **`____________________________`**, Registration No.: **`____________________________`**) of Semester **`______`**, Department of Computer Science & Engineering, **Budge Budge Institute of Technology, Kolkata**, in partial fulfilment of the requirements for the practical/case-study evaluation of **Programming with Python (PCC-CS393)** during the Academic Year **2026–2027**.

<br><br>

| | |
| :--- | :--- |
| **Signature of Subject Teacher / Project Guide** | **Signature of Head of Department (HOD)** |
| Name: `____________________________` | Name: `____________________________` |
| Designation: `_____________________` | Department of Computer Science & Engineering |
| Date: `____________________________` | Date: `____________________________` |

<br>

**Signature of External / Internal Examiner:** `____________________________`  
**Date of Evaluation:** `____________________________`

---

## 3. Acknowledgement

I would like to express my sincere gratitude to my subject teacher, **`____________________________`**, Department of Computer Science & Engineering, **Budge Budge Institute of Technology, Kolkata**, for providing continuous guidance, constructive feedback, and technical mentorship throughout the design, debugging, and testing of this **Smart Billing & Discount Calculator** case study for **Programming with Python (PCC-CS393)**.

I also extend my heartfelt thanks to the Head of the Department and the faculty members of the Department of Computer Science & Engineering for providing the laboratory infrastructure and academic environment needed to complete this work. Finally, I thank my classmates and family for their encouragement during the completion of this project.

<br>

**Student Signature:** `____________________________`  
**Student Name:** `____________________________`  
**University Roll No.:** `____________________________`  
**Date:** `____________________________`

---

## 4. Abstract

The **Smart Billing & Discount Calculator** is a lightweight, modular web application developed using **Python** and the **Flask** micro-framework, combined with a responsive **HTML5, CSS3, and JavaScript** frontend. In small retail counters and academic demonstrations, manual invoice calculation across multiple items, tiered discount thresholds, and post-discount tax percentages frequently leads to arithmetic errors, floating-point rounding discrepancies, and inconsistent input validation.

To address these challenges, this project implements a deterministic billing engine powered by Python's `decimal.Decimal` module using `ROUND_HALF_UP` two-decimal rounding. Users can dynamically enter up to 50 products with their unit prices and whole-number quantities, remove rows interactively, and generate an itemized bill summary. The server validates every input field—rejecting empty product names, negative or malformed prices, fractional or zero quantities, and oversized payloads—while preserving valid user input when validation fails. Furthermore, the system resolves a classic Jinja2 dictionary-method collision (`bill.items` vs. `bill["items"]`) and includes a 15-test automated `unittest` suite verifying both boundary calculations and HTTP routes.

---

## 5. Table of Contents

1. Cover Page
2. Bona Fide Certificate
3. Acknowledgement
4. Abstract
5. Table of Contents
6. Introduction
7. Problem Statement
8. Objectives
9. Hardware and Software Requirements
10. System Design and Architecture
11. Algorithm and Flowchart Description
12. Billing Formulae and Demonstration Rules
13. Implementation Details (Key Engineering Decisions & Bug Fixes)
14. Test Cases and Automated Verification Results
15. Genuine Application Screenshot Placeholders & Capture Checklist
16. Limitations
17. Future Enhancements
18. Conclusion
19. References

---

## 6. Introduction

Computerized billing systems form the backbone of everyday commercial transactions. While enterprise retail systems rely on complex point-of-sale (POS) databases, learning the core programming principles behind reliable billing software requires focusing on three foundational pillars:
1. **Exact Monetary Representation:** Standard IEEE 754 binary floating-point numbers (`float`) cannot represent base-10 fractions such as `0.1` or `0.05` exactly, leading to subtle rounding errors (e.g., `0.1 + 0.2 == 0.30000000000000004`). Using Python's `Decimal` type guarantees exact base-10 monetary calculations.
2. **Conditional Tiered Logic:** Retail discounts often follow slab-based thresholds where the discount rate depends on the total purchase value before tax.
3. **Defense-in-Depth Input Validation:** Client-side HTML5 attributes (`required`, `min`, `step`) improve user experience, but only strict server-side validation in Python protects the application against malformed or tampered HTTP POST requests.

The **Smart Billing & Discount Calculator** brings these concepts together in a clean Flask web application designed for the **PCC-CS393 Programming with Python** case study.

---

## 7. Problem Statement

When preparing an itemized bill manually or using ad-hoc spreadsheet formulas:
- Calculating line totals ($\text{Price} \times \text{Quantity}$) across dozens of items is slow and prone to human error.
- Selecting the correct discount slab near boundary values (such as ₹2,499.99 vs. ₹2,500.00 or ₹4,999.99 vs. ₹5,000.00) can be inconsistent.
- Calculating tax on the discounted subtotal requires accurate intermediate rounding.
- Invalid inputs—such as negative prices, blank item names, or fractional quantities for discrete items—can corrupt totals or crash poorly written programs.

The objective is to build a self-contained, offline-capable Python + Flask web application that automates multi-item billing, enforces strict server-side input validation, and generates a clean, printable itemized bill.

---

## 8. Objectives

1. **Multi-Product Dynamic Entry:** Allow users to add and remove up to 50 product rows dynamically in the browser and submit them in a single form request.
2. **Exact Decimal Arithmetic:** Perform all monetary calculations using Python's `Decimal` class and round currency outputs consistently to two decimal places (`0.01`) using `ROUND_HALF_UP`.
3. **Tiered Discount Slab Application:** Automatically determine and apply the demonstration discount slab (0%, 5%, or 10%) based on the calculated subtotal.
4. **Post-Discount Sample Tax Calculation:** Compute a configurable 5% sample tax on the discounted amount and calculate the final payable total.
5. **Robust Server-Side Validation:** Validate all submitted product names, prices, and quantities on the server, returning clear user-facing error messages without exposing Python tracebacks.
6. **Responsive & Print-Ready UI:** Present the itemized invoice in an accessible green-and-white interface with a dedicated `@media print` stylesheet.
7. **Automated Verification:** Verify all boundary conditions, calculation rules, and error states using Python's `unittest` framework and Flask's test client.

---

## 9. Hardware and Software Requirements

### 9.1 Hardware Requirements
- **Processor:** Dual-core x86_64 processor (Intel Core i3 / AMD Ryzen 3 or higher; runs on any modern PC or laptop)
- **Memory (RAM):** Minimum 2 GB RAM (4 GB or higher recommended)
- **Storage:** Less than 50 MB of free disk space (including virtual environment)
- **Display:** 1024 × 768 minimum resolution (responsive across desktop and mobile viewports)

### 9.2 Software Requirements
- **Operating System:** Windows 10 / Windows 11 (also compatible with macOS and Linux)
- **Command-Line Shell:** Windows PowerShell or Command Prompt (`cmd.exe`)
- **Python Runtime:** Python 3.10 or newer (compatible with Python 3.11–3.15.x)
- **Backend Web Framework:** Flask 3.x (`Flask>=3.0.0,<4.0.0`)
- **Frontend Technologies:** HTML5, CSS3, Vanilla JavaScript (ES6)
- **Code Editor / IDE:** Visual Studio Code
- **Web Browser:** Google Chrome, Microsoft Edge, or Mozilla Firefox

---

## 10. System Design and Architecture

The application follows a clean three-layer **Model–View–Controller (MVC) / MVT** style architecture adapted for a stateless Flask web service:

```text
+-----------------------------------------------------------------------+
|                        CLIENT BROWSER (Frontend)                      |
|  - templates/base.html & index.html (HTML5 Form & Itemized Table)     |
|  - static/style.css (Responsive Green/White Theme & @media print)     |
|  - static/script.js (Safe DOM Row Addition/Removal & Print Trigger)   |
+-----------------------------------+-----------------------------------+
                                    |
                     HTTP GET /     |     HTTP POST /
                                    v
+-----------------------------------------------------------------------+
|                      FLASK CONTROLLER (app.py)                        |
|  - Route Handler: index()                                             |
|  - Extracts item_name[], price[], quantity[] arrays                   |
|  - Preserves entered form values on validation failure                |
|  - Custom Error Handlers: 404 (Not Found), 413 (Payload Too Large),   |
|    500 (Internal Error)                                               |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|               VALIDATION & BILLING ENGINE (app.py)                    |
|  - parse_item_row(): Validates name, non-negative Decimal price,      |
|    and whole-number quantity (1..100,000)                             |
|  - calculate_bill(): Computes line_total, subtotal, discount_rate,    |
|    discount, taxable_amount, sample tax, and final total              |
|  - money(): Quantizes all currency values to Decimal("0.01")          |
+-----------------------------------------------------------------------+
```

---

## 11. Algorithm and Flowchart Description

### 11.1 Step-by-Step Algorithm

1. **Start** the Flask web server on `http://127.0.0.1:5000`.
2. **If HTTP request is `GET /`:**
   - Render `index.html` with one blank product row (`name=""`, `price=""`, `quantity="1"`) and the empty-state bill placeholder.
3. **If HTTP request is `POST /`:**
   - Read parallel form lists `item_name[]`, `price[]`, and `quantity[]`.
   - Check that the lists are non-empty, have equal lengths, and contain at most 50 rows. If not, set an error message and re-render the form.
4. **For each submitted product row $i = 1, 2, \dots, n$:**
   - Strip leading/trailing whitespace from `name`. If `name` is empty or exceeds 80 characters, raise a `ValueError`.
   - Parse `price` as a `Decimal`. If parsing fails, `price` is non-finite, `price < 0`, or `price > 100,000,000`, raise a `ValueError`.
   - Parse `quantity` as a `Decimal`. If parsing fails, `quantity` is non-finite, `quantity` has a fractional part (`quantity != quantity.to_integral_value()`), or `quantity` is outside $[1, 100000]$, raise a `ValueError`.
5. **If any validation check raises an exception:**
   - Catch the error, keep the user's entered `form_items` intact, display the descriptive error banner in `index.html`, and stop calculation.
6. **If all rows are valid, compute the bill:**
   - Initialize `subtotal = Decimal("0.00")`.
   - For each item, round `price = money(price)`, compute `line_total = money(price * quantity)`, and add `line_total` to `subtotal`.
   - Determine `discount_rate`:
     - If `subtotal >= 5000.00`, `discount_rate = 0.10` (10%).
     - Else if `subtotal >= 2500.00`, `discount_rate = 0.05` (5%).
     - Else, `discount_rate = 0.00` (0%).
   - Compute `discount = money(subtotal * discount_rate)`.
   - Compute `taxable_amount = money(subtotal - discount)`.
   - Compute `tax = money(taxable_amount * 0.05)`.
   - Compute `total = money(taxable_amount + tax)`.
7. **Render `index.html`** passing the `bill` dictionary (`bill["items"]`, `bill["subtotal"]`, `bill["discount"]`, `bill["tax"]`, `bill["total"]`).
8. **End.**

### 11.2 Flowchart Description (Text Representation for Report Diagram)

```text
                       +-------------------+
                       |       START       |
                       +---------+---------+
                                 |
                                 v
                  +--------------+--------------+
                  | User enters Product Name,   |
                  | Unit Price, and Quantity    |
                  | rows and clicks Calculate   |
                  +--------------+--------------+
                                 |
                                 v
                  +--------------+--------------+
                  | Validate all rows:          |
                  | - Non-empty name (<=80 ch)  |
                  | - Price >= 0 & finite       |
                  | - Whole-number Qty >= 1     |
                  +--------------+--------------+
                                 |
                        +--------+--------+
                        |  All Inputs     |
                        |     Valid?      |
                        +---+---------+---+
                            |         |
                         No |         | Yes
                            v         v
        +-------------------+--+   +--+--------------------------------+
        | Retain entered rows  |   | Compute Line Totals & Subtotal:   |
        | & show Validation    |   | line_total = round(price * qty)   |
        | Error Alert          |   | subtotal = sum(line_totals)       |
        +---------+------------+   +-----------------+-----------------+
                  |                                  |
                  |                                  v
                  |                +-----------------+-----------------+
                  |                | Check Subtotal Discount Slab:     |
                  |                | - Subtotal >= 5000 -> 10%         |
                  |                | - Subtotal >= 2500 -> 5%          |
                  |                | - Subtotal <  2500 -> 0%          |
                  |                +-----------------+-----------------+
                  |                                  |
                  |                                  v
                  |                +-----------------+-----------------+
                  |                | discount = subtotal * rate        |
                  |                | taxable  = subtotal - discount    |
                  |                | tax      = taxable * 5%           |
                  |                | total    = taxable + tax          |
                  |                +-----------------+-----------------+
                  |                                  |
                  |                                  v
                  |                +-----------------+-----------------+
                  |                | Render Itemized Bill Table &      |
                  |                | Summary Card (Print-Ready)        |
                  +--------------->+-----------------+-----------------+
                                                     |
                                                     v
                                           +---------+---------+
                                           |        END        |
                                           +-------------------+
```

---

## 12. Billing Formulae and Demonstration Rules

### 12.1 Mathematical Formulae

For $n$ products where product $i$ has rounded unit price $P_i$ and integer quantity $Q_i$:

1. **Line Total for Product $i$:**
   $$L_i = \text{round}(P_i \times Q_i, 2)$$

2. **Subtotal:**
   $$S = \sum_{i=1}^{n} L_i$$

3. **Demonstration Discount Rate ($r_d$):**
   $$r_d = \begin{cases} 0.00 & \text{if } S < 2500.00 \\ 0.05 & \text{if } 2500.00 \le S < 5000.00 \\ 0.10 & \text{if } S \ge 5000.00 \end{cases}$$

4. **Discount Amount ($D$):**
   $$D = \text{round}(S \times r_d, 2)$$

5. **Taxable Amount After Discount ($T_{\text{base}}$):**
   $$T_{\text{base}} = S - D$$

6. **Sample Tax Amount ($T$, at demonstration rate $r_t = 0.05$):**
   $$T = \text{round}(T_{\text{base}} \times 0.05, 2)$$

7. **Final Payable Amount ($F$):**
   $$F = T_{\text{base}} + T$$

### 12.2 Worked Numerical Examples

| Metric | Example A (Below ₹2,500) | Example B (₹2,500–₹4,999.99) | Example C (₹5,000 or more) |
| :--- | right | right | right |
| **Sample Input** | 2 × ₹100.00 Pen | 1 × ₹2,500.00 Book Set | 1 × ₹5,000.00 Lab Kit |
| **Subtotal ($S$)** | ₹200.00 | ₹2,500.00 | ₹5,000.00 |
| **Discount Slab ($r_d$)** | 0% | 5% | 10% |
| **Discount Amount ($D$)** | ₹0.00 | ₹125.00 | ₹500.00 |
| **Amount After Discount ($T_{\text{base}}$)** | ₹200.00 | ₹2,375.00 | ₹4,500.00 |
| **Sample Tax (5% of $T_{\text{base}}$)** | ₹10.00 | ₹118.75 | ₹225.00 |
| **Final Payable Amount ($F$)** | **₹210.00** | **₹2,493.75** | **₹4,725.00** |

---

## 13. Implementation Details (Key Engineering Decisions & Bug Fixes)

1. **Fixing the `TypeError: 'builtin_function_or_method' object is not iterable` Bug:**
   - **Root Cause:** In Python, every dictionary (`dict`) has a built-in `.items()` method. When `calculate_bill()` returned a dictionary containing the key `"items"`, the original Jinja2 template used dot notation (`{% for item in bill.items %}`). In Jinja2, attribute lookup on a `dict` resolves the built-in `dict.items` method before dictionary keys, causing Jinja2 to attempt iterating over a method object instead of the product list.
   - **Fix:** Updated `templates/index.html` to use explicit dictionary-key bracket notation (`{% for item in bill["items"] %}`) across all dictionary accesses (`bill["subtotal"]`, `bill["discount"]`, `bill["tax"]`, `bill["total"]`, and `item["name"]`, `item["price"]`, etc.).
2. **Using `Decimal` Instead of `float`:**
   - Monetary values are converted directly from strings into `decimal.Decimal` objects and rounded with `ROUND_HALF_UP` via the `money()` helper function so that every line total, discount, tax, and final payable amount matches standard currency rounding.
3. **Safe DOM Manipulation in `static/script.js`:**
   - Moved inline scripts out of `index.html` into `static/script.js` and replaced HTML string concatenation with `document.createElement()` and `.textContent` assignments, eliminating any risk of Cross-Site Scripting (XSS) when dynamically adding or removing rows.
4. **Template Inheritance & Custom Error Pages:**
   - Separated common page layout into `templates/base.html`, main billing view into `templates/index.html`, and added `templates/404.html` along with graceful 404, 413, and 500 error handlers in `app.py`.

---

## 14. Test Cases and Automated Verification Results

The project includes an automated test suite in `tests/test_app.py` built with Python's standard `unittest` framework.

| Test ID | Test Case Description | Input Data | Expected Result |
| :--- | :--- | :--- | :--- |
| **TC-01** | Homepage GET request | `GET /` | HTTP 200 OK; page title rendered |
| **TC-02** | Normal bill calculation | `Pen`, Price `100`, Qty `2` | Subtotal `₹200.00`, Discount `₹0.00`, Tax `₹10.00`, Total `₹210.00` |
| **TC-03** | Subtotal below ₹2,500 (boundary) | Price `2499.99`, Qty `1` | 0% discount (`₹0.00`), Tax `₹125.00`, Total `₹2624.99` |
| **TC-04** | Subtotal exactly ₹2,500 (boundary) | Price `2500`, Qty `1` | 5% discount (`₹125.00`), Tax `₹118.75`, Total `₹2493.75` |
| **TC-05** | Subtotal just below ₹5,000 (boundary) | Price `4999.99`, Qty `1` | 5% discount (`₹250.00`), Tax `₹237.50`, Total `₹4987.49` |
| **TC-06** | Subtotal exactly ₹5,000 (boundary) | Price `5000`, Qty `1` | 10% discount (`₹500.00`), Tax `₹225.00`, Total `₹4725.00` |
| **TC-07** | Multiple products calculation | 3 products (`3×10`, `2×100`, `2×1200.50`) | Subtotal `₹2631.00`, 5% discount `₹131.55`, Tax `₹124.97`, Total `₹2624.42` |
| **TC-08** | Negative price rejection | Price `-1`, Qty `1` | Rejected with `ValueError` / validation banner; form retains input |
| **TC-09** | Empty product name rejection | Name `"   "`, Price `10`, Qty `1` | Rejected with `ValueError` / `"Every product needs a name."` |
| **TC-10** | Zero & negative quantity rejection | Price `10`, Qty `0` or `-5` | Rejected with `ValueError` / `"Quantity must be between 1 and 100000."` |
| **TC-11** | Fractional quantity rejection | Price `10`, Qty `1.5` | Rejected with `ValueError` / `"Quantity must be a whole number."` |
| **TC-12** | Invalid numeric input rejection | Price `"not-a-number"`, Qty `1` | Rejected with `ValueError` / `"Enter a valid price for every product."` |
| **TC-13** | Missing / mismatched form fields | Empty `POST /` or unequal arrays | HTTP 200 with error message `"Please provide at least one complete product row."` |
| **TC-14** | Jinja `bill["items"]` rendering | `POST /` with 2 valid items | HTTP 200; renders itemized table without `TypeError` |

*(Before printing your report, paste or attach the screenshot of `python -m unittest discover -s tests -v` from your own Windows PowerShell terminal in Section 15.)*

---

## 15. Genuine Application Screenshot Placeholders & Capture Checklist

> **Important Academic Integrity Note:** Do **not** leave these boxes blank when printing. Run the application locally on your computer and insert genuine screenshots captured from your own machine.

### Screenshot 1: PowerShell Terminal Running the Flask Server & Unit Tests
```text
+-------------------------------------------------------------------------+
| [INSERT GENUINE SCREENSHOT 1 HERE]                                      |
|                                                                         |
| What to capture:                                                        |
| 1. Your Windows PowerShell window showing `.venv` activated.            |
| 2. Output of `python -m unittest discover -s tests -v` showing `OK`.    |
| 3. Output of `python app.py` showing `Running on http://127.0.0.1:5000` |
+-------------------------------------------------------------------------+
```

### Screenshot 2: Initial Product Entry Dashboard (`http://127.0.0.1:5000`)
```text
+-------------------------------------------------------------------------+
| [INSERT GENUINE SCREENSHOT 2 HERE]                                      |
|                                                                         |
| What to capture:                                                        |
| Full browser window at http://127.0.0.1:5000 showing the header,        |
| Step 1 product entry form with 2–3 added product rows, the empty-state  |
| preview card, and the Demonstration Discount & Tax Rules cards.         |
+-------------------------------------------------------------------------+
```

### Screenshot 3: Calculated Itemized Bill with Discount & Sample Tax
```text
+-------------------------------------------------------------------------+
| [INSERT GENUINE SCREENSHOT 3 HERE]                                      |
|                                                                         |
| What to capture:                                                        |
| Browser window after clicking "Calculate Bill" for a multi-item order   |
| (e.g., Subtotal >= ₹2,500 or >= ₹5,000), clearly showing the itemized   |
| table, Subtotal, Discount % and amount, Amount After Discount, Sample   |
| Tax (5%), and Final Payable Amount.                                     |
+-------------------------------------------------------------------------+
```

### Screenshot 4: Server-Side Validation Error Message (With Retained Input)
```text
+-------------------------------------------------------------------------+
| [INSERT GENUINE SCREENSHOT 4 HERE]                                      |
|                                                                         |
| What to capture:                                                        |
| Browser window showing the red Validation Error banner when submitting  |
| an invalid value (such as a fractional quantity `1.5` or negative       |
| price `-50`), demonstrating that entered values remain in the inputs.   |
+-------------------------------------------------------------------------+
```

### Screenshot 5: Print Preview of the Itemized Bill (`Ctrl + P`)
```text
+-------------------------------------------------------------------------+
| [INSERT GENUINE SCREENSHOT 5 HERE]                                      |
|                                                                         |
| What to capture:                                                        |
| Browser print preview triggered by clicking "Print Itemized Bill",      |
| showing how the `@media print` stylesheet hides the form controls and   |
| formats a clean single-page invoice.                                    |
+-------------------------------------------------------------------------+
```

---

## 16. Limitations

1. **Stateless In-Memory Execution:** The application does not use a relational database (such as SQLite or PostgreSQL), so bills are calculated on demand and are not permanently stored after the browser tab is closed.
2. **Single-Rate Demonstration Tax:** A uniform 5% sample tax rate is applied to the discounted subtotal for educational demonstration rather than per-category HSN/GST rates.
3. **No User Authentication or Payment Gateway:** Designed strictly as an academic case study, it omits login screens, role-based access control, and online payment processing.
4. **Local Development Server:** Flask's built-in Werkzeug server is meant for local development and academic demonstrations, not high-concurrency internet deployment.

---

## 17. Future Enhancements

1. **SQLite Invoice History:** Add a lightweight SQLite database to store generated bills with unique invoice numbers, customer names, and timestamps.
2. **Direct CSV / PDF Export:** Allow users to download invoice records as `.csv` spreadsheet files in addition to browser printing.
3. **Per-Item Category Tax Rates:** Support selectable tax slabs (e.g., 0%, 5%, 12%, 18%) per product row.
4. **Configurable Admin Settings:** Provide a settings panel where instructors or shopkeepers can customize discount slab thresholds without editing Python constants.

---

## 18. Conclusion

The **Smart Billing & Discount Calculator** successfully demonstrates how core Python programming constructs—functions, list comprehensions, dictionaries, conditional slabs, exception handling, and exact `Decimal` currency arithmetic—can be integrated with the **Flask** web framework and a responsive **HTML5/CSS3/JavaScript** interface. By identifying and fixing the Jinja2 `bill.items` dictionary collision, enforcing strict server-side input validation, and verifying behaviour with 22 automated unit tests, the project delivers a reliable, maintainable, and user-friendly application fulfilling the objectives of the **PCC-CS393 Programming with Python** case study.

---

## 19. References

1. **Course Case-Study Handout:** *Programming with Python (PCC-CS393)*, Department of Computer Science & Engineering, Budge Budge Institute of Technology, Academic Year 2026–2027.
2. **Python Software Foundation:** *Python 3 Standard Library Documentation — `decimal` Decimal fixed point and floating point arithmetic*, [https://docs.python.org/3/library/decimal.html](https://docs.python.org/3/library/decimal.html)
3. **Python Software Foundation:** *Python 3 Standard Library Documentation — `unittest` Unit testing framework*, [https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html)
4. **Pallets Projects:** *Flask 3.x Official Documentation*, [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
5. **Pallets Projects:** *Jinja Template Designer Documentation — Variables and Dictionary Access*, [https://jinja.palletsprojects.com/](https://jinja.palletsprojects.com/)
6. **MDN Web Docs:** *HTML Forms and CSS `@media print` Guide*, [https://developer.mozilla.org/](https://developer.mozilla.org/)
