from typing import Optional
import win32com.client  # type: ignore
from dotenv import dotenv_values  # type: ignore
from .result import Result, error_list  # noqa: F401
from ..Gui.elements import GuiElement  # noqa: F401
from ..Gui.vkeys import VKeys  # noqa: F401

sap_connections: list[str] = []
sap_sessions: list[str] = []
sap_windows: list[str] = []


class SAP:
    def __init__(self, sid: str) -> None:
        global sap_connections, sap_sessions, sap_windows
        self.keys: VKeys = VKeys()
        self._config = dotenv_values(".env")
        self.sap_connections: list[str] = sap_connections
        self.sap_sessions: list[str] = sap_sessions
        self.sap_windows: list[str] = sap_windows
        self.errors: list[object] = error_list
        self.sid: str = sid
        self.gui: win32com.client.CDispatch | None = self.get_gui().value
        self.app: win32com.client.CDispatch = self.get_app().value
        self.connection_number: int | None = None
        self.connection: win32com.client.CDispatch | None = self.get_connection().value
        self.session_number: int | None = None
        self.session: win32com.client.CDispatch | None = self.get_session().value
        self.window_number: int | None = None
        self.window: win32com.client.CDispatch | None = self.get_window().value
        self.client: str | None = None
        self.user: str | None = None
        self.current_transaction: str | None = None

    def __repr__(self) -> str:
        return f"SAP({self.sid})"

    def __str__(self) -> str:
        return f"SAP({self.sid})"

    def get_gui(self) -> Result:
        try:
            return Result(value=win32com.client.GetObject("SAPGUI"))
        except Exception as e:
            return Result(error=e, message="Error getting SAP GUI.")

    def get_app(self) -> Result:
        try:
            return Result(value=self.gui.GetScriptingEngine)
        except Exception as e:
            return Result(error=e, message="Error getting SAP GUI scripting engine.")

    def get_connection(self) -> Result:
        if len(self.sap_connections) == 0:
            try:
                self.sap_connections = self.app.connections
            except Exception as _:
                pass
        try:
            if len(self.sap_connections) > 0:
                for _connection in self.sap_connections:
                    if _connection.description == self.sid:
                        self.connection_number = _connection.Id[-2]
                        return Result(value=_connection)
            else:
                _connection = self.app.OpenConnection(self.sid, True)
                self.connection_number = _connection.Id[-2]
                self.sap_connections = self.app.connections
                return Result(value=_connection)
        except Exception as e:
            return Result(error=e, message="Error getting connection.")

    def get_session(self, session_number: Optional[int | None] = None) -> Result:
        if len(self.sap_sessions) == 0:
            try:
                self.sap_sessions = self.connection.sessions
            except Exception as _:
                pass
        if session_number is not None:
            if len(self.sap_sessions) >= self.session_number:
                self.session_number = session_number
        else:
            self.session_number = 0
        try:
            return Result(value=self.connection.children(self.session_number))
        except Exception as e:
            return Result(error=e, message="Error getting session.")

    def get_window(self, window_number: Optional[int | None] = None) -> Result:
        if window_number is not None:
            self.window_number = window_number
        else:
            self.window_number = 0
        try:
            _window = self.session.findById(f"wnd[{self.window_number}]")
            if _window in self.sap_windows:
                return Result(value=_window)
            else:
                self.sap_windows.append(_window)
                return Result(value=_window)
        except Exception as e:
            return Result(error=e, message="Error getting window.")

    def get_session_info(self) -> Result:
        try:
            return Result(value=self.session.Info)
        except Exception as e:
            return Result(error=e, message="Error getting session info.")

    def start_transaction(self, value: str) -> Result:
        try:
            self.session.StartTransaction(Transaction=value)
            _result = Result(message=f"Transaction {value} started.")
            self.current_transaction = value
            return _result
        except Exception as e:
            return Result(error=e, message=f"Error starting transaction {value}.")

    def end_transaction(self) -> Result:
        try:
            self.session.EndTransaction()
            _result = Result(message=f"Transaction {self.current_transaction} ended.")
            self.current_transaction = None
            return _result
        except Exception as e:
            return Result(error=e, message="Error ending transaction.")

    def close_connection(self) -> Result:
        try:
            self.connection.Close()
            _result = Result(message="Connection closed.")
            return _result
        except Exception as e:
            return Result(error=e, message="Error closing connection.")

    def close_session(self) -> Result:
        try:
            self.session.Close()
            _result = Result(message="Session closed.")
            return _result
        except Exception as e:
            return Result(error=e, message="Error closing session.")

    def close_window(self) -> Result:
        try:
            self.window.Close()
            _result = Result(message="Window closed.")
            return _result
        except Exception as e:
            return Result(error=e, message="Error closing window.")

    def send_key(self, key: str) -> Result:
        try:
            self.window.sendVKey(self.keys.get_key_id(key))
            return Result(message=f"Key {key} sent.")
        except Exception as e:
            return Result(error=e, message=f"Error sending key {key}.")

    def get_element(self, id: str) -> Result:
        try:
            return Result(value=GuiElement(element=self.session.findById(id)))
        except Exception as e:
            return Result(error=e, message="Error getting element.")
