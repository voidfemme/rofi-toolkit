from rofi import Rofi
from src.utils.notify_send import notify
from typing import Literal
import logging
import re
import subprocess
import sys
import time

# Text Strings
SCAN_AGAIN = "== scan again =="

logger = logging.getLogger(__name__)


class RofiBluetooth:
    def __init__(
        self,
        rofi: Rofi,
        show_scanned: bool = False,
        show_saved: bool = True,
        scan_time: int = 5,
    ) -> None:
        self.show_scanned = show_scanned
        self.show_saved = show_saved
        self.scan_time = scan_time
        self.rofi = rofi
        logger.debug("== RofiBluetooth is initialized ==")
        logger.debug(f"show_scanned = {self.show_scanned}")
        logger.debug(f"show_saved = {self.show_saved}")
        logger.debug(f"scan_time = {self.scan_time}\n")

    def _strip_ansi(self, text: str | bytes | None) -> str:
        logger.debug(f"== RofiBluetooth._strip_ansi(self, text={text})\n")
        return re.sub(r"\x1b\[[0-9;]*m", "", text.__str__())

    def scan_devices(self) -> list[str]:
        logger.debug("== RofiBluetooth.scan_devices(self) ==\n")
        try:
            result = subprocess.run(
                ["bluetoothctl", "scan", "on"],
                capture_output=True,
                timeout=self.scan_time,
            )
            logger.debug(f"    == Subprocess result ==\n{result}\n")
            stdout = self._strip_ansi(result.stdout)
            lines = [line for line in stdout.splitlines() if "[NEW] Device" in line]
            lines = [line.replace("[NEW] Device ", "") for line in lines]
            return lines

        except subprocess.TimeoutExpired as e:
            logger.error(f"    == Bluetooth Subprocess Timeout Expired ==\n{e}\n")
            partial = self._strip_ansi(e.stdout or "")
            lines = [line for line in partial.splitlines() if "[NEW] Device" in line]
            lines = [line.replace("[NEW] Device ", "") for line in lines]
            return lines

    def get_saved_devices(self) -> list[str]:
        logger.debug("== RofiBluetooth.get_saved_devices(self) ==\n")
        result = subprocess.run(
            ["bluetoothctl", "devices"],
            capture_output=True,
        )
        logger.debug(f"    == Subprocess result ==\n{result}\n")
        lines = [line for line in result.stdout.decode("utf-8").splitlines()]
        logger.debug("    get_saved_devices() lines:")
        for line in lines:
            logger.debug(f"    {line}")
        logger.debug("\n")
        return lines

    def annotate_devices(self, devices: list[str]) -> list[str]:
        logger.debug(f"== RofiBluetooth.annotate_devices() ==\n")
        logger.debug("ARGS:")
        logger.debug("    devices=")
        annotated_devices = []
        for device in devices:
            logger.debug(f"    {device}")

        for device in devices:
            logger.debug(f"    == Device: {device} ==")
            if not device:
                continue

            parts = device.split(" ")
            mac = parts[1]
            name = " ".join(parts[2:])

            info = subprocess.run(["bluetoothctl", "info", mac], capture_output=True)
            info_text = info.stdout.decode("utf-8")
            logger.debug(f"    == info_text ==")
            logger.debug(f"    {info_text}\n")

            if re.search(r"Connected: yes", info_text):
                annotated_devices.append(f"{mac} {name} (connected)")
            elif re.search(r"Paired: yes", info_text):
                annotated_devices.append(f"{mac} {name} (disconnected)")
            else:
                annotated_devices.append(f"{mac} {name} (new)")

        return annotated_devices

    def dedupe_devices(self, devices: list[str]) -> list[str]:
        logger.debug(f"RofiBluetooth.dedupe_devices(\nself,\ndevices={devices}\n)\n")
        seen = set()
        result = []
        for device in devices:
            key = device.split(" ")[0]
            logger.debug(key)
            if key not in seen:
                seen.add(key)
                result.append(device)
                logger.debug(f"    key = {key}")
                logger.debug(f"    device = {device}")
        return result

    def build_device_list(self) -> list[str]:
        logger.debug(f"RofiBluetooth.build_device_list(self)\n")

        scanned = []
        saved = []
        options = []

        logger.debug(f"self.show_scanned = {self.show_scanned}")
        logger.debug(f"self.show_saved = {self.show_saved}")

        if self.show_scanned:
            scanned = self.annotate_devices(self.scan_devices())
            logger.debug(f"== scanned ==\n{scanned}\n")
        if self.show_saved:
            saved = self.annotate_devices(self.get_saved_devices())
            logger.debug(f"== saved ==\n{saved}\n")

        if self.show_scanned and self.show_saved:
            options.extend(scanned)
            options.append(SCAN_AGAIN)
            options.extend(self.dedupe_devices(saved))
        elif self.show_scanned:
            options.extend(scanned)
            options.append(SCAN_AGAIN)
        else:
            options.extend(saved)

        logger.debug("== options ==")
        if len(options) > 0:
            logger.debug(f"`options` contains {len(options)} items\n")
        else:
            logger.debug("No options exist in the list")
            for option in options:
                logger.debug(f"option: {option}")

        return options

    def connect_device(self, mac: str) -> None:
        logger.debug(f"RofiBluetooth.connect_device(self, mac={mac})\n")
        # Pairing Failed
        info_result = subprocess.run(["bluetoothctl", "info", mac], capture_output=True)
        info_stdout = info_result.stdout.decode("utf-8")
        if not re.search(r"Paired: yes", info_stdout):
            pair_result = subprocess.run(
                ["bluetoothctl", "pair", mac], capture_output=True
            )
            if pair_result.returncode != 0:
                notify("pairing failed", "bluetooth error")
                sys.exit(1)

        # Connection Failed
        connection_result = subprocess.run(
            ["bluetoothctl", "connect", mac], capture_output=True
        )
        connection_stdout = connection_result.stdout.decode("utf-8")
        if mac not in connection_stdout:
            notify("connection failed", "bluetooth error")
            sys.exit(1)

    def disconnect_device(self, mac: str) -> None:
        logger.debug(f"RofiBluetooth.disconnect_device(self, mac={mac})\n")
        disconnect_result = subprocess.run(
            ["bluetoothctl", "disconnect", mac], capture_output=True
        )
        disconnect_stdout = disconnect_result.stdout.decode("utf-8")
        if mac not in disconnect_stdout:
            notify("disconnect failed", "bluetooth error")


