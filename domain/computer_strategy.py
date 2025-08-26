import copy
import random

from domain.reversi_board import ReversiBoard
from exceptions.exceptions import NoValidMovesException, InvalidMoveException


class ComputerStrategy:
    def __init__(self, game):
        self._game = game
        self._symbol = game.computer_player
        self._opp_symbol = game.human_player
        self._directions = [(0, 1), (1, 1), (1, 0), (1, -1),
                            (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    def get_move(self, board: ReversiBoard, symbol: str) -> tuple:
        """
        Gets the move that the computer will make.
        :param board: The current board state.
        :param symbol: The symbol of the computer player.
        :return: The move that the computer will make.
        """
        valid_moves = self._game.get_valid_moves(symbol)
        if not valid_moves:
            raise NoValidMovesException("No valid moves for computer. Skipping its turn.")
        return random.choice(valid_moves)

class ComputerHardStrategy(ComputerStrategy):
    def __init__(self, game):
        """
        Constructor for ComputerHardStrategy class.
        :param game: The Othello game that the strategy will be used for.
        """
        super().__init__(game)

    def get_move(self, board: ReversiBoard, symbol: str) -> tuple:
        """
        Gets the move that the computer will make using some strategies to choose the best possible move.
        :param board: The current board state.
        :param symbol: The symbol of the computer player.
        :return: The move that the computer will make.
        """
        valid_moves = self._game.get_valid_moves(symbol)
        if not valid_moves:
            raise NoValidMovesException("No valid moves for computer. Skipping its turn.")

        best_move = random.choice(valid_moves)
        max_opp_flips = 0

        for move in valid_moves:
            if self.is_winning_move(move):
                return move
            if self.blocks_opponent_winning_move(move):
                return move
            if self.is_corner_move(move):
                return move
            opp_flips = self.get_opp_flips(move)
            if opp_flips > max_opp_flips:
                max_opp_flips = opp_flips
                best_move = move
        return best_move

    def is_winning_move(self, move: tuple) -> bool:
        """
        Checks if the game can be won by making this move.
        :param move: The move to be checked.
        :return: True if the game can be won by making this move, False otherwise.
        """
        row, col = move
        board_copy = copy.deepcopy(self._game.board)
        try:
            board_copy.make_move(row, col, self._symbol)
            if self.check_win(self._symbol, board_copy):
                return True
        except InvalidMoveException:
            return False
        return False

    def is_corner_move(self, move: tuple) -> bool:
        """
        Checks if the move is a corner move.
        :param move: The move to be checked.
        :return: True if the move is a corner move, False otherwise.
        """
        return move in [(0, 0), (0, 7), (7, 0), (7, 7)]

    def check_win(self, symbol: str, board: ReversiBoard) -> bool:
        """
        Checks if the game was won by a player.
        :param symbol: The symbol of the player to be checked.
        :param board: The current board state.
        :return: True if the game was won by the player, False otherwise.
        """
        opp_symbol = 'X' if symbol == 'O' else 'O'
        temp_score = {symbol: 0, opp_symbol: 0}
        for row in board.data:
            for cell in row:
                if cell == symbol:
                    temp_score[symbol] += 1
                elif cell == opp_symbol:
                    temp_score[opp_symbol] += 1

        if temp_score[symbol] + temp_score[opp_symbol] == 64 and temp_score[symbol] > temp_score[opp_symbol]:
            return True
        if temp_score[opp_symbol] == 0:
            return True
        return False

    def blocks_opponent_winning_move(self, move: tuple) -> bool:
        """
        Checks if the opponent can win by making a single move. If so, the computer will try to block that move.
        :param move: The move to be checked.
        :return: True if the opponent can win by making a single move, False otherwise.
        """
        row, col = move
        board_copy = copy.deepcopy(self._game.board)
        try:
            board_copy.make_move(row, col, self._symbol)
            if self.check_win(self._opp_symbol, board_copy):
                return True
        except InvalidMoveException:
            return False
        return False

    def get_opp_flips(self, move: tuple) -> int:
        """
        Gets the total number of opponent flips that will be made if the move is made.
        :param move: The move to be checked.
        :return: The total number of opponent flips that will be made.
        """
        flips = 0
        for direction in self._directions:
            dir_flips = 0
            row, col = move
            row += direction[0]
            col += direction[1]
            while 0 <= row < 8 and 0 <= col < 8:
                if self._game.get_cell_value(row, col) == self._opp_symbol:
                    dir_flips += 1
                    row += direction[0]
                    col += direction[1]
                elif self._game.get_cell_value(row, col) == self._symbol:
                    flips += dir_flips
                    break
                else:
                    break
        return flips

class ComputerMediumStrategy(ComputerStrategy):
    def __init__(self, game, depth = 3):
        """
        Constructor for ComputerMediumStrategy class.
        :param game: The Othello game that the strategy will be used for.
        :param depth: The depth of the minimax algorithm.
        """
        super().__init__(game)
        self._depth = depth

    def get_move(self, board: ReversiBoard, symbol: str) -> tuple:
        """
        Gets the best move that the computer will make using the minimax algorithm.
        :param board: The current board state.
        :param symbol: The symbol of the computer player.
        :return: The move that the computer will make.
        """
        valid_moves = self._game.get_valid_moves(symbol)
        if not valid_moves:
            raise NoValidMovesException("No valid moves for computer. Skipping its turn.")

        best_move = valid_moves[0]
        best_score = float('-inf')

        for move in valid_moves:
            board_copy = copy.deepcopy(board)
            row, col = move
            try:
                board_copy.make_move(row, col, symbol)
                score = self.minimax(board_copy, self._depth, False, symbol)
                if score > best_score:
                    best_score = score
                    best_move = move
            except InvalidMoveException:
                continue
        return best_move

    def minimax(self, board: ReversiBoard, depth: int, maximizing: bool, symbol: str) -> int:
        """
        The minimax algorithm. It will recursively evaluate the board state to find the best move.
        :param board: The current board state.
        :param depth: The remaining depth of the algorithm. The algorithm will stop when depth is 0.
        :param maximizing: True if the current layer is maximizing (trying to get the highest score),
         False if it is minimizing (simulating the opponent's turn).
        :param symbol: The symbol of the computer player.
        :return: The score of the board state (a higher score is better for the computer player).
        """
        opp_symbol = 'X' if symbol == 'O' else 'O'
        valid_moves = self._game.get_valid_moves(symbol if maximizing else opp_symbol)

        if depth == 0 or not valid_moves:
            return self.evaluate_board(board, symbol)

        if maximizing: # Computer's turn
            max_score = float('-inf')
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                row, col = move
                try:
                    board_copy.make_move(row, col, symbol)
                    score = self.minimax(board_copy, depth - 1, False, symbol)
                    max_score = max(max_score, score)
                except InvalidMoveException:
                    continue
            return max_score
        else: # Simulate opponent's best move (in order to minimize the score for the next recursive step)
            min_score = float('inf')
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                row, col = move
                try:
                    board_copy.make_move(row, col, opp_symbol)
                    score = self.minimax(board_copy, depth - 1, True, symbol)
                    min_score = min(min_score, score)
                except InvalidMoveException:
                    continue
            return min_score

    def evaluate_board(self, board: ReversiBoard, symbol: str) -> int:
        """
        Evaluates the board state in order to determine how favorable it is for the computer player.
        :param board: The current board state.
        :param symbol: The symbol of the computer player.
        :return: The score of the board state. A higher score is better for the computer player.
        """
        opp_symbol = 'X' if symbol == 'O' else 'O'
        computer_score = sum([row.count(symbol) for row in board.data])
        human_score = sum([row.count(opp_symbol) for row in board.data])

        # Weight corners more (they are permanent and cannot be flipped)
        corner_weight = 10
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for corner in corners:
            row, col = corner
            if board.data[row][col] == symbol:
                computer_score += corner_weight
            elif board.data[row][col] == opp_symbol:
                human_score += corner_weight

        return computer_score - human_score
