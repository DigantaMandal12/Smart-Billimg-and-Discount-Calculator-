# Smart Billing & Discount Calculator

An academic Python + Flask web application built for the **Programming with Python (PCC-CS393)** case study at **Budge Budge Institute of Technology, Kolkata** (Academic Year 2026–2027).

---

## 1. Key Features

- **Dynamic Product Entry:** Add up to 50 product rows with product name, unit price (₹), and whole-number quantity, or remove unneeded rows dynamically.
- **Exact Monetary Arithmetic:** Uses Python's `decimal.Decimal` with `ROUND_HALF_UP` two-decimal quantization to avoid binary floating-point rounding errors.
- **Automated Discount Slabs & Sample Tax:** Calculates line totals, subtotal, discount percentage and amount, discounted taxable subtotal, sample tax, and final payable amount.
- **Comprehensive Server-Side Validation:** Rejects empty names, names over 80 characters, non-numeric or negative prices, excessively large prices, zero/negative/fractional quantities, empty submissions, and malformed requests while preserving valid user inputs.
- **Responsive & Accessible UI:** Clean green-and-white interface with keyboard navigation, explicit form labels, mobile card layout, and a dedicated `@media print` invoice stylesheet.

---

## 2. Demonstration Calculation Rules

> **Disclaimer:** The discount slabs and sample tax rate below are configurable **demonstration values** for this academic project, not official tax guidance. Update `DISCOUNT_SLABS` and `TAX_RATE` in `app.py` if your instructor specifies different rules.

| Subtotal Slab | Discount Rate | Sample Tax Rate (Post-Discount) |
| :--- | :--- | :--- |
| Below ₹2,500.00 | **0%** | 5% on amount after discount |
| ₹2,500.00 to ₹4,999.99 | **5%** | 5% on amount after discount |
| ₹5,000.00 or more | **10%** | 5% on amount after discount |

---

## 3. Project Folder Structure

```text
SmartBillingCalculator/
├── app.py                  # Flask backend, Decimal billing engine, validation, and error handlers
├── requirements.txt        # Python package dependencies (Flask>=3.0.0,<4.0.0)
├── README.md               # Project documentation and setup guide
├── .gitignore              # Excludes .venv, __pycache__, and temporary logs from version control
├── templates/
│   ├── base.html           # Shared HTML5 layout shell, header, footer, and asset links
│   ├── index.html          # Billing form, itemized bill summary table, and discount rules
│   └── 404.html            # Custom HTTP 404 Page Not Found template
├── static/
│   ├── style.css           # Responsive green-and-white theme and @media print stylesheet
│   └── script.js           # Safe DOM row addition/removal and print button handler
├── tests/
│   └── test_app.py         # 15-test automated unittest suite (billing logic + HTTP routes)
└── report/
    └── REPORT_DRAFT.md     # Complete 19-section editable college project report draft
```

---

## 4. Windows 10/11 Setup & Run Instructions (PowerShell)

> **Backup Advice:** Before replacing your existing project folder, make a backup copy of your current `SmartBillingCalculator` folder (for example, `SmartBillingCalculator_Backup`) so none of your earlier notes or edits are lost.

### Step 1: Open the Project Folder in PowerShell
```powershell
cd path\to\SmartBillingCalculator
```

### Step 2: Verify Your Installed Python Version
```powershell
py --version
```
*(If `py` is not recognized, run `python --version`. On Windows with Python 3.15.1 installed, ensure "Add python.exe to PATH" was checked during setup or use the `py` launcher.)*

### Step 3: Create a Virtual Environment
```powershell
py -m venv .venv
```

### Step 4: Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```
**If PowerShell blocks script execution** (`PSSecurityException: ... cannot be loaded because running scripts is disabled on this system`), run this command to allow local scripts for the **current PowerShell window only**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```
**Alternative (Command Prompt / `cmd.exe`):**
```bat
.venv\Scripts\activate.bat
```

### Step 5: Install Dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 6: Start the Flask Application Server
```powershell
python app.py
```
*(Optional: To enable Flask's interactive reloader during local development only, run `$env:FLASK_DEBUG="1"; python app.py`.)*

Open your browser and navigate to:
**http://127.0.0.1:5000**

### Step 7: Run Automated Unit Tests
Open a terminal in the `SmartBillingCalculator` folder with `.venv` activated and run:
```powershell
python -m unittest discover -s tests -v
```

### Step 8: Stop the Server
Press **`Ctrl + C`** in the PowerShell terminal window where Flask is running, then run `deactivate` when you want to exit the virtual environment.
