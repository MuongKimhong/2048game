from typing import Dict, Union
from random import randrange
import time

from textual.containers import Container
from textual.app import ComposeResult
from textual.widgets import Static
from textual import log, events

from components.tile import Tile
from components.score import Score


'''
|1 |2 |3 |4 |    |1 |5 |9 |13|
|5 |6 |7 |8 | -> |2 |6 |10|14|  or Revert back to original
|9 |10|11|12|    |3 |7 |11|15| 
|13|14|15|16|    |4 |8 |12|16|
'''
def transpose(matrix: list[Dict[str, Tile]], reverse=False) -> list[Dict[str, Tile]]:
    counter = 0
    counter_increment = 4 if reverse else 1
    item: Dict[str, Tile] = dict()
    new_matrix: list[Dict[str, Tile]] = []

    for i in range(4):
        for row in matrix:
            smallest_num = int(list(row.keys())[0]) + counter
            item[str(smallest_num)] = row[str(smallest_num)]

        counter = counter + counter_increment
        new_matrix.append(item)
        item = dict()

    return new_matrix


def contruct_new_blocks(matrix: list[Dict[str, Tile]]) -> Dict[str, Tile]:
    new_blocks: Dict[str, Tile] = dict()
    for row in matrix: 
        new_blocks.update(row)
    return new_blocks


'''
As board has 16 blocks, seperate boards into 4 rows,
each row has 4 blocks (which means work with 4 blocks at a time)

|1 |2 |3 |4 | <- 4 greatest number
|5 |6 |7 |8 | <- 8 greatest number
|9 |10|11|12| <- 12 greatest number
|13|14|15|16| <- 16 greatest number
- each row has a greatest block number which is divisible by 4, 
- each row has a smallest block number which is divisible by 4 after added by 3

in mathematic, 4 is called multiple of 4. for variable name called it multiple_of_block_num
'''
def decompose_blocks_to_rows(blocks: Dict[str, Tile]) -> list[Dict[str, Tile]]:
    MULTIPLE_OF_BLOCK_NUMBER = 4
    row: Dict[str, Tile] = dict()
    seperate_rows: list[Dict[str, Tile]] = []

    for block_num, tile in blocks.items():
        row[str(block_num)] = tile

        if int(block_num) % MULTIPLE_OF_BLOCK_NUMBER == 0:
            seperate_rows.append(row)
            row = dict()
    
    return seperate_rows


def pair_processing(left_block: Tile, right_block: Tile, score: Score, move_direction: str) -> None:
    if move_direction not in ["left", "right", "up", "down"]:
        return None

    block_to_update = left_block if (move_direction == "left" or move_direction == "up") else right_block
    block_to_delete = right_block if (move_direction == "left" or move_direction == "up") else left_block

    if block_to_update.is_empty:
        block_to_update.change_value(block_to_delete.value)
        block_to_delete.change_value(0)
    elif block_to_update.value == block_to_delete.value:
        score.update_score(sum_value=block_to_update.value + block_to_delete.value)
        block_to_update.change_value(block_to_update.value + block_to_delete.value)
        block_to_delete.change_value(0)


class Board(Container, can_focus=True):
    DEFAULT_CSS = """
    Board {
        layout: grid;
        background: darkslategray; 
        grid-size: 4 4;
        grid-gutter: 1;
    } 
    """

    def handle_right_direction(self, blocks: Dict[str, Tile]) -> Dict[str, Tile]:        
        seperate_rows: list[Dict[str, Tile]] = decompose_blocks_to_rows(blocks)

        for row in seperate_rows:
            smallest_num, greatest_num = (int(list(row.keys())[0]), int(list(row.keys())[-1]))
            right_block_num, left_block_num = (greatest_num, greatest_num - 1)

            for count in range(12): # each row, loop 12 times for pair processing. read paper for more info
                for key in reversed(list(row.keys())):
                    right_block, left_block = (row[str(right_block_num)], row[str(left_block_num)])

                    if left_block.is_empty: break

                    pair_processing(left_block, right_block, self.app.query_one("Score"), "right")
                    break

                if right_block_num - 1 == smallest_num:
                    right_block_num, left_block_num = (greatest_num, greatest_num - 1)
                else:
                    right_block_num, left_block_num = (right_block_num - 1, left_block_num - 1)

        return contruct_new_blocks(seperate_rows)

    def handle_left_direction(self, blocks: Dict[str, Tile]) -> Dict[str, Tile]:
        seperate_rows: list[Dict[str, Tile]] = decompose_blocks_to_rows(blocks)

        for row in seperate_rows:
            smallest_num, greatest_num = (int(list(row.keys())[0]), int(list(row.keys())[-1]))
            left_block_num, right_block_num = (smallest_num, smallest_num + 1)

            for count in range(12): # each row, loop 12 times for pair processing. read paper for more info
                for key in list(row.keys()):
                    left_block, right_block = (row[str(left_block_num)], row[str(right_block_num)])

                    if right_block.is_empty: break

                    pair_processing(left_block, right_block, self.app.query_one("Score"), "left")
                    break 

                if left_block_num + 1 == greatest_num:
                    left_block_num, right_block_num = (smallest_num, smallest_num + 1)
                else:
                    left_block_num, right_block_num = (left_block_num + 1, right_block_num + 1)

        return contruct_new_blocks(seperate_rows)

    def handle_up_direction(self, blocks: Dict[str, Tile]) -> Dict[str, Tile]:    
        seperate_rows: list[Dict[str, Tile]] = decompose_blocks_to_rows(blocks)
        seperate_columns: list[Dict[str, Tile]] = transpose(seperate_rows)

        for column in seperate_columns:
            smallest_num, greatest_num = (int(list(column.keys())[0]), int(list(column.keys())[-1]))
            left_block_num, right_block_num = (smallest_num, smallest_num + 4)

            for count in range(12): # each column, loop 12 times for pair processing. read paper for more info
                for key in list(column.keys()):
                    left_block, right_block = (column[str(left_block_num)], column[str(right_block_num)])

                    if right_block.is_empty: break

                    pair_processing(left_block, right_block, self.app.query_one("Score"), "up")
                    break

                if left_block_num + 4 == greatest_num:
                    left_block_num, right_block_num = (smallest_num, smallest_num + 4)
                else:
                    left_block_num, right_block_num = (left_block_num + 4, right_block_num + 4)

        return contruct_new_blocks(transpose(seperate_columns, reverse=True))

    def handle_down_direction(self, blocks: Dict[str, Tile]) -> Dict[str, Tile]:
        seperate_rows: list[Dict[str, Tile]] = decompose_blocks_to_rows(blocks)
        seperate_columns: list[Dict[str, Tile]] = transpose(seperate_rows)

        for column in seperate_columns:
            smallest_num, greatest_num = (int(list(column.keys())[0]), int(list(column.keys())[-1]))
            right_block_num, left_block_num = (greatest_num, greatest_num - 4)

            for count in range(12): # each column, loop 12 times for pair processing. read paper for more info
                for key in reversed(list(column.keys())):
                    left_block, right_block = (column[str(left_block_num)], column[str(right_block_num)])

                    if left_block.is_empty: break

                    pair_processing(left_block, right_block, self.app.query_one("Score"), "down")
                    break

                if right_block_num - 4 == smallest_num:
                    right_block_num, left_block_num = (greatest_num, greatest_num - 4)
                else:
                    left_block_num, right_block_num = (left_block_num - 4, right_block_num - 4)

        return contruct_new_blocks(transpose(seperate_columns, reverse=True)) 
