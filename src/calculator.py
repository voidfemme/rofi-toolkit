from rofi import Rofi
from src.utils.notify_send import notify
from src.utils.utils import copy_to_clipboard
import logging
import os
import re
import sys

logger = logging.getLogger(__name__)

HISTORY_FILE = os.path.expanduser("~/Scripts/.rofi_calculator_history")
MAX_HISTORY = 10


def is_safe_expression(expr: str) -> bool:
    return bool(re.match(r"^[\d\s\+\-\*/\(\)\.\^%]+$", expr))


def read_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return f.read().splitlines()
    return []


def add_to_history(entry: str) -> None:
    history = read_history()
    history.insert(0, entry)
    history = history[:MAX_HISTORY]
    with open(HISTORY_FILE, "w") as f:
        f.write("\n".join(history))


def evaluate_expression(expr: str) -> str:
    expr = expr.strip()  # remove leading/trailing whitespace
    expr = expr.replace("^", "**")
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


def calculate(args: list[str]) -> list[str]:
    if len(args) > 1:
        if args[0] == "--history":
            return ["\n".join(read_history())]
        else:
            return [evaluate_expression(sys.argv[0])]
    else:
        return ["Usage\nUsage: calculator <expression> or --history"]


def calculator_menu(rofi: Rofi):
    while True:
        history = calculate(["--history"])

        options = history + [":Calculate"]
        index, _ = rofi.select("Calculator:", options)
        if index == -1:
            sys.exit(0)
        expression = options[index]

        if expression == ":Calculate":
            expression = rofi.text_entry("Calculate:")
        elif "=" in expression:
            expression = history[index].split("=")[0].strip()

        logger.debug(f"Expression to evaluate: {expression}")

        if isinstance(expression, str):
            result = calculate([expression])
        else:
            result = None

        logger.debug(f"raw result from calculate(): {result}")

        if result is None:
            notify("Calculator Error", "No output from calculation")
            continue

        # Display results in rofi and get user selection
        selection = rofi.text_entry("Result (Enter to copy):", result[0])

        logger.debug(f"User selection: {selection}")

        if selection is None:
            continue

        copy_to_clipboard(selection)

        continue_calc = rofi.select("Continue calculating?", ["yes", "no"])

        if continue_calc[0] != 0:
            break
