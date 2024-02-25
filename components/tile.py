from textual.widgets import Static
from textual import events


class Tile(Static):
    def __init__(self, value: int | None, id: str, is_empty: bool = True) -> None:
        self.value = value
        self.is_empty = is_empty
        self.can_move = {
            "right": False,
            "left" : False,
            "up"   : False,
            "down" : False
        }
        super().__init__(id=id)

    def update_can_move(self, moved_direction: str) -> None:
        for key in self.can_move:
            self.can_move[key] = True if key == moved_direction else False

    def change_to_empty(self) -> None:
        self.renderable = ""
        self.styles.background = "lightgrey"

    def change_to_not_empty(self) -> None:
        self.renderable = f"{self.value}"
        self.styles.color = "white"
        self.styles.text_align = "center"
        self.styles.background = "darkorange"
        self.styles.text_style = "bold"
        self.styles.padding = (2, 0) # 2 top, 0 bottom

    def on_mount(self, event: events.Mount) -> None:
        self.styles.height = "100%"

        if self.is_empty:
            self.change_to_empty()
        else:
            self.change_to_not_empty()
