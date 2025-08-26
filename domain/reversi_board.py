import string
from enum import Enum
from texttable import Texttable
from exceptions.exceptions import InvalidMoveException

class ReversiSymbol(Enum):
    """
    Enum class for the Othello symbols.
    """
    BLACK = 'X'
    WHITE = 'O'
    EMPTY = ' '

class ReversiBoard:
    def __init__(self):
        self._data = []
        for i in range(8):
            self._data.append([' '] * 8)
        self._data[3][3] = ReversiSymbol.WHITE.value
        self._data[3][4] = ReversiSymbol.BLACK.value
        self._data[4][3] = ReversiSymbol.BLACK.value
        self._data[4][4] = ReversiSymbol.WHITE.value

        self._directions = [(0, 1), (1, 1), (1, 0), (1, -1),
                            (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def __str__(self) -> str:
        """
        Returns a string representation of the board using the Texttable library.
        :return: The representation of the board.
        """
        t = Texttable()
        header = ['/'] + list(string.ascii_uppercase[:8])
        t.header(header)

        for row in range(8):
            t.add_row([row + 1] + self._data[row])
        return t.draw()

    def copy(self):
        """
        Returns a copy of the board.
        :return: A copy of the board.
        """
        new_board = ReversiBoard()
        new_board.data = [row[:] for row in self._data]
        return new_board

    def is_valid_move(self, row: int, col: int, symbol: str) -> bool:
        """
        Checks if the move is valid.
        :param row: The row of the move.
        :param col: The column of the move.
        :param symbol: The symbol of the player who made the move.
        :return: True if the move is valid, False otherwise.
        """
        if not (0 <= row < 8 and 0 <= col < 8):
            return False

        if self._data[row][col] != ReversiSymbol.EMPTY.value:
            return False

        opp = ReversiSymbol.BLACK.value if symbol == ReversiSymbol.WHITE.value else ReversiSymbol.WHITE.value

        for dr, dc in self._directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self._data[r][c] == opp:
                r, c = r + dr, c + dc
                same_piece_end = False
                while 0 <= r < 8 and 0 <= c < 8:
                    if self._data[r][c] == ReversiSymbol.EMPTY.value:
                        break
                    if self._data[r][c] == symbol:
                        same_piece_end = True
                        break
                    r, c = r + dr, c + dc
                if same_piece_end:
                    return True
        return False

    def make_move(self, row: int, col: int, symbol: str) -> None:
        """
        Makes a move on the board.
        :param row: The row of the move.
        :param col: The column of the move.
        :param symbol: The symbol of the player who made the move.
        :return: None
        """
        if not self.is_valid_move(row, col, symbol):
            raise InvalidMoveException('Invalid move. Please try again.')
        self._data[row][col] = symbol
        self.flip_pieces(row, col, symbol)

    def get_cell_value(self, row: int, col: int) -> str:
        """
        Returns the value of the cell at the given row and column.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :return: The value of the cell.
        """
        return self._data[row][col]

    def flip_pieces(self, row: int, col: int, symbol: str) -> None:
        """
        Flips all the pieces situated between the newly placed piece and another piece of the same color.
        :param row: The row of the newly placed piece.
        :param col: The column of the newly placed piece.
        :param symbol: The symbol of the piece which was placed.
        :return: None
        """
        opp = ReversiSymbol.BLACK.value if symbol == ReversiSymbol.WHITE.value else ReversiSymbol.WHITE.value

        for dr, dc in self._directions:
            r, c = row + dr, col + dc
            squares_to_flip = []
            # find the opponents' pieces in this direction
            while 0 <= r < 8 and 0 <= c < 8 and self._data[r][c] == opp:
                squares_to_flip.append((r, c))
                r, c = r + dr, c + dc
            # if we reached a piece of the same color, flip the pieces
            if 0 <= r < 8 and 0 <= c < 8 and self._data[r][c] == symbol:
                for fr, fc in squares_to_flip:
                    self._data[fr][fc] = symbol
