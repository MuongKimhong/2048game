from typing import Union, Dict
import random
import time

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
        self.can_spawn_new_tile: bool = True
        self.TOTAL_BLOCKS: int = 16
        super().__init__()

    def random_block_nums_on_game_start(self) -> tuple:
        ''' 
        notes:
        - when game start, only 2 tiles appear, Tile number 2 and Tile number 4 
        - both tiles appear in random block number between block 1 and block 16
        '''
        tile_number_two: int = random.randrange(1, self.TOTAL_BLOCKS) 
        tile_number_four: Union[int, None] = None
        while True:
            tile_number_four = random.randrange(1, self.TOTAL_BLOCKS)

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

    @property
    def game_over(self) -> bool:
        empty_blocks = [block_num for block_num, tile in self.blocks.items() if tile.is_empty]
        return True if len(empty_blocks) <= 0 else False

    def spawn_new_tile(self) -> None:
        tile_number = random.choice([2, 4])
        random_block: Union[int, None] = None

        empty_blocks = [block_num for block_num, tile in self.blocks.items() if tile.is_empty]
        while True:
            random_block = random.randrange(1, self.TOTAL_BLOCKS)

            if str(random_block) in empty_blocks:
                break        

        self.blocks[str(random_block)].change_value(new_value=tile_number)
        list(self.query("Tile"))[random_block - 1].change_to_not_empty(new_value=tile_number)

    # change tiles value and position on key press
    def update_tiles(self) -> None: 
        tiles_widget = list(self.query("Tile"))

        for i, tile in enumerate(list(self.blocks.values())):
            tiles_widget[i].change_to_not_empty(tile.value) if tile.value > 0 else tiles_widget[i].change_to_empty()

        if self.can_spawn_new_tile: self.spawn_new_tile()

    def on_mount(self, event: events.Mount) -> None:
        self.screen.styles.background = "grey"
        self.create_blocks()
        self.mount_tiles() 

    def compose(self) -> ComposeResult:
        yield UpperContainer()
        yield Board()

    def on_key(self, event: events.Key) -> None:
        if event.key in self.all_move_directions:
            if self.game_over:
                time.sleep(1)
                self.exit(return_code=4, message=f"Game is over with score: {self.query_one('Score').renderable}")

            board = self.query_one("Board")

            match event.key:
                case "right": 
                    self.blocks = board.handle_right_direction(self.blocks)
                case "left": 
                    self.blocks = board.handle_left_direction(self.blocks)
                case "up": 
                    self.blocks = board.handle_up_direction(self.blocks)
                case "down": 
                    self.blocks = board.handle_down_direction(self.blocks)

            self.update_tiles()


if __name__ == "__main__":
    game = GameApp()
    game.run()
    import sys
    sys.exit(game.return_code or 0)
