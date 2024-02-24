from textual.widgets import Static
from textual import events


class Score(Static):
    DEFAULT_CSS = """
    Score {
        width: 12;   
        height: 7;
        color: white;
        background: ansi_white;
        text-style: bold;
        text-align: center;
        padding-top: 2;
        margin-left: 28;
    }  
    """
    total_score = 0

    def on_mount(self, event: events.Mount) -> None:
        self.renderable = "00"