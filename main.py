from textual.app import App, ComposeResult
from textual.containers import Container
from textual import events

from components.board import Board
from components.score import Score
from components.logo import Logo


class UpperContainer(Container, can_focus=True):
    DEFAULT_CSS = """
    UpperContainer {
        layout: horizontal;
        padding: 1;
        height: 7;
        align: center middle;
    } 
    """

    def compose(self) -> ComposeResult:
        yield Logo()
        yield Score()


class BoardContainer(Container, can_focus=True):
    DEFAULT_CSS = """
    BoardContainer {
        layout: grid;
        height: 28;
        align: center middle;
    } 
    """

    def compose(self) -> ComposeResult:
        yield Board()


class GameApp(App):
    def on_mount(self, event: events.Mount) -> None:
        self.screen.styles.background = "grey"

    def compose(self) -> ComposeResult:
        yield UpperContainer()
        yield BoardContainer()


if __name__ == "__main__":
    game = GameApp()
    game.run()
