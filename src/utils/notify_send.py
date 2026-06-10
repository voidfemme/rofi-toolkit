import subprocess
from typing import Literal

UrgencyLevel = Literal["low", "normal", "critical"]
HintType = Literal["int", "double", "string", "byte"]


class Notification:
    def __init__(
        self,
        summary: str,
        body: str = "",
        app_name: str = "",
        urgency: UrgencyLevel = "normal",
        icon: str = "",
        expire_time: int | None = None,
        replace_id: int | None = None,
        categories: list[str] | None = None,
        hints: list[tuple[HintType, str, str]] | None = None,
        actions: list[tuple[str, str]] | None = None,
        transient: bool = False,
        print_id: bool = False,
        wait: bool = False,
    ) -> None:
        self.summary = summary
        self.body = body
        self.app_name = app_name
        self.urgency = urgency
        self.icon = icon
        self.expire_time = expire_time
        self.replace_id = replace_id
        self.categories = categories or []
        self.hints = hints or []
        self.actions = actions or []
        self.transient = transient
        self.print_id = print_id
        self.wait = wait

    def _build_cmd(self) -> list[str]:
        cmd = ["notify-send"]

        if self.app_name:
            cmd += ["--app-name", self.app_name]
        if self.urgency != "normal":
            cmd += ["--urgency", self.urgency]
        if self.icon:
            cmd += ["--icon", self.icon]
        if self.expire_time is not None:
            cmd += ["--expire-time", str(self.expire_time)]
        if self.replace_id is not None:
            cmd += ["--replace-id", str(self.replace_id)]
        if self.categories:
            cmd += ["--category", ",".join(self.categories)]
        for hint_type, name, value in self.hints:
            cmd += ["--hint", f"{hint_type}:{name}:{value}"]
        for name, label in self.actions:
            cmd += ["--action", f"{name}={label}"]
        if self.transient:
            cmd.append("--transient")
        if self.print_id:
            cmd.append("--print-id")
        if self.wait or self.actions:
            cmd.append("--wait")

        cmd.append(self.summary)
        if self.body:
            cmd.append(self.body)

        return cmd

    def send(self) -> bool:
        result = subprocess.run(self._build_cmd(), capture_output=True)
        return result.returncode == 0


def notify(
    summary: str,
    body: str = "",
    app_name: str = "",
    urgency: UrgencyLevel = "normal",
    icon: str = "",
    expire_time: int | None = None,
    replace_id: int | None = None,
    categories: list[str] | None = None,
    hints: list[tuple[HintType, str, str]] | None = None,
    actions: list[tuple[str, str]] | None = None,
    transient: bool = False,
    print_id: bool = False,
    wait: bool = False,
) -> bool:
    return Notification(
        summary,
        body,
        app_name,
        urgency,
        icon,
        expire_time,
        replace_id,
        categories,
        hints,
        actions,
        transient,
        print_id,
        wait,
    ).send()
