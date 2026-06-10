# src/nether.py
from rofi import Rofi
from src.utils.notify_send import notify
import subprocess


def process_coordinates(coordinates: str) -> tuple[int, int]:
    # Remove any spaces and replace "/" or "," with space
    input = coordinates.replace(" ", "").translate(str.maketrans("/,", " "))

    # Read the two numbers
    parts = input.split()
    if len(parts) != 2:
        raise ValueError("expected exactly 2 coordinates")
    x, y = int(parts[0]), int(parts[1])

    nether_x = int(x / 8)
    nether_y = int(y / 8)
    return nether_x, nether_y


def nether_menu(rofi: Rofi):
    input = rofi.integer_entry("Enter coordinates (x,y):")

    if input:
        try:
            result = f"{process_coordinates(input)}"

            subprocess.run(["wl-copy"], input=result)

            rofi.select("Result", [result, "(Copied to clipboard)"])
        except ValueError as e:
            notify("Error", f"{input}\n{e}")
