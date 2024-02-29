from typing import Union, Dict
from random import randrange

from textual.app import App, ComposeResult
from textual.containers import Container
from textual import events, log

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
        self.all_move_directions: list[str] = ["right", "left", "up", "down"]
        self.TOTAL_BLOCKS: int = 16
        super().__init__()

    def create_blocks(self) -> None:
        ''' 
        notes:
        - when game start, only 2 tiles appear, Tile number 2 and Tile number 4 
        - both tiles appear in random block between block 1 and block 16
        '''
     
        tile_two_block: int = randrange(self.TOTAL_BLOCKS)
        tile_four_block: Union[int, None] = None
        while True:
            tile_four_block = randrange(self.TOTAL_BLOCKS)

            if tile_four_block != tile_two_block:
                break

        for block in range(self.TOTAL_BLOCKS):
            value: int = 0

            if (block + 1) == tile_two_block:
                value = 2
            elif (block + 1) == tile_four_block:
                value = 4

            is_empty: bool = True if value == 0 else False
            tile = Tile(value=value, id=f"block-{block+1}", block_number=block+1, is_empty=is_empty) 
            self.blocks.update({f"{block+1}": tile})

    def mount_tiles(self) -> None:
        board = self.query_one("Board")
        for tile in self.blocks.values(): 
            board.mount(tile)

    def on_mount(self, event: events.Mount) -> None:
        self.screen.styles.background = "grey"
        self.create_blocks()
        self.mount_tiles() 

    def compose(self) -> ComposeResult:
        yield UpperContainer()
        yield Board()

    def on_key(self, event: events.Key) -> None:
        if event.key in self.all_move_directions:
            board = self.query_one("Board")

            match event.key:
                case "right": 
                    self.blocks = board.handle_right_direction(blocks=self.blocks)
                    tiles_widget = list(self.query("Tile"))

                    for index, tile in enumerate(list(self.blocks.values())):
                        if tile.value > 0:
                            tiles_widget[index].change_to_not_empty(new_value=tile.value)
                            continue
                            
                        tiles_widget[index].change_to_empty()

                case "left": board.handle_left_direction()
                case "up": board.handle_up_direction()
                case "down": board.handle_down_direction()


if __name__ == "__main__":
    game = GameApp()
    game.run()
