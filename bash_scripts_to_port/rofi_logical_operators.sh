#!/bin/bash

# Array of logical operators
operators=(
    "∧ (AND)"
    "∨ (OR)"
    "¬ (NOT)"
    "⊕ (XOR)"
    "→ (IMPLIES)"
    "↔ (IFF)"
    "∀ (FOR ALL)"
    "∃ (EXISTS)"
    "∈ (ELEMENT OF)"
    "∉ (NOT ELEMENT OF)"
    "⊂ (SUBSET OF)"
    "⊃ (SUPERSET OF)"
    "∪ (UNION)"
    "∩ (INTERSECTION)"
    "∅ (EMPTY SET)"
    "ℕ (NATURAL NUMBERS)"
    "ℤ (INTEGERS)"
    "ℚ (RATIONAL NUMBERS)"
    "ℝ (REAL NUMBERS)"
    "ℂ (COMPLEX NUMBERS)"
    "∞ (INFINITY)"
    "≈ (APPROXIMATELY EQUAL)"
    "≠ (NOT EQUAL)"
    "≤ (LESS THAN OR EQUAL)"
    "≥ (GREATER THAN OR EQUAL)"
    "± (PLUS-MINUS)"
    "× (MULTIPLICATION)"
    "÷ (DIVISION)"
    "√ (SQUARE ROOT)"
    "∑ (SUMMATION)"
    "∏ (PRODUCT)"
    "∂ (PARTIAL DERIVATIVE)"
    "∇ (NABLA/DEL)"
    "∫ (INTEGRAL)"
    "∮ (CONTOUR INTEGRAL)"
    "∝ (PROPORTIONAL TO)"
    "° (DEGREE)"
    "⊥ (PERPENDICULAR)"
    "∠ (ANGLE)"
    "π (PI)"
    "ε (EPSILON)"
    "μ (MU)"
    "σ (SIGMA)"
    "Ω (OMEGA)"
    "α (ALPHA)"
    "β (BETA)"
    "γ (GAMMA)"
    "δ (DELTA)"
    "θ (THETA)"
    "λ (LAMBDA)"
    "φ (PHI)"
    "ψ (PSI)"
    "ω (OMEGA LOWERCASE)"
    "ℏ (PLANCK CONSTANT)"
    "⟨ (LEFT ANGLE BRACKET)"
    "⟩ (RIGHT ANGLE BRACKET)"
    "ℒ (SCRIPT L - LAGRANGIAN)"
    "ℋ (SCRIPT H - HAMILTONIAN)"
    "⊗ (TENSOR PRODUCT)"
    "⊕ (DIRECT SUM)"
    "† (DAGGER - HERMITIAN CONJUGATE)"
    "‖ (NORM)"
    "→ (VECTOR ARROW)"
    "⇌ (EQUILIBRIUM)"
    "⇋ (REVERSIBLE REACTION)"
  )

# Use rofi to display the list and get user selection
selected=$(printf '%s\n' "${operators[@]}" | rofi -dmenu -i -p "Select logical operator:")

# Extract the symbol from the selection (everything before the space)
symbol=$(echo "$selected" | cut -d' ' -f1)

# Copy the symbol to the clipboard using xclip
echo -n "$symbol" | wl-copy

# Optionally, provide feedback
notify-send "Copied to clipboard" "$symbol"
