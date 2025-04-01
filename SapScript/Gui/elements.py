from enum import Enum, auto
from typing import Any, Generator
import win32com.client  # type: ignore


class GuiElement:
    def __init__(self, element: win32com.client.CDispatch) -> None:
        self._element: win32com.client.CDispatch | None = element

    def __repr__(self) -> str:
        return f"GuiElement({self._element})"

    def __str__(self) -> str:
        return f"GuiElement({self._element})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GuiElement):
            return self._element == other._element
        return False

    @property
    def element(self) -> win32com.client.CDispatch:
        return self._element

    @element.setter
    def element(self, value: win32com.client.CDispatch) -> None:
        self._element = value

    @property
    def id(self) -> str:
        return self._element.Id

    @property
    def type(self) -> str:
        return self._element.Type

    @property
    def changeable(self) -> bool:
        return self._element.Changeable

    @property
    def container_type(self) -> bool:
        return self._element.ContainerType

    @property
    def name(self) -> str:
        return self._element.Name

    @property
    def text(self) -> str:
        return self._element.Text

    @text.setter
    def text(self, value: str) -> None:
        if self.changeable:
            self._element.Text = value
        else:
            raise ValueError("Element is not changeable")

    @property
    def tooltip(self) -> str:
        return self._element.Tooltip

    @property
    def screen_left(self) -> int:
        return self._element.ScreenLeft

    @property
    def screen_top(self) -> int:
        return self._element.ScreenTop

    @property
    def left(self) -> int:
        return self._element.Left

    @property
    def top(self) -> int:
        return self._element.Top

    @property
    def width(self) -> int:
        return self._element.ScreenWidth

    @property
    def height(self) -> int:
        return self._element.ScreenHeight

    @property
    def handle(self) -> int:
        return self._element.Handle

    @property
    def icon_name(self) -> str:
        return self._element.IconName

    @property
    def key(self) -> str:
        return self._element.Key

    @property
    def parent(self) -> win32com.client.CDispatch:
        return self._element.Parent

    @property
    def children(self) -> list[win32com.client.CDispatch]:
        return self._element.Children


class TextElements(Enum):
    """
    TextElements - Enum for Text Elements
    """

    GuiTextField = auto()
    GuiCTextField = auto()
    GuiPasswordField = auto()
    GuiLabel = auto()
    GuiTitlebar = auto()
    GuiStatusbar = auto()
    GuiButton = auto()
    GuiTab = auto()
    GuiShell = auto()
    GuiStatusPane = auto()