def bluetooth_menu(rofi: Rofi):
    bt = RofiBluetooth(rofi, show_scanned=True)
    while True:
        devices = bt.build_device_list()
        logger.debug(f"Devices:\n{devices}\n")

        index, key = bt.rofi.select("Bluetooth Devices", devices)
        logger.debug(f"Index: {index}, Key: {key}\n")

        # If the user closes the window without making a selection, exit
        if index == -1:
            sys.exit(0)

        choice = devices[index]
        logger.debug(f"choice: {choice}")

        if choice == SCAN_AGAIN:
            logger.debug("rescanning")
            continue

        mac = choice.split(" ")[0]
        logger.debug(f"mac: {mac}")

        if "(connected)" in choice:
            bt.disconnect_device(mac)
        else:
            bt.connect_device(mac)

        time.sleep(1)

        # gather the string after the mac into a single string
        human_readable_name = " ".join(choice.split(" ")[1:-1])
        logger.debug(f"human readable name: {human_readable_name}")

        status_result = subprocess.run(
            ["bluetoothctl", "info", mac], capture_output=True
        )
        device_status = status_result.stdout.decode("utf-8")

        if "Connected: yes" in device_status:
            notify(human_readable_name, "Bluetooth Connected")
        else:
            notify(human_readable_name, "Bluetooth Disconnected")
        break
