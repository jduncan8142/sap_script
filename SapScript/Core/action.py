from typing import Any, Self
from ..Gui.elements import GuiElement


class Actions:
    def __init__(self) -> None:
        self._element: GuiElement | None = None
        self._success: bool | None = None
        self._result: Any | None = None

    def __repr__(self) -> str:
        return f"Action({self._success}, {self._result})"

    def __str__(self) -> str:
        return f"Action({self._success}, {self._result})"

    @staticmethod
    def press(element: GuiElement) -> Self:
        _actions = Actions()
        if not isinstance(element, GuiElement):
            raise ValueError("Invalid element")
        _actions._element = element
        try:
            _actions._element.Press()
            _actions._success = True
            _actions._result = None
        except Exception as e:
            _actions._success = False
            _actions._result = e
        finally:
            return _actions

    @staticmethod
    def set_focus(element: GuiElement) -> Self:
        _actions = Actions()
        if not isinstance(element, GuiElement):
            raise ValueError("Invalid element")
        _actions._element = element
        try:
            _actions._element.Select()
            _actions._success = True
            _actions._result = None
        except Exception as e:
            _actions._success = False
            _actions._result = e
        finally:
            return _actions

    @staticmethod
    def select(element: GuiElement) -> Self:
        _actions = Actions()
        if not isinstance(element, GuiElement):
            raise ValueError("Invalid element")
        _actions._element = element
        try:
            _actions._element.Select()
            _actions._success = True
            _actions._result = None
        except Exception as e:
            _actions._success = False
            _actions._result = e
        finally:
            return _actions

    @staticmethod
    def call_function(element: GuiElement, function: str) -> Self:
        _actions = Actions()
        if not isinstance(element, GuiElement):
            raise ValueError("Invalid element")
        _actions._element = element
        if hasattr(element, function) and callable(element.function):
            try:
                getattr(element, function)()
                _actions._success = True
                _actions._result = None
            except Exception as e:
                _actions._success = False
                _actions._result = e
        else:
            raise ValueError("Invalid function")
        return _actions
