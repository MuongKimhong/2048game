from typing import Union, Dict

from textual.widgets import Static
from textual import events, log


class Tile(Static):
    def __init__(self, value: int, id: str, block_number: int, is_empty: bool = True) -> None:
        self.value = value
        self.is_empty = is_empty
        self.block_number = block_number
        super().__init__(id=id)

    def change_to_empty(self) -> None:
        self.value = 0
        self.is_empty = True
        self.renderable = ""
        self.set_empty_style()

    def change_to_not_empty(self, new_value: int = 0) -> None:
        self.value = new_value if new_value > 0 else self.value
        self.is_empty = False
        self.renderable = f"{self.value}"
        self.set_style()

    def set_style(self) -> None:
        self.styles.color = "white"
        self.styles.text_align = "center"
        self.styles.background = "darkorange"
        self.styles.text_style = "bold"
        self.styles.padding = (2, 0) # 2 top, 0 bottom 

    def set_empty_style(self) -> None: # empty tile
        self.styles.background = "lightgrey"

    def on_mount(self, event: events.Mount) -> None:
        self.styles.height = "100%"
        self.renderable = str(self.value) if self.value > 0 else ""
        self.set_empty_style() if self.is_empty else self.set_style()
