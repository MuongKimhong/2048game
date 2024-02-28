from typing import Union, Dict

from textual.app import App, ComposeResult
from textual.containers import Container
from textual import events

from components.board import Board
from components.score import Score
from components.logo import Logo
from components.tile import Tile


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


class GameApp(App):
    def __init__(self) -> None:
        self.blocks: Dict[str, Tile] = dict()
        super().__init__()

    def create_blocks(self) -> None:
        ''' 
        notes:
        - when game start, only 2 tiles appear, Tile number 2 and Tile number 4 
        - both tiles appear in random block between block 1 and block 16
        '''
     
        # tile_two_block: int = randrange(self.TOTAL_BLOCKS)
        # tile_four_block: Union[int, None] = None
        # while True:
        #     tile_four_block = randrange(self.TOTAL_BLOCKS)

        #     if tile_four_block != tile_two_block:
        #         break
        tile_two_block = 1
        tile_four_block = 2
        for block in range(self.TOTAL_BLOCKS):
            is_empty: bool = True
            value: int = 0

            if (block + 1) == tile_two_block:
                value = 2
                is_empty = False
            elif (block + 1) == tile_four_block:
                value = 4
                is_empty = False
            elif block + 1 == 3:
                value = 4
                is_empty = False

            tile = Tile(value=value, id=f"block-{block+1}", block_number=block+1, is_empty=is_empty) 
            self.blocks.update({f"{block+1}": tile})

    def on_mount(self, event: events.Mount) -> None:
        self.screen.styles.background = "grey"
        self.create_blocks()

    def compose(self) -> ComposeResult:
        yield UpperContainer()
        yield Board()


if __name__ == "__main__":
    game = GameApp()
    game.run()
