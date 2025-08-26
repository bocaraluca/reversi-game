from domain.computer_strategy import ComputerStrategy, ComputerMediumStrategy, ComputerHardStrategy
from domain.reversi_game import ReversiGame


class Service:
    def __init__(self, human_player: str, strategy: str):
        """
        Initialize the service with the human player and the strategy for the computer player
        :param human_player: The human player
        :param strategy: The strategy for the computer player
        """
        self._game = ReversiGame(human_player)
        if strategy == 'easy':
            self._game.set_computer_strategy(ComputerStrategy(self._game))
        elif strategy == 'medium':
            self._game.set_computer_strategy(ComputerMediumStrategy(self._game))
        elif strategy == 'hard':
            self._game.set_computer_strategy(ComputerHardStrategy(self._game))

    def get_board(self) -> list:
        """
        Get the current game board
        :return: The game board
        """
        return self._game.board

    def is_valid_human_move(self, row: int, col: int) -> bool:
        """
        Check if the move the human player wants to make is valid
        :param row: The row of the move
        :param col: The column of the move
        :return: True if the move is valid, False otherwise
        """
        return self._game.is_valid_move(row, col, self._game.human_player)

    def is_valid_computer_move(self, row: int, col: int) -> bool:
        """
        Check if the move the computer player wants to make is valid
        :param row: The row of the move
        :param col: The column of the move
        :return: True if the move is valid, False otherwise
        """
        return self._game.is_valid_move(row, col, self._game.computer_player)

    def get_cell_value(self, row: int, col: int) -> str:
        """
        Gets the value of a cell on the board
        :param row: The row of the cell
        :param col: The column of the cell
        :return: The value of the cell
        """
        return self._game.get_cell_value(row, col)

    def get_human_player(self) -> str:
        """
        Returns the symbol of the human player
        :return: The symbol of the human player
        """
        return self._game.human_player

    def get_computer_player(self) -> str:
        """
        Returns the symbol of the computer player
        :return: The symbol of the computer player
        """
        return self._game.computer_player

    def get_score(self) -> dict:
        """
        Gets the score of the game
        :return: A dictionary containing the score of the game for the human player and the computer player
        """
        return self._game.get_score()

    def get_valid_human_moves(self) -> list:
        """
        Gets the valid moves for the human player
        :return: A list of tuples containing all the valid moves for the human player
        """
        return self._game.get_valid_moves(self._game.human_player)

    def get_valid_computer_moves(self) -> list:
        """
        Gets the valid moves for the computer player
        :return: A list of tuples containing all the valid moves for the computer player
        """
        return self._game.get_valid_moves(self._game.computer_player)

    def play_human_move(self, row: int, col: int) -> None:
        """
        Makes a move for the human player at the specified row and column
        :param row: The row of the move
        :param col: The column of the move
        :return: None
        """
        self._game.play_human_move(row, col)

    def play_computer_move(self) -> tuple:
        """
        Makes a move for the computer player using the strategy
        :return: A tuple containing the row and column of the move made by the computer player
        """
        return self._game.play_computer_move()

    def is_game_over(self) -> bool:
        """
        Checks if the game is over
        :return: True if the game is over, False otherwise
        """
        return self._game.is_game_over()


