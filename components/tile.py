from textual.widgets import Static
from textual import events


class Tile(Static):
    def __init__(self, value: int | None, id: str, is_empty: bool = True) -> None:
        self.value = value
        self.is_empty = is_empty
        super().__init__(id=id)

    def on_mount(self, event: events.Mount) -> None:
        self.styles.height = "100%"

        if self.is_empty:
            self.styles.background = "lightgrey"
        else:
            self.renderable = f"{self.value}"
            self.styles.color = "white"
            self.styles.text_align = "center"
            self.styles.background = "darkorange"
            self.styles.text_style = "bold"
            self.styles.padding = (2, 0) # 2 top, 0 bottom