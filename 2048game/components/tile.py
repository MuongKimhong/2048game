from typing import Union, Dict

from textual.widgets import Static
from textual import events, log


class Tile(Static):
    def __init__(self, value: int, id: str, block_number: int, is_empty: bool = True) -> None:
        self.value = value
        self.is_empty = is_empty
        self.block_number = block_number
        super().__init__(id=id)

    def change_value(self, new_value: int) -> None:
        self.value = new_value
        self.is_empty = True if new_value == 0 else False
        self.renderable = str(new_value) if new_value > 0 else ""

    def change_to_empty(self) -> None:
        self.change_value(new_value=0)
        self.set_empty_style()

    def change_to_not_empty(self, new_value: int = 0) -> None:
        self.change_value(new_value=new_value)
        self.set_style()

    def set_color(self, color: str, background: str) -> None:
        self.styles.color = color
        self.styles.background = background

    def set_style(self) -> None:
        self.styles.text_align = "center"
        self.styles.text_style = "bold"
        self.styles.padding = (2, 0) # 2 top, 0 bottom 

        if self.value == 2:
            self.set_color("white", "cadetblue")
        elif self.value == 4:
            self.set_color("white", "darkgoldenrod")
        elif self.value == 8:
            self.set_color("white", "orange")
        elif self.value == 16:
            self.set_color("white", "darkorange")
        elif self.value == 32:
            self.set_color("white", "darksalmon")
        elif self.value == 64:
            self.set_color("white", "darkred")
        elif self.value == 128:
            self.set_color("white", "ansi_blue")
        elif self.value == 256:
            self.set_color("white", "ansi_yellow")
        else:
            self.set_color("white", "coral")

    def set_empty_style(self) -> None: # empty tile
        self.styles.background = "lightgrey"

    def on_mount(self, event: events.Mount) -> None:
        self.styles.height = "100%"
        self.renderable = str(self.value) if self.value > 0 else ""
        self.set_empty_style() if self.is_empty else self.set_style()
