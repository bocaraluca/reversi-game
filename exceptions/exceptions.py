class InvalidMoveException(Exception):
    def __init__(self, message: str) -> None:
        """
        Exception raised when a move is invalid
        :param message: The message to be displayed
        """
        super().__init__(message)

class NoValidMovesException(Exception):
    def __init__(self, message: str) -> None:
        """
        Exception raised when there are no valid moves for a player
        :param message: The message to be displayed
        """
        super().__init__(message)