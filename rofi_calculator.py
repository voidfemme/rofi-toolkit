#!/usr/bin/env python3
import sys
import re
import os

HISTORY_FILE = os.path.expanduser("~/scripts/.rofi_calculator_history")
MAX_HISTORY = 10


def is_safe_expression(expr):
    return bool(re.match(r"^[\d\s\+\-\*/\(\)\.]+$", expr))


def evaluate_expression(expr):
    expr = expr.strip()  # Remove leading/trailing whitespace
    if is_safe_expression(expr):
        try:
            result = eval(expr)
            output = f"{result}\n{expr} = {result}"
            add_to_history(f"{expr} = {result}")
            return output
        except Exception as e:
            return f"Error\nError: {str(e)}"
    else:
        return f"Error\nError: Invalid expression: {expr}"


def add_to_history(entry):
    history = read_history()
    history.insert(0, entry)
    history = history[:MAX_HISTORY]
    with open(HISTORY_FILE, "w") as f:
        f.write("\n".join(history))


def read_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return f.read().splitlines()
    return []


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--history":
            print("\n".join(read_history()))
        else:
            print(evaluate_expression(sys.argv[1]))
    else:
        print("Usage\nUsage: ./rofi_calculator.py <expression> or --history")
