from typing import Dict, Union
from random import randrange
import math

from textual.containers import Container
from textual.app import ComposeResult
from textual.widgets import Static
from textual import log, events

from components.tile import Tile


class GeometricSequence:
    def __init__(self) -> None:
        self.first_term = 2
        self.last_term = 2048
        self.common_ratio = 2

    @property
    def sequence(self) -> list[int]:
        s = []

        term = self.first_term
        while True:
            s.append(term)
            term = term * self.common_ratio

            if term == self.last_term: break

        return s


class Board(Container, can_focus=True):
    DEFAULT_CSS = """
    Board {
        layout: grid;
        background: darkslategray; 
        grid-size: 4 4;
        grid-gutter: 1;
    } 
    """
    geometric_sequence = GeometricSequence().sequence
    blocks: Dict[str, Tile] = {}
    TOTAL_BLOCKS: int = 16
    TOTAL_ROWS = 4
    TOTAL_COLUMNS = 4

    move_direction: Union[str, None] = None
    all_move_directions: list[str] = ["left", "right", "up", "down"]


    def compose(self) -> ComposeResult:
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
        tile_two_block = 2
        tile_four_block = 3

        '''
        loop thru TOTAL_ROWS and TOTAL_COLUMNS instead of TOTAL_BLOCKS to get
        board region (which_row, which_column)
        '''
        starting_block_number = 1
        for row in range(self.TOTAL_ROWS):
            for column in range(self.TOTAL_COLUMNS):
                if starting_block_number == tile_two_block:
                    value = 2
                    is_empty = False
                elif starting_block_number == tile_four_block:
                    value = 4
                    is_empty = False
                else:
                    value = None
                    is_empty = True

                tile = Tile(
                    value=value,
                    id=f"block-{starting_block_number}",
                    block_number=starting_block_number,
                    board_region={"row": row+1, "column": column+1},
                    is_empty=is_empty
                )
                self.blocks[f"{starting_block_number}"] = tile
                starting_block_number = starting_block_number + 1
                yield tile

        # for i in range(self.TOTAL_BLOCKS):
        #     if i == tile_two_block:
        #         tile = Tile(value=2, id=f"block-{i+1}", block_number=i+1, is_empty=False)
        #     elif i == tile_four_block:
        #         tile = Tile(value=4, id=f"block-{i+1}", block_number=i+1, is_empty=False)
        #     else:
        #         tile = Tile(value=None, id=f"block-{i+1}", block_number=i+1, is_empty=True)

        #     self.blocks[f"{i+1}"] = tile
        #     yield tile

    # check which tile can be moved to the move_direction
    def can_move_to_direction(self, tile: Tile) -> bool:
        match self.move_direction:
            case "right":
                if tile.content_region.x + tile.content_region.width < self.content_region.width:
                    next_tile = self.query_one(f"#block-{tile.block_number+1}")
                    if (next_tile.is_empty) or (next_tile.value == tile.value):
                        return True
            case "left":
                if tile.content_region.x > self.content_region.x:
                    return True
            case "up":
                if tile.content_region.y > self.content_region.y:
                    return True
            case "down":
                if (tile.content_region.y + tile.content_region.height) < self.content_region.height:
                    return True

        return False

    def handle_right_direction(self) -> None:
        for tile in self.blocks.values():
            if tile.value is None:
                continue

            can_move_count = self.TOTAL_COLUMNS - tile.board_region["column"]
            for i in range(can_move_count):
                next_tile = self.query_one(f"#block-{tile.block_number + i + 1}")
                if (self.can_move_to_direction(tile)) and (next_tile.is_empty) and (self.can_move_to_direction(next_tile)):
                    continue
                elif not next_tile.is_empty:
                    break
                elif not self.can_move_to_direction(next_tile) and next_tile.is_empty:
                    next_tile.change_to_not_empty(new_value=tile.value)
                    tile.change_to_empty()
                elif self.can_move_to_direction(tile) and next_tile.value == tile.value:
                    next_tile.change_to_not_empty(new_value=tile.value + next_tile.value)
                    tile.change_to_empty()

    def handle_left_direction(self) -> None:
        pass

    def handle_up_direction(self) -> None:
        pass

    def handle_down_direction(self) -> None:
        pass

    def on_mount(self, event: events.Mount) -> None:
        self.focus()

    def on_blur(self, event: events.Blur) -> None:
        '''if user accidently click on something and Board loses focus, re-focus the board'''
        self.focus()
 
    def on_key(self, event: events.Key) -> None:
        if event.key in self.all_move_directions:
            self.move_direction = event.key 

            match self.move_direction:
                case "right":
                    self.handle_right_direction()
                case "left":
                    self.handle_left_direction()
                case "up":
                    self.handle_up_direction()
                case "down":
                    self.handle_down_direction()
