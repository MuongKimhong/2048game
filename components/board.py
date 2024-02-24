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


class Board(Container):
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
    total_blocks: int = 16

    mouse_move_direction: Union[str, None] = None
    mouse_down_coordinate: tuple = ()
    mouse_up_coordinate: tuple = ()

    def compose(self) -> ComposeResult:
        ''' 
        notes:
        - when game start, only 2 tiles appear, Tile number 2 and Tile number 4 
        - both tiles appear in random block between block 1 and block 16
        '''
     
        tile_two_block: int = randrange(self.total_blocks)
        tile_four_block: Union[int, None] = None
        while True:
            tile_four_block = randrange(self.total_blocks)

            if tile_four_block != tile_two_block:
                break

        for i in range(self.total_blocks):
            if i == tile_two_block:
                tile = Tile(value=2, id=f"block-{i+1}", is_empty=False)
            elif i == tile_four_block:
                tile = Tile(value=4, id=f"block-{i+1}", is_empty=False)
            else:
                tile = Tile(value=None, id=f"block-{i+1}", is_empty=True)

            self.blocks[f"{i+1}"] = tile
            yield tile

    def calculate_move_direction(self) -> None:
        '''
        if (up[x] - down[x] > up[y] - down[y]) && 
        '''

        after_moved_coordinate: tuple = (
            self.mouse_up_coordinate[0] - self.mouse_down_coordinate[0],
            self.mouse_up_coordinate[1] - self.mouse_down_coordinate[1]
        )



    def on_mouse_down(self, event: events.MouseDown) -> None:
        self.mouse_down_coordinate = (event.x, event.y)

    def on_mouse_up(self, event: events.MouseUp) -> None:
        self.mouse_up_coordinate = (event.x, event.y)

        log(f"down {self.mouse_down_coordinate}, up {self.mouse_up_coordinate}")
