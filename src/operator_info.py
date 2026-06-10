# src/operator_info.py
import subprocess
from rofi import Rofi
from src.utils.notify_send import notify
import sys

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
    "∴ THEREFORE triangle of dots",
    "⟨| BRA left angle bracket with vertical bar",
    "|⟩ KET vertical bar with right angle bracket",
    "⟨|⟩ BRAKET left angle bracket, vertical bar, right angle bracket",
]

operator_info = {
    "∧": "Logical AND: True if both operands are true.",
    "∨": "Logical OR: True if at least one operand is true.",
    "¬": "Logical NOT: Negates the truth value of its operand.",
    "⊕": [
        "Exclusive OR: True if exactly one operand is true.",
        "Direct sum: A binary operation between two vector spaces.",
    ],
    "→": [
        "Implication: False only when the antecedent is true and the consequent is false.",
        "Vector arrow: Indicates a vector quantity or an implication",
    ],
    "↔": "If and only if (IFF): True when both operands have the same truth value.",
    "∃": "Existential Quantifier: There exists at least one instance where the statement is true.",
    "∀": "Universal Quantifier: The statement is true for all instances.",
    "∈": "Element of: Indicates that an element belongs to a set.",
    "∉": "Not an element of: Indicates that an element does not belong to a set.",
    "⊂": "Subset: All elements of one set are contained in another set.",
    "⊃": "Superset: Contains all elements of another set.",
    "∪": "Union: Combines all unique elements from two or more sets.",
    "∩": "Intersection: Contains elements common to all sets involved.",
    "∅": "Empty Set: A set that contains no elements.",
    "ℕ": "Natural Numbers: The set of positive integers (sometimes including 0).",
    "ℤ": "Integers: The set of all positive and negative whole numbers, including zero.",
    "ℚ": "Rational Numbers: Numbers that can be expressed as a fraction of two integers.",
    "ℝ": "Real Numbers: The set of all rational and irrational numbers.",
    "ℂ": "Complex Numbers: Numbers with both real and imaginary parts.",
    "∞": "Infinity: A concept of something without any limit.",
    "≈": "Approximately equal: Indicates that two values are nearly equal.",
    "≠": "Not equal: Indicates that two values are not equal.",
    "≤": "Less than or equal to: Indicates that one value is less than or equal to another.",
    "≥": "Greater than or equal to: Indicates that one value is greater than or equal to another.",
    "±": "Plus-minus: Indicates a value that can be either positive or negative.",
    "×": "Multiplication: The operation of multiplying two numbers.",
    "÷": "Division: The operation of dividing one number by another.",
    "√": "Square root: A value that, when multiplied by itself, gives the number under the radical.",
    "∑": "Summation: The addition of a sequence of numbers.",
    "∏": "Product: The multiplication of a sequence of numbers.",
    "∂": "Partial derivative: The derivative of a function of several variables with respect to one variable.",
    "∇": "Nabla or Del: A vector differential operator.",
    "∫": "Integral: In calculus, used to calculate areas, volumes, and other quantities.",
    "∮": "Contour integral: An integral taken along a path in a complex plane.",
    "∝": "Proportional to: Indicates that two values have a constant ratio.",
    "°": "Degree: A unit of measurement for angles or temperature.",
    "⊥": "Perpendicular: Indicates that two lines are at right angles to each other.",
    "∠": "Angle: A figure formed by two rays sharing a common endpoint.",
    "π": "Pi: The ratio of a circle's circumference to its diameter, approximately 3.14159.",
    "ε": "Epsilon: Often used to represent a small positive quantity.",
    "μ": "Mu: Often used to represent the mean of a distribution in statistics.",
    "σ": "Sigma: Often used to represent standard deviation in statistics.",
    "Ω": "Omega: Often used to represent ohms in electrical engineering or the sample space in probability.",
    "α": "Alpha: Often used to represent angular acceleration in physics.",
    "β": "Beta: Often used to represent the standardized regression coefficient in statistics.",
    "γ": "Gamma: Often used to represent the specific weight in physics.",
    "δ": "Delta: Often used to represent a small change in a variable.",
    "θ": "Theta: Often used to represent an angle in geometry.",
    "λ": "Lambda: Often used to represent wavelength in physics.",
    "φ": "Phi: Often used to represent the golden ratio in mathematics.",
    "ψ": "Psi: Often used to represent the wave function in quantum mechanics.",
    "ω": "Omega (lowercase): Often used to represent angular velocity in physics.",
    "ℏ": "Planck constant: A fundamental constant of quantum mechanics.",
    "⟨": "Left angle bracket: Often used in bra-ket notation in quantum mechanics.",
    "⟩": "Right angle bracket: Often used in bra-ket notation in quantum mechanics.",
    "ℒ": "Lagrangian: A function that summarizes the dynamics of a physical system.",
    "ℋ": "Hamiltonian: A function used to describe the total energy of a system.",
    "⊗": "Tensor product: An operation on two tensors that yields a tensor.",
    "†": "Hermitian conjugate: The conjugate transpose of a matrix.",
    "‖": "Norm: A function that assigns a strictly positive length or size to a vector.",
    "⇌": "Equilibrium: Indicates a reversible reaction in chemical equations.",
    "⇋": "Reversible reaction: Indicates a reaction that can proceed in both directions.",
    "∴": "Therefore: Used to indicate that a statement follows logically from previous statements.",
    "⟨|": "Bra: In quantum mechanics, represents a row vector in the dual space of the ket vectors. Part of the bra-ket notation introduced by Paul Dirac.",
    "|⟩": "Ket: In quantum mechanics, represents a column vector in a complex Hilbert space. Part of the bra-ket notation introduced by Paul Dirac.",
    "⟨|⟩": "Braket: In quantum mechanics, represents the inner product of a bra and a ket. Used to calculate expectation values and transition amplitudes.",
}


def notify_and_print(title: str, symbol: str, symbol_name: str) -> None:
    if not notify(title, f"{symbol} {symbol_name}"):
        print(f"Notification failed. {title}: {symbol} {symbol_name}", file=sys.stderr)
    print(f"Copied to clipboard: {symbol} {symbol_name}")


def show_info(rofi: Rofi, symbol: str, selected: str) -> bool:
    info = operator_info.get(
        symbol, "No additional information available for this symbol"
    )
    message = "\n".join(info) if isinstance(info, list) else info
    _, key = rofi.select(
        "Info (Enter to copy, Esc to return):", [symbol], message=message
    )
    if key == 0:
        # User pressed enter, copy the symbol
        subprocess.run(["wl-copy"], input=symbol.encode())
        notify_and_print("Copied to clipboard", symbol, selected.split(" ", 1)[1])
        return False
    else:
        # User pressed Esc, return to main menu
        return True


def operator_info_menu(rofi: Rofi) -> None:
    while True:
        index, key = rofi.select(
            "Select logical operator:", operators, key1=("Alt+i", None)
        )
        selected = operators[index]

        if key == -1:
            break
        elif key == 1:
            # User pressed Alt+i, show additional info
            symbol = selected.split(" ", 1)[0]
            show_info(rofi, symbol, selected)
            continue
        else:
            # User made a selection, copy to clipboard and exit
            symbol = selected.split(" ", 1)[0]
            subprocess.run(["wl-copy"], input=symbol.encode())
            notify_and_print("Copied to clipboard", symbol, selected.split(" ", 1)[1])
            break
    sys.exit(0)