class Table(GuiElement):
    """
    Table - Class for SAP GUI Table Elements

    Represents SAP GUI Table control objects with methods and properties
    for interacting with table data, rows, and columns.
    """

    def __init__(self, element: GuiElement) -> None:
        super().__init__(element.element)

    @property
    def rows_count(self) -> int:
        """Returns the total number of rows in the table"""
        return self._element.RowCount

    @property
    def columns_count(self) -> int:
        """Returns the total number of columns in the table"""
        return self._element.ColumnCount

    @property
    def visible_row_count(self) -> int:
        """Returns the number of visible rows in the table"""
        return self._element.VisibleRowCount

    @property
    def column_order(self) -> list[str]:
        """Returns the current column order"""
        return [x for x in self._element.ColumnOrder]

    @property
    def selected_rows(self) -> list[int]:
        """Returns the currently selected rows as a list of row indices"""
        # The SelectedRows property returns a string with comma-separated row indices
        selected = self._element.SelectedRows
        if not selected:
            return []
        return [int(idx) for idx in selected.split(",")]

    @property
    def selected_cell(self) -> tuple[int, int]:
        """Returns the currently selected cell as (row, column)"""
        return (self._element.SelectedRow, self._element.SelectedColumn)

    def get_cell_value(self, row: int, col: int) -> str:
        """
        Gets the value of a cell at the specified row and column

        Args:
            row: Zero-based row index
            col: Zero-based column index

        Returns:
            The cell value as a string
        """
        return self._element.GetCellValue(row, col)

    def set_cell_value(self, row: int, col: int, value: str) -> None:
        """
        Sets the value of a cell at the specified row and column

        Args:
            row: Zero-based row index
            col: Zero-based column index
            value: The value to set

        Raises:
            ValueError: If the table is not changeable
        """
        if self.changeable:
            self._element.ModifyCell(row, col, value)
        else:
            raise ValueError("Table is not changeable")

    def select_row(self, row: int) -> None:
        """
        Selects a specific row

        Args:
            row: Zero-based row index to select
        """
        self._element.SelectedRows = str(row)

    def select_rows(self, rows: list[int]) -> None:
        """
        Selects multiple rows

        Args:
            rows: List of zero-based row indices to select
        """
        self._element.SelectedRows = ",".join(str(row) for row in rows)

    def select_all_rows(self) -> None:
        """Selects all rows in the table"""
        self._element.SelectAll()

    def clear_selection(self) -> None:
        """Clears any selection in the table"""
        self._element.SelectedRows = ""

    def get_column_titles(self) -> list[str]:
        """
        Returns the titles of all columns

        Returns:
            A list of column titles as strings
        """
        return [self._element.GetDisplayedColumnTitle(i) for i in self._element.ColumnOrder]

    def scroll_to_row(self, row: int) -> None:
        """
        Scrolls the table to make the specified row visible

        Args:
            row: Zero-based row index to scroll to
        """
        if hasattr(self._element, "VerticalScrollbar"):
            self._element.VerticalScrollbar.Position = row
        else:
            # Alternative method if no scrollbar is available
            self._element.FirstVisibleRow = row

    def double_click_cell(self, row: int, col: int) -> None:
        """
        Double-clicks a cell at the specified row and column

        Args:
            row: Zero-based row index
            col: Zero-based column index
        """
        self._element.SetCurrentCell(row, col)
        self._element.DoubleClick()

    def press_button(self, row: int, col: int) -> None:
        """
        Presses a button in a cell at the specified row and column

        Args:
            row: Zero-based row index
            col: Zero-based column index
        """
        self._element.pressButton(row, col)

    def get_row_data(self, row: int) -> dict[str, str]:
        """
        Gets all cell values for a row as a dictionary

        Args:
            row: Zero-based row index

        Returns:
            Dictionary with column titles as keys and cell values as values
        """
        result = {}
        column_titles = self._element.ColumnOrder
        for col in range(self.columns_count):
            result[column_titles[col]] = self.get_cell_value(row=row, col=column_titles[col])
        return result

    def get_column_data(self, col: int) -> list[str]:
        """
        Gets all cell values for a column

        Args:
            col: Zero-based column index

        Returns:
            List of cell values in the column
        """
        return [self.get_cell_value(row, col) for row in range(self.rows_count)]

    def find_row_by_value(self, col: int, value: str) -> int:
        """
        Finds the first row that has the specified value in the specified column

        Args:
            col: Zero-based column index to search in
            value: Value to search for

        Returns:
            Zero-based row index or -1 if not found
        """
        for row in range(self.rows_count):
            if self.get_cell_value(row, col) == value:
                return row
        return -1

    def __iter__(self) -> Generator["TableRow", Any, None]:
        """
        Enables iterating over the table rows with support for dot notation column access

        Yields:
            TableRow: Row wrapper with dot notation access to columns

        Example:
            ```python
            for row in table:
                print(row.ColumnName)  # Access column data using dot notation
            ```
        """
        for row_index in range(self.rows_count):
            yield TableRow(self, row_index)

    def get_header_widths(self) -> list[dict[str, int]]:
        """
        Returns the widths of each column header

        Returns:
            List of widths for each column header
        """
        return [{c: self._element.GetCellWidth(0, c)} for c in self.column_order]

    def get_table_width(self) -> int:
        """
        Returns the total width of the table
        """
        column_widths: list = []
        for x in self.get_header_widths():
            column_widths.extend(x.values())
        return sum(column_widths) + len(column_widths) - 1

    def pprint(self) -> None:
        """
        Pretty prints the table data with headers and rows

        Example:
            ```python
            table.pprint()
            ```
        """
        headers = self.get_column_titles()
        print(" | ".join(headers))
        print("-" * self.get_table_width())
        row_data: list[dict] = [self.get_row_data(i) for i in range(self.rows_count)]
        for row in row_data:
            print(" | ".join([str(v) for _, v in row.items()]))
        print("-" * self.get_table_width())


class TableRow:
    """
    TableRow - Represents a row in a Table with dot notation access to columns

    This class provides dot notation access to column values for a specific row.
    """

    def __init__(self, table: Table, row_index: int) -> None:
        self._table = table
        self._row_index = row_index
        self._column_titles = table.get_column_titles()

    def __getattr__(self, name: str) -> str:
        """
        Allows accessing column values using dot notation

        Args:
            name: The column name to access

        Returns:
            The cell value as a string

        Raises:
            AttributeError: If the column name doesn't exist
        """
        try:
            col_index = self._column_titles.index(name)
            return self._table.get_cell_value(self._row_index, col_index)
        except ValueError:
            raise AttributeError(
                f"'TableRow' object has no attribute '{name}'. Available columns: {', '.join(self._column_titles)}"
            )

    def __repr__(self) -> str:
        return f"TableRow({self._row_index})"

    def __str__(self) -> str:
        return f"Row {self._row_index}: {self._table.get_row_data(self._row_index)}"
