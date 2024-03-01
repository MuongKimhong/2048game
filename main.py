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

    def random_block_nums_on_game_start(self) -> tuple:
        ''' 
        notes:
        - when game start, only 2 tiles appear, Tile number 2 and Tile number 4 
        - both tiles appear in random block number between block 1 and block 16
        '''
        tile_number_two: int = randrange(1, self.TOTAL_BLOCKS) 
        tile_number_four: Union[int, None] = None
        while True:
            tile_number_four = randrange(1, self.TOTAL_BLOCKS)

            if tile_number_four != tile_number_two:
                break

        return (tile_number_two, tile_number_four)
        

    def create_blocks(self) -> None:
        tile_two, tile_four = self.random_block_nums_on_game_start()

        for block in range(self.TOTAL_BLOCKS):
            value = 2 if (block + 1) == tile_two else 4 if (block + 1) == tile_four else 0
            is_empty = True if value == 0 else False
            tile = Tile(value=value, id=f"block-{block+1}", block_number=block+1, is_empty=is_empty) 
            self.blocks.update({str(block+1): tile})

    def mount_tiles(self) -> None:
        board = self.query_one("Board")
        for tile in self.blocks.values(): 
            board.mount(tile)

    # change tiles value and position on key press
    def update_tiles(self) -> None:
        tiles_widget = list(self.query("Tile"))

        for i, tile in enumerate(list(self.blocks.values())):
            tiles_widget[i].change_to_not_empty(tile.value) if tile.value > 0 else tiles_widget[i].change_to_empty()

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
                    self.update_tiles()

                case "left": board.handle_left_direction()
                case "up": board.handle_up_direction()
                case "down": board.handle_down_direction()


if __name__ == "__main__":
    game = GameApp()
    game.run()
