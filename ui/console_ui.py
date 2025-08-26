from exceptions.exceptions import InvalidMoveException, NoValidMovesException
from service.service import Service


class ConsoleUi:
    def __init__(self, service):
        self._service = service

    def print_board(self):
        print(self._service.get_board())

    def print_score(self):
        score = self._service.get_score()
        print(f"Black (X): {score['X']} \nWhite (O): {score['O']}")

    def get_human_move(self):
        while True:
            try:
                move = input(">> ").strip().upper()
                if len(move) != 2 or move[0] not in 'ABCDEFGH' or not move[1].isdigit():
                    raise ValueError("Invalid input format. Use letter and number (e.g., D3).")
                col = ord(move[0]) - ord('A')
                row = int(move[1]) - 1
                return row, col
            except ValueError as ve:
                print(ve)

    def get_winner(self):
        score = self._service.get_score()
        if self._service.get_human_player() == 'X':
            if score['X'] > score['O']:
                print(f"You (black) win with {score['X']} points!")
            elif score['X'] < score['O']:
                print(f"Computer (white) wins with {score['O']} points!")
            else:
                print("It's a tie!")
        else:
            if score['X'] > score['O']:
                print(f"Computer (black) wins with {score['X']} points!")
            elif score['X'] < score['O']:
                print(f"You (white) win with {score['O']} points!")
            else:
                print("It's a tie!")

    def play(self):
        self.print_board()

        # Computer starts
        if self._service.get_human_player() == 'O':
            r, c = self._service.play_computer_move()
            print(f'Computer moved at {chr(c + 65)}{r + 1}')
            self.print_board()
            self.print_score()

        while not self._service.is_game_over():
            try:
                valid_moves = self._service.get_valid_human_moves()
                print("Your valid moves:", [f"{chr(c + 65)}{r + 1}" for r, c in valid_moves])
                row, col = self.get_human_move()
                self._service.play_human_move(row, col)

                self.print_board()
                self.print_score()

                if not self._service.is_game_over():
                    r, c = self._service.play_computer_move()
                    self.print_board()
                    print(f'Computer moved at {chr(c + 65)}{r + 1}')
                    self.print_score()

            except InvalidMoveException as e:
                print(e)
            except NoValidMovesException as e:
                print(e)

        print("Game over!")
        self.get_winner()
