# src/recents.py
import sys
from rofi import Rofi
from pathlib import Path
import subprocess
import os
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


def recents_menu(
    rofi: Rofi,
    recent_count: int = 10,
) -> None:
    xbel_path = Path.home() / ".local/share/recently-used.xbel"
    tree = ET.parse(xbel_path)
    root = tree.getroot()

    bookmarks = root.findall("bookmark")
    bookmarks.sort(key=lambda b: b.get("modified", ""), reverse=True)

    files = []
    for bookmark in bookmarks[:recent_count]:
        href = bookmark.get("href", "")
        if href.startswith("file://"):
            files.append(href[7:])

    index, key = rofi.select("Open Recent File:", files)
    if index == -1:
        sys.exit(0)
    selected = files[index]

    subprocess.run(["xdg-open", str(selected)])
