from flask import Flask, render_template, request, jsonify
import math
import sympy as sp

app = Flask(__name__)


def safe_eval(expr_str, x_val):
    """Safely evaluate a mathematical expression at a given x value."""
    allowed_names = {
        "x": x_val,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "log": math.log,
        "log10": math.log10,
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,
    }
    try:
        result = eval(expr_str, {"__builtins__": {}}, allowed_names)
        return float(result)
    except Exception as e:
        raise ValueError(f"Could not evaluate expression: {e}")


def booles_rule(f_expr, a, b):
    """
    Apply Boole's Rule for numerical integration.
    
    Formula:
        h = (b - a) / 4
        integral ≈ (2h/45) * [7f(x0) + 32f(x1) + 12f(x2) + 32f(x3) + 7f(x4)]
    
    Returns a dict with all intermediate steps.
    """
    h = (b - a) / 4.0

    x0 = a
    x1 = a + h
    x2 = a + 2 * h
    x3 = a + 3 * h
    x4 = b

    fx0 = safe_eval(f_expr, x0)
    fx1 = safe_eval(f_expr, x1)
    fx2 = safe_eval(f_expr, x2)
    fx3 = safe_eval(f_expr, x3)
    fx4 = safe_eval(f_expr, x4)

    weighted_sum = 7 * fx0 + 32 * fx1 + 12 * fx2 + 32 * fx3 + 7 * fx4
    result = (2 * h / 45) * weighted_sum

    return {
        "h": h,
        "x0": x0, "x1": x1, "x2": x2, "x3": x3, "x4": x4,
        "fx0": fx0, "fx1": fx1, "fx2": fx2, "fx3": fx3, "fx4": fx4,
        "weighted_sum": weighted_sum,
        "coefficient": 2 * h / 45,
        "result": result,
        "f_expr": f_expr,
        "a": a,
        "b": b,
    }


def try_sympy_exact(f_expr, a, b):
    """Try to compute the exact integral using SymPy for comparison."""
    try:
        x = sp.Symbol("x")
        expr_str = f_expr.replace("^", "**")
        expr = sp.sympify(expr_str, locals={"x": x, "e": sp.E, "pi": sp.pi})
        exact = float(sp.integrate(expr, (x, a, b)))
        return exact
    except Exception:
        return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/examples")
def examples():
    return render_template("examples.html")


@app.route("/calculator")
def calculator():
    return render_template("calculator.html")


@app.route("/compute", methods=["POST"])
def compute():
    data = request.get_json()
    f_expr = data.get("function", "").strip()
    a_str = data.get("a", "")
    b_str = data.get("b", "")

    errors = []

    if not f_expr:
        errors.append("Function f(x) is required.")
    if a_str == "":
        errors.append("Lower bound 'a' is required.")
    if b_str == "":
        errors.append("Upper bound 'b' is required.")

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    try:
        a = float(eval(a_str, {"__builtins__": {}, "pi": math.pi, "e": math.e}))
        b = float(eval(b_str, {"__builtins__": {}, "pi": math.pi, "e": math.e}))
    except Exception:
        return jsonify({"success": False, "errors": ["Invalid bounds. Use numbers or expressions like 'pi'."] }), 400

    if a >= b:
        return jsonify({"success": False, "errors": ["Lower bound 'a' must be less than upper bound 'b'."]}), 400

    try:
        steps = booles_rule(f_expr, a, b)
    except ValueError as e:
        return jsonify({"success": False, "errors": [str(e)]}), 400

    exact = try_sympy_exact(f_expr, a, b)
    if exact is not None:
        steps["exact"] = exact
        steps["error"] = abs(steps["result"] - exact)
        steps["relative_error"] = abs(steps["error"] / exact) * 100 if exact != 0 else None

    return jsonify({"success": True, "steps": steps})


if __name__ == "__main__":
    app.run(debug=True)
