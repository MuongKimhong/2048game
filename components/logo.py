from textual.widgets import Static
from textual import events


class Logo(Static):
    DEFAULT_CSS = """
    Logo {
        width: 12;   
        height: 7;
        color: white;
        background: goldenrod;
        text-style: bold;
        text-align: center;
        padding-top: 2;
        margin-right: 28;
    }  
    """

    def on_mount(self, event: events.Mount) -> None:
        self.renderable = "2048"