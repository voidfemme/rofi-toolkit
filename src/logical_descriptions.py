from rofi import Rofi
from src.utils.notify_send import notify
import subprocess
import sys

# Array of logical operators with natural language descriptions
operators = [
    "∧ AND",
    "∨ OR",
    "¬ NOT",
    "⊕ XOR",
    "→ IMPLIES",
    "↔ IFF",
    "∃ EXISTS backwards e",
    "∀ FOR ALL upside down A",
    "∈ ELEMENT OF lowercase e with line",
    "∉ NOT ELEMENT OF slashed lowercase e with line",
    "⊂ SUBSET OF c shape",
    "⊃ SUPERSET OF backwards c shape",
    "∪ UNION u shape",
    "∩ INTERSECTION n shape",
    "∅ EMPTY SET circle with slash",
    "ℕ NATURAL NUMBERS",
    "ℤ INTEGERS",
    "ℚ RATIONAL NUMBERS",
    "ℝ REAL NUMBERS",
    "ℂ COMPLEX NUMBERS",
    "∞ INFINITY sideways 8",
    "≈ APPROXIMATELY EQUAL",
    "≠ NOT EQUAL",
    "≤ LESS THAN OR EQUAL",
    "≥ GREATER THAN OR EQUAL",
    "± PLUS-MINUS",
    "× MULTIPLICATION",
    "÷ DIVISION",
    "√ SQUARE ROOT check mark",
    "∑ SUMMATION big sigma",
    "∏ PRODUCT big pi",
    "∂ PARTIAL DERIVATIVE curly d",
    "∇ NABLA/DEL triangle",
    "∫ INTEGRAL long s",
    "∮ CONTOUR INTEGRAL circle integral",
    "∝ PROPORTIONAL TO infinity symbol on side",
    "° DEGREE",
    "⊥ PERPENDICULAR",
    "∠ ANGLE less than symbol with line",
    "π PI",
    "ε EPSILON",
    "μ MU",
    "σ SIGMA",
    "Ω OMEGA",
    "α ALPHA",
    "β BETA",
    "γ GAMMA",
    "δ DELTA",
    "θ THETA",
    "λ LAMBDA",
    "φ PHI",
    "ψ PSI",
    "ω OMEGA LOWERCASE",
    "ℏ PLANCK CONSTANT h with bar",
    "⟨ LEFT ANGLE BRACKET left pointy bracket",
    "⟩ RIGHT ANGLE BRACKET right pointy bracket",
    "ℒ LAGRANGIAN cursive L",
    "ℋ HAMILTONIAN cursive H",
    "⊗ TENSOR PRODUCT circle with x",
    "⊕ DIRECT SUM circle with plus",
    "† HERMITIAN CONJUGATE cross",
    "‖ NORM double vertical lines",
    "→ VECTOR ARROW",
    "⇌ EQUILIBRIUM double arrow with equal top",
    "⇋ REVERSIBLE REACTION double arrow with half arrow top",
]


def logical_descriptions_menu(rofi: Rofi):
    selection = rofi.select("Select logical operator:", operators)

    if isinstance(selection, str):
        symbol = selection.split(" ")[0]
    else:
        # error
        symbol = None

    if symbol is None:
        sys.exit(0)

    subprocess.run(["wl-copy"], input=symbol)

    notify("Copied to clipboard", symbol)
