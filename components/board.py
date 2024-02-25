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
    total_blocks: int = 16

    move_direction: Union[str, None] = None
    all_move_directions: list[str] = ["left", "right", "up", "down"]

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

    # check which tile can be moved to the move_direction
    def check_move_ability(self) -> None:
        for key, value in self.blocks.items():
            tile = value

            match self.move_direction:
                case "right":
                    if (tile.content_region.x + tile.content_region.width) < self.content_region.width:
                        tile.update_can_move(moved_direction=self.move_direction)
                case "left":
                    if tile.content_region.x > self.content_region.x:
                        tile.update_can_move(moved_direction=self.move_direction)
                case "up":
                    if tile.content_region.y > self.content_region.y:
                        tile.update_can_move(moved_direction=self.move_direction)
                case "down":
                    if (tile.content_region.y + tile.content_region.height) < self.content_region.height:
                        tile.update_can_move(moved_direction=self.move_direction)    

    def move_tile_right(self) -> None:
        pass

    def on_mount(self, event: events.Mount) -> None:
        self.focus()

    def on_blur(self, event: events.Blur) -> None:
        '''if user accidently click on something and Board loses focus, re-focus the board'''
        self.focus()
 
    def on_key(self, event: events.Key) -> None:
        if event.key in self.all_move_directions:
            self.move_direction = event.key 
            self.check_move_ability()

            if self.move_direction == "right":
                self.move_tile_right()
