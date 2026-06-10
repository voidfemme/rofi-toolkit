#!/usr/bin/env python3
import argparse
import logging
import shutil
import sys
from rofi import Rofi

from src.utils.notify_send import notify

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(name)s - %(levelname)s - %(message)s",
)


def check_dependencies(programs: list[str]) -> bool:
    missing_deps = [p for p in programs if not shutil.which(p)]

    if missing_deps:
        notify("Missing Dependencies for RofiMultiTool:", ", ".join(missing_deps))
        return False
    return True


def main():
    if not check_dependencies(
        ["rofi", "wl-copy", "bluetoothctl", "nvim", "notify-send", "xdg-open"]
    ):
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Rofi Multitool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("bluetooth")
    subparsers.add_parser("calculator")
    subparsers.add_parser("nether")
    subparsers.add_parser("logical-operators")
    subparsers.add_parser("operator-info")
    subparsers.add_parser("update")

    recents_parser = subparsers.add_parser("recents")
    recents_parser.add_argument("-n", "--count", type=int, default=10, metavar="N")

    keymaps_parser = subparsers.add_parser("nvim-keymaps")
    keymaps_parser.add_argument("-r", "--refresh", action="store_true")
    keymaps_parser.add_argument("-c", "--categories", action="store_true")
    keymaps_parser.add_argument("-f", "--filter", metavar="CATEGORY")
    keymaps_parser.add_argument("-j", "--json", action="store_true")
    keymaps_parser.add_argument("-l", "--list", action="store_true")

    args = parser.parse_args()

    rofi = Rofi()

    match args.command:
        case "bluetooth":
            from src import bluetooth

            bluetooth.bluetooth_menu(rofi)
        case "calculator":
            from src import calculator

            calculator.calculator_menu(rofi)
        case "nether":
            from src import nether

            nether.nether_menu(rofi)
        case "logical-descriptions":
            from src import logical_descriptions

            logical_descriptions.logical_descriptions_menu(rofi)
        case "operator-info":
            from src import operator_info

            operator_info.operator_info_menu(rofi)
        case "recents":
            from src import recents

            recents.recents_menu(rofi, recent_count=args.count)
        case "nvim-keymaps":
            from src import nvim_keymaps

            nvim_keymaps.nvim_keymaps_menu(
                rofi,
                refresh=args.refresh,
                categories=args.categories,
                filter_category=args.filter,
                json_output=args.json,
                list_only=args.list,
            )
        case "update":
            import subprocess
            from pathlib import Path

            # __file__ is main.py, so .parent is the project root
            project_root = Path(__file__).parent
            pull = subprocess.run(
                ["git", "pull"], cwd=project_root, capture_output=True, text=True
            )
            if pull.returncode == 0:
                subprocess.run(
                    ["pip", "install", "-e", ".", "--break-system-packages"],
                    cwd=project_root,
                )
            else:
                print(pull.stderr, file=sys.stderr)
            sys.exit(pull.returncode)


if __name__ == "__main__":
    main()
