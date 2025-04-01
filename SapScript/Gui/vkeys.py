from enum import Enum, auto


class VKeys:
    """
    VKeys - Virtual Keys Enum
    """

    def __init__(self) -> None:
        self.vkeys = [
            "ENTER",
            "F1",
            "F2",
            "F3",
            "F4",
            "F5",
            "F6",
            "F7",
            "F8",
            "F9",
            "F10",
            "F11",
            "F12",
            None,
            "SHIFT+F2",
            "SHIFT+F3",
            "SHIFT+F4",
            "SHIFT+F5",
            "SHIFT+F6",
            "SHIFT+F7",
            "SHIFT+F8",
            "SHIFT+F9",
            "CTRL+SHIFT+0",
            "SHIFT+F11",
            "SHIFT+F12",
            "CTRL+F1",
            "CTRL+F2",
            "CTRL+F3",
            "CTRL+F4",
            "CTRL+F5",
            "CTRL+F6",
            "CTRL+F7",
            "CTRL+F8",
            "CTRL+F9",
            "CTRL+F10",
            "CTRL+F11",
            "CTRL+F12",
            "CTRL+SHIFT+F1",
            "CTRL+SHIFT+F2",
            "CTRL+SHIFT+F3",
            "CTRL+SHIFT+F4",
            "CTRL+SHIFT+F5",
            "CTRL+SHIFT+F6",
            "CTRL+SHIFT+F7",
            "CTRL+SHIFT+F8",
            "CTRL+SHIFT+F9",
            "CTRL+SHIFT+F10",
            "CTRL+SHIFT+F11",
            "CTRL+SHIFT+F12",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "CTRL+E",
            "CTRL+F",
            "CTRL+A",
            "CTRL+D",
            "CTRL+N",
            "CTRL+O",
            "SHIFT+DEL",
            "CTRL+INS",
            "SHIFT+INS",
            "ALT+BACKSPACE",
            "CTRL+PAGEUP",
            "PAGEUP",
            "PAGEDOWN",
            "CTRL+PAGEDOWN",
            "CTRL+G",
            "CTRL+R",
            "CTRL+P",
            "CTRL+B",
            "CTRL+K",
            "CTRL+T",
            "CTRL+Y",
            "CTRL+X",
            "CTRL+C",
            "CTRL+V",
            "SHIFT+F10",
            None,
            None,
            "CTRL+#",
        ]

    def get_key_id(self, key: str) -> int:
        _id = None
        _key: str = str(key.strip())
        if not _key.isdigit():
            _search_comb: str = _key.upper()
            _search_comb = _search_comb.replace(" ", "")
            _search_comb = _search_comb.replace("CONTROL", "CTRL")
            _search_comb = _search_comb.replace("DELETE", "DEL")
            _search_comb = _search_comb.replace("INSERT", "INS")
            try:
                _id = self.vkeys.index(_search_comb)
            except ValueError:
                if _search_comb == "CTRL+S":
                    _id = 11
                elif _search_comb == "ESC":
                    _id = 12
        return _id
