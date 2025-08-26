from domain.reversi_board import ReversiBoard, ReversiSymbol
from exceptions.exceptions import InvalidMoveException, NoValidMovesException


class ReversiGame:
    def __init__(self, human_player):
        self._board = ReversiBoard()
        self._human_player = human_player
        self._computer_player = ReversiSymbol.BLACK.value if human_player == ReversiSymbol.WHITE.value else ReversiSymbol.WHITE.value
        self._computer_strategy = None

    def set_computer_strategy(self, computer_strategy):
        self._computer_strategy = computer_strategy

    @property
    def board(self):
        return self._board

    @property
    def human_player(self):
        return self._human_player

    @property
    def computer_player(self):
        return self._computer_player

    def get_valid_moves(self, symbol: str) -> list:
        """
        Returns a list of all the valid moves the player having a certain symbol can make.
        :param symbol: The symbol of the player.
        :return: A list of all the valid moves the player can make.
        """
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, symbol):
                    valid_moves.append((row, col))
        return valid_moves

    def is_valid_move(self, row: int, col: int, symbol: str) -> bool:
        """
        Checks if the move the player with a certain symbol wants to make is valid.
        :param row: The row of the move.
        :param col: The column of the move.
        :param symbol: The symbol of the player.
        :return: True if the move is valid, False otherwise.
        """
        return self._board.is_valid_move(row, col, symbol)

    def get_cell_value(self, row: int, col: int) -> str:
        """
        Returns the value of the cell at the given row and column.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :return: The value of the cell.
        """
        return self._board.get_cell_value(row, col)

    def is_game_over(self) -> bool:
        """
        Checks if the game is over.
        :return: True if the game is over, False otherwise.
        """
        return not self.get_valid_moves(self._human_player) and not self.get_valid_moves(self._computer_player)

    def play_human_move(self, row: int, col: int) -> None:
        """
        Makes a move for the human player at the given row and column.
        :param row: The row of the move.
        :param col: The column of the move.
        :return: None
        :
        """
        valid_moves = self.get_valid_moves(self._human_player)
        if not valid_moves:
            raise NoValidMovesException("No valid moves for you. Skipping your turn.")
        if (row, col) not in valid_moves:
            raise InvalidMoveException("Invalid move for you.")
        self._board.make_move(row, col, self._human_player)

    def play_computer_move(self) -> tuple:
        """
        Makes a move for the computer player using the given strategy.
        :return: The row and column of the move.
        """
        try:
            row, col = self._computer_strategy.get_move(self._board, self._computer_player)
            self._board.make_move(row, col, self._computer_player)
        except NoValidMovesException as e:
            raise e
        return row, col

    def get_score(self) -> dict:
        """
        Returns the score of the game for the human player and the computer player.
        :return: A dictionary containing the score for both players.
        """
        score = {ReversiSymbol.BLACK.value: 0, ReversiSymbol.WHITE.value: 0}
        for row in self._board.data:
            for cell in row:
                if cell == ReversiSymbol.BLACK.value:
                    score[ReversiSymbol.BLACK.value] += 1
                elif cell == ReversiSymbol.WHITE.value:
                    score[ReversiSymbol.WHITE.value] += 1
        return score

