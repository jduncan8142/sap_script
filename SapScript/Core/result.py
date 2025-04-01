from typing import Any, Optional


error_list: list[object] = []


class Result:
    def __init__(
        self,
        value: Optional[Any] = None,
        message: Optional[str] = None,
        error: Optional[object] = None,
    ) -> None:
        global error_list
        self.value: Any = value if value is not None else None
        self.message: str | None = message if message is not None else None
        self.error: object | None = error if error is not None else None
        self.ok: bool = True if error is None else False
        if not self.ok:
            error_list.append(self.error)
