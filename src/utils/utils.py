import subprocess
from src.notify_send import notify


def copy_to_clipboard(content: str) -> None:
    subprocess.run(
        ["xclip", "-selection", "clipboard"],
        input=content.encode(),
    )
    notify("Calculator", f"Copied to clipboard: {content}")
