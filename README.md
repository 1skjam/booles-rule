# Boole's Rule — Numerical Integration Web App

A Flask web application demonstrating Boole's Rule for numerical integration, with a theory page, worked examples, and an interactive calculator.

## Features

- **Theory Page** — Mathematical explanation with MathJax-rendered formulas, weight visualization, error analysis, and comparison table
- **Worked Examples** — Two fully step-by-step solved problems (`x⁴` and `sin(x)`)
- **Interactive Calculator** — Enter any `f(x)`, `a`, `b` and get the full step-by-step Boole's Rule computation with error comparison (via SymPy)

## Project Structure

```
booles-rule/
├── app.py                  # Flask backend + Boole's Rule logic
├── requirements.txt
├── vercel.json             # Vercel deployment config
├── templates/
│   ├── base.html           # Shared layout, nav, footer
│   ├── index.html          # Theory / home page
│   ├── examples.html       # Worked examples
│   └── calculator.html     # Interactive calculator
└── static/
    └── css/
        └── style.css       # All styles
```

## Local Setup

```bash
# 1. Clone / download the project
cd booles-rule

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py

# 5. Open in browser
# http://127.0.0.1:5000
```

## Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow the prompts. The vercel.json config handles routing automatically.
```

## Supported Functions (Calculator)

| Category     | Syntax                              |
|--------------|-------------------------------------|
| Power        | `x**2`, `x**4`, `x**0.5`           |
| Trig         | `sin(x)`, `cos(x)`, `tan(x)`       |
| Inverse Trig | `asin(x)`, `acos(x)`, `atan(x)`    |
| Hyperbolic   | `sinh(x)`, `cosh(x)`, `tanh(x)`    |
| Exponential  | `exp(x)`, `exp(-x**2)`             |
| Logarithm    | `log(x)`, `log10(x)`               |
| Square root  | `sqrt(x)`                           |
| Constants    | `pi`, `e`                           |
| Composite    | `sin(x)*exp(-x)`, `x**2 + cos(x)`  |

## Boole's Rule Formula

```
h = (b - a) / 4

∫[a,b] f(x) dx ≈ (2h/45) × [7f(x₀) + 32f(x₁) + 12f(x₂) + 32f(x₃) + 7f(x₄)]

where xᵢ = a + i·h, i = 0, 1, 2, 3, 4
```

Error order: O(h⁷) — exact for polynomials of degree ≤ 5.
