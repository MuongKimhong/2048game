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
            yield tile

    def re_render_tiles(self) -> None:
        for tile in self.app.query("Tile"):
            tile.remove()

        self.mount(*list(self.blocks.values()))

    def handle_right_direction(self) -> None:
        '''
        modify the blocks variable and re-render the tiles

        As board has 16 blocks, seperate boards into 4 parts,
        each part has 4 blocks (which means work with 4 blocks at a time)
        '''

        '''
        |1 |2 |3 |4 | <- 4 greatest number
        |5 |6 |7 |8 | <- 8 greatest number
        |9 |10|11|12| <- 12 greatest number
        |13|14|15|16| <- 16 greatest number
        each row has a greatest block number which is divisible by 4, 
        in mathematic, 4 is called multiple of 4. for variable name called it multiple_of_block_num
        '''
        multiple_of_block_num = 4
        seperate_rows: list[Dict[str, Tile]] = []
        row: Dict[str, Tile] = dict()
        pair_processing_loop: int = 12 # read paper

        # seperate blocks into 4 seperate rows
        for block_num, tile in self.blocks.items():
            row[f"{block_num}"] = tile

            if (int(block_num) % multiple_of_block_num) == 0:
                seperate_rows.append(row)
                row = dict()  

        for row in seperate_rows:
            smallest_num_in_row: int = int(list(row.keys())[0])
            greatest_num_in_row: int = int(list(row.keys())[-1])
            right_block_num: int = greatest_num_in_row
            left_block_num: int = right_block_num - 1

            for count in range(pair_processing_loop):
                for key in reversed(list(row.keys())): # start pair processing
                    right_block: Tile = row[str(right_block_num)]
                    left_block: Tile = row[str(left_block_num)]

                    if left_block.is_empty:
                        break
                    elif right_block.is_empty:
                        row[str(right_block_num)].change_to_not_empty(new_value=left_block.value)
                        row[str(left_block_num)].change_to_empty()
                    elif left_block.value == right_block.value:
                        row[str(right_block_num)].change_value(new_value=left_block.value + right_block.value)
                        row[str(left_block_num)].change_to_empty()
                    
                    break

                if right_block_num - 1 == smallest_num_in_row:
                    right_block_num = greatest_num_in_row
                    left_block_num = right_block_num - 1
                else:
                    right_block_num = right_block_num - 1
                    left_block_num = left_block_num - 1

        self.blocks = dict() 
        # combine all rows together to make full board
        for row in seperate_rows:
            self.blocks.update(row)

        self.re_render_tiles()


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
                case "right": self.handle_right_direction()
                case "left": self.handle_left_direction()
                case "up": self.handle_up_direction()
                case "down": self.handle_down_direction()
