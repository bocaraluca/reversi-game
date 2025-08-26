import tkinter as tk
from tkinter import messagebox

from exceptions.exceptions import NoValidMovesException


class GraphicUi:
    def __init__(self, service):
        self._service = service
        self.board = self._service.get_board()
        self.score_label = None
        self.human_player = self._service.get_human_player()
        self.computer_player = self._service.get_computer_player()
        self.buttons = []
        self.window = tk.Tk()
        self.set_window()
        self.create_board()
        self.create_score_label()
        messagebox.showinfo("Your Color",
                            f"You are {'Black. You go first.' if self.human_player == 'X' else 'White. The computer goes first.'}")
        if self.human_player == 'O':
            self._service.play_computer_move()
            self.update_board()

    def set_window(self):
        self.window.title('Othello Game')
        self.window.geometry('530x600')
        window_width = 530
        window_height = 600
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def create_score_label(self):
        self.score_label = tk.Label(self.window, text='', font=('Arial', 14))
        self.score_label.grid(row=8, column=0, columnspan=8)
        self.update_score()

    def create_board(self):
        for row in range(8):
            row_buttons = []
            for col in range(8):
                cell_value = self.board.get_cell_value(row, col)
                color, state = self.get_button_properties(row, col, cell_value)

                button = tk.Button(self.window, width=8, height=4, bg=color, state=state,
                                   command=lambda r=row, c=col: self.handle_move(r, c))
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def get_button_properties(self, row, col, cell_value):
        # Determine the properties of the button based on the cell value
        if cell_value == 'X':
            color = 'black'
            state = 'disabled'
        elif cell_value == 'O':
            color = 'white'
            state = 'disabled'
        else:
            color = 'green'
            state = 'normal'

        if (row, col) in self._service.get_valid_human_moves():
            color = 'light green'

        return color, state

    def handle_move(self, row, col):
        # Check if the game is over before making a move
        if self._service.is_game_over():
            self.game_over()
            return

        # Human's turn
        if self._service.get_valid_human_moves():
            if self._service.is_valid_human_move(row, col):
                try:
                    self._service.play_human_move(row, col)
                    self.update_board()
                except NoValidMovesException:
                    messagebox.showinfo("No Valid Moves", "No valid moves for you. Skipping your turn.")
            else:
                messagebox.showwarning("Invalid Move", "Invalid move! Try again.")
                return
        else:
            messagebox.showinfo("No Valid Moves", "No valid moves for you. Skipping your turn.")

        # Check if the game is over after the human's turn
        if self._service.is_game_over():
            self.game_over()
            return

        # Computer's turn
        if self._service.get_valid_computer_moves():
            try:
                self._service.play_computer_move()
                self.update_board()
            except NoValidMovesException:
                messagebox.showinfo("No Valid Moves", "No valid moves for the computer. Skipping its turn.")
        else:
            messagebox.showinfo("No Valid Moves", "No valid moves for the computer. Skipping its turn.")

        # Final check if the game is over after the computer's move
        if self._service.is_game_over():
            self.game_over()

    def update_board(self):
        for row in range(8):
            for col in range(8):
                cell_value = self._service.get_cell_value(row, col)
                color, state = self.get_button_properties(row, col, cell_value)

                self.buttons[row][col].config(bg=color, state=state)
        self.update_score()

    def game_over(self):
        score = self._service.get_score()
        human_score = score[self.human_player]
        computer_score = score[self.computer_player]
        if human_score > computer_score:
            message = f'You have won with {human_score} points!'
        elif computer_score > human_score:
            message = f'The computer has won with {computer_score} points!'
        else:
            message = "It's a draw!"

        messagebox.showinfo("Game Over", message)
        self.window.quit()

    def update_score(self):
        score = self._service.get_score()
        human_score = score[self.human_player]
        computer_score = score[self.computer_player]
        if self.human_player == 'X':
            score_text = f'Black: {human_score} White: {computer_score}'
        else:
            score_text = f'Black: {computer_score} White: {human_score}'
        self.score_label.config(text=score_text)

    def play(self):
        self.window.mainloop()
