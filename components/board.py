from typing import Dict, Union
from random import randrange
import math
import time

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

    def update_score(self, sum_value: int) -> None:
        score_widget = self.app.query_one("Score")
        old_score = int(str(score_widget.renderable))
        score_widget.update(str(old_score + sum_value))


    def handle_right_direction(self, blocks: Dict[str, Tile]) -> Dict[str, Tile]:
        '''
        modify the blocks variable and re-render the tiles

        As board has 16 blocks, seperate boards into 4 rows,
        each row has 4 blocks (which means work with 4 blocks at a time)
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
        
        '''each row, loop 12 times for pair processing. read paper for more info'''
        pair_processing_loop: int = 12

        # seperate blocks into 4 seperate rows
        for block_num, tile in blocks.items():
            row[str(block_num)] = tile

            if int(block_num) % multiple_of_block_num == 0:
                seperate_rows.append(row)
                row = dict()  

        for row in seperate_rows:
            smallest_num_in_row = int(list(row.keys())[0])
            greatest_num_in_row = int(list(row.keys())[-1])

            right_block_num: int = greatest_num_in_row
            left_block_num: int = right_block_num - 1

            for count in range(pair_processing_loop):
                for key in reversed(list(row.keys())): # start pair processing
                    right_block: Tile = row[str(right_block_num)]
                    left_block: Tile = row[str(left_block_num)]

                    if left_block.is_empty:
                        break
                    elif right_block.is_empty:
                        row[str(right_block_num)].change_value(new_value=left_block.value)
                        row[str(left_block_num)].change_value(new_value=0)
                    elif left_block.value == right_block.value:
                        row[str(right_block_num)].change_value(new_value=left_block.value + right_block.value)
                        row[str(left_block_num)].change_value(new_value=0)
                        self.update_score(sum_value=left_block.value + right_block.value)
                    
                    break

                if right_block_num - 1 == smallest_num_in_row:
                    right_block_num = greatest_num_in_row
                    left_block_num = right_block_num - 1
                else:
                    right_block_num = right_block_num - 1
                    left_block_num = left_block_num - 1


        new_blocks: Dict[str, Tile] = dict()
        for row in seperate_rows:
            new_blocks.update(row)

        return new_blocks


    def handle_left_direction(self, blocks: Dict[str, Tile]) -> Dict[str, Tile]:
        '''
        1 smallest number, 1 + 3 = 4 (divisible by 4) -> |1 |2 |3 |4 |
        5 smallest number, 5 + 3 = 8 (divisible by 4) -> |5 |6 |7 |8 |
        9 smallest number, 9 + 3 = 12 (divisible by 4) ->|9 |10|11|12|
        13 smallest number,13 + 3 = 16(divisible by 4) ->|13|14|15|16|
        each row has smallest block number which is divisible by 4 after added 3, 
        in mathematic, 4 is called multiple of 4. for variable name called it multiple_of_block_num
        '''
        multiple_of_block_num = 4
        seperate_rows: list[Dict[str, Tile]] = []
        row: Dict[str, Tile] = dict()

        '''each row, loop 12 times for pair processing. read paper for more info'''
        pair_processing_loop: int = 12

        # seperate blocks into 4 seperate rows
        for block_num, tile in blocks.items():
            row[str(block_num)] = tile

            if int(block_num) % multiple_of_block_num == 0:
                seperate_rows.append(row)
                row = dict()  

        for row in seperate_rows:
            smallest_num_in_row = int(list(row.keys())[0])
            greatest_num_in_row = int(list(row.keys())[-1])

            left_block_num: int = smallest_num_in_row
            right_block_num: int = left_block_num + 1

            for count in range(pair_processing_loop):
                for key in list(row.keys()):
                    left_block: Tile = row[str(left_block_num)]
                    right_block: Tile = row[str(right_block_num)]

                    if right_block.is_empty:
                        break
                    elif left_block.is_empty:
                        row[str(left_block_num)].change_value(new_value=right_block.value)
                        row[str(right_block_num)].change_value(new_value=0)
                    elif left_block.value == right_block.value:
                        row[str(left_block_num)].change_value(new_value=left_block.value+right_block.value)
                        row[str(right_block_num)].change_value(new_value=0)
                        self.update_score(sum_value=left_block.value + right_block.value)

                    break

                if left_block_num + 1 == greatest_num_in_row:
                    left_block_num = smallest_num_in_row
                    right_block_num = left_block_num + 1
                else:
                    left_block_num = left_block_num + 1
                    right_block_num = right_block_num + 1
            
        new_blocks: Dict[str, Tile] = dict()
        for row in seperate_rows:
            new_blocks.update(row)

        return new_blocks

    def handle_up_direction(self, blocks: Dict[str, Tile]) -> Dict[str, Tile]:
        multiple_of_block_num = 4
        seperate_rows: list[Dict[str, Tile]] = []
        row: Dict[str, Tile] = dict()
        
        '''each row, loop 12 times for pair processing. read paper for more info'''
        pair_processing_loop: int = 12

        # seperate blocks into 4 seperate rows
        for block_num, tile in blocks.items():
            row[str(block_num)] = tile

            if int(block_num) % multiple_of_block_num == 0:
                seperate_rows.append(row)
                row = dict()

        '''
        transposition the seperate rows
        |1 |2 |3 |4 |    |1 |5 |9 |13|
        |5 |6 |7 |8 | -> |2 |6 |10|14| 
        |9 |10|11|12|    |3 |7 |11|15|
        |13|14|15|16|    |4 |8 |12|16|

        '''
        counter = 0
        seperate_columns: list[Dict[str, Tile]] = []
        column: Dict[str, Tile] = dict()

        for i in range(4):
            for row in seperate_rows:
                smallest_num = int(list(row.keys())[0]) + counter
                column[str(smallest_num)] = row[str(smallest_num)]

            counter = counter + 1 
            seperate_columns.append(column)
            column = dict()

        for column in seperate_columns:
            smallest_num_in_column = int(list(column.keys())[0])
            greatest_num_in_column = int(list(column.keys())[-1])

            left_block_num: int = smallest_num_in_column
            right_block_num: int = left_block_num + 4

            for count in range(pair_processing_loop):
                for key in list(column.keys()):
                    left_block: Tile = column[str(left_block_num)]
                    right_block: Tile = column[str(right_block_num)]

                    if right_block.is_empty:
                        break
                    elif left_block.is_empty:
                        column[str(left_block_num)].change_value(new_value=right_block.value)
                        column[str(right_block_num)].change_value(new_value=0)
                    elif left_block.value == right_block.value:
                        column[str(left_block_num)].change_value(new_value=left_block.value+right_block.value)
                        column[str(right_block_num)].change_value(new_value=0)
                        self.update_score(sum_value=left_block.value+right_block.value)

                    break

                if left_block_num + 4 == greatest_num_in_column:
                    left_block_num = smallest_num_in_column
                    right_block_num = left_block_num + 4
                else:
                    left_block_num = left_block_num + 4
                    right_block_num = right_block_num + 4

        # transform back to seperate row
        counter = 0
        seperate_rows: list[Dict[str, Tile]] = []
        row: Dict[str, Tile] = dict()
        for i in range(4):
            for column in seperate_columns:
                smallest_num = int(list(column.keys())[0]) + counter
                row[str(smallest_num)] = column[str(smallest_num)]

            counter = counter + 4
            seperate_rows.append(row)
            row = dict()

        new_blocks: Dict[str, Tile] = dict()
        for row in seperate_rows:
            new_blocks.update(row)

        return new_blocks

    def handle_down_direction(self, blocks: Dict[str, Tile]) -> Dict[str, Tile]:
        multiple_of_block_num = 4
        seperate_rows: list[Dict[str, Tile]] = []
        row: Dict[str, Tile] = dict()
        
        '''each row, loop 12 times for pair processing. read paper for more info'''
        pair_processing_loop: int = 12

        # seperate blocks into 4 seperate rows
        for block_num, tile in blocks.items():
            row[str(block_num)] = tile

            if int(block_num) % multiple_of_block_num == 0:
                seperate_rows.append(row)
                row = dict()

        '''
        transposition the seperate rows
        |1 |2 |3 |4 |    |1 |5 |9 |13|
        |5 |6 |7 |8 | -> |2 |6 |10|14| 
        |9 |10|11|12|    |3 |7 |11|15|
        |13|14|15|16|    |4 |8 |12|16|

        '''
        counter = 0
        seperate_columns: list[Dict[str, Tile]] = []
        column: Dict[str, Tile] = dict()

        for i in range(4):
            for row in seperate_rows:
                smallest_num = int(list(row.keys())[0]) + counter
                column[str(smallest_num)] = row[str(smallest_num)]

            counter = counter + 1 
            seperate_columns.append(column)
            column = dict()

        for column in seperate_columns:
            smallest_num_in_column = int(list(column.keys())[0])
            greatest_num_in_column = int(list(column.keys())[-1])

            right_block_num: int = greatest_num_in_column
            left_block_num: int = right_block_num - 4

            for count in range(pair_processing_loop):
                for key in reversed(list(column.keys())):
                    left_block: Tile = column[str(left_block_num)]
                    right_block: Tile = column[str(right_block_num)]

                    if left_block.is_empty:
                        break
                    elif right_block.is_empty:
                        column[str(right_block_num)].change_value(new_value=left_block.value)
                        column[str(left_block_num)].change_value(new_value=0)
                    elif left_block.value == right_block.value:
                        column[str(right_block_num)].change_value(new_value=left_block.value+right_block.value)
                        column[str(left_block_num)].change_value(new_value=0)
                        self.update_score(sum_value=left_block.value+right_block.value)

                    break

                if right_block_num - 4 == smallest_num_in_column:
                    right_block_num = greatest_num_in_column
                    left_block_num = right_block_num - 4
                else:
                    left_block_num = left_block_num - 4
                    right_block_num = right_block_num - 4

        # transform back to seperate row
        counter = 0
        seperate_rows: list[Dict[str, Tile]] = []
        row: Dict[str, Tile] = dict()
        for i in range(4):
            for column in seperate_columns:
                smallest_num = int(list(column.keys())[0]) + counter
                row[str(smallest_num)] = column[str(smallest_num)]

            counter = counter + 4
            seperate_rows.append(row)
            row = dict()

        new_blocks: Dict[str, Tile] = dict()
        for row in seperate_rows:
            new_blocks.update(row)

        return new_blocks 
