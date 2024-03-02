from textual.widgets import Static
from textual import events, log


class Score(Static):
    DEFAULT_CSS = """
    Score {
        width: 12;   
        height: 7;
        color: white;
        background: maroon;
        text-style: bold;
        text-align: center;
        padding-top: 2;
        margin-left: 28;
    }  
    """

    def on_mount(self, event: events.Mount) -> None:
        self.renderable = "00"

    def update_score(self, sum_value: int) -> None:
        old_score = int(str(self.renderable))
        self.update(str(old_score + sum_value))
