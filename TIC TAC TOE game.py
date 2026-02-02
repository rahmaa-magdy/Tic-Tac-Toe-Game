import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        #Window
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe – AI Game")
        self.window.geometry("420x650")
        self.window.configure(bg="#f4f6f8")
        self.window.resizable(False, False)

        #Game Data
        self.board = [' ' for _ in range(9)]
        self.human = 'X'
        self.ai = 'O'
        self.current_player = self.human

        #Header
        self.title_label = tk.Label(
            self.window,
            text="Tic Tac Toe",
            font=("Segoe UI", 22, "bold"),
            bg="#f4f6f8",
            fg="#333"
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = tk.Label(
            self.window,
            text="Play against AI (Minimax Algorithm)",
            font=("Segoe UI", 11),
            bg="#f4f6f8",
            fg="#666"
        )
        self.subtitle_label.pack(pady=(0, 15))

        #Status
        self.status_label = tk.Label(
            self.window,
            text="Your turn (X)",
            font=("Segoe UI", 14, "bold"),
            bg="#f4f6f8",
            fg="#2c7be5"
        )
        self.status_label.pack(pady=10)

        #Board Frame
        self.frame = tk.Frame(self.window, bg="#f4f6f8")
        self.frame.pack(pady=10)

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    self.frame,
                    text="",
                    font=("Segoe UI", 24, "bold"),
                    width=4,
                    height=2,
                    bg="white",
                    fg="#333",
                    activebackground="#e9ecef",
                    relief="solid",
                    bd=1,
                    command=lambda r=i, c=j: self.make_move(r, c)
                )
                button.grid(row=i, column=j, padx=6, pady=6)
                row.append(button)
            self.buttons.append(row)

        #Control Buttons
        self.reset_button = tk.Button(
            self.window,
            text="New Game",
            font=("Segoe UI", 12, "bold"),
            bg="#198754",
            fg="white",
            activebackground="#157347",
            relief="flat",
            padx=20,
            pady=8,
            command=self.reset_game
        )
        self.reset_button.pack(pady=20)

        #Footer
        self.footer = tk.Label(
            self.window,
            text="AI Project | Minimax + Alpha-Beta Pruning",
            font=("Segoe UI", 10),
            bg="#f4f6f8",
            fg="#888"
        )
        self.footer.pack(side="bottom", pady=15)

        self.window.mainloop()

    #Game Logic
    def make_move(self, row, col):
        index = 3 * row + col

        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.buttons[row][col].config(
                text=self.current_player,
                fg="#0d6efd" if self.current_player == 'X' else "#dc3545"
            )

            if self.check_winner(self.board, self.current_player):
                self.status_label.config(
                    text=f"{self.current_player} wins!",
                    fg="#198754"
                )
                self.disable_all_buttons()
                return

            if ' ' not in self.board:
                self.status_label.config(
                    text="It's a tie!",
                    fg="#fd7e14"
                )
                return

            if self.current_player == self.human:
                self.current_player = self.ai
                self.status_label.config(
                    text="AI is thinking...",
                    fg="#dc3545"
                )
                self.window.after(500, self.ai_move)
            else:
                self.current_player = self.human
                self.status_label.config(
                    text="Your turn (X)",
                    fg="#2c7be5"
                )

    def ai_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.ai
                score = self.minimax(self.board, 0, False, float('-inf'), float('inf'))
                self.board[i] = ' '

                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            row, col = best_move // 3, best_move % 3
            self.make_move(row, col)

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if self.check_winner(board, self.ai):
            return 10 - depth
        if self.check_winner(board, self.human):
            return depth - 10
        if ' ' not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.ai
                    score = self.minimax(board, depth + 1, False, alpha, beta)
                    board[i] = ' '
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.human
                    score = self.minimax(board, depth + 1, True, alpha, beta)
                    board[i] = ' '
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score

    def check_winner(self, board, player):
        for i in range(0, 9, 3):
            if board[i] == board[i + 1] == board[i + 2] == player:
                return True
        for i in range(3):
            if board[i] == board[i + 3] == board[i + 6] == player:
                return True
        if board[0] == board[4] == board[8] == player:
            return True
        if board[2] == board[4] == board[6] == player:
            return True
        return False

    def disable_all_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state="disabled")

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal", fg="#333")
        self.current_player = self.human
        self.status_label.config(
            text="Your turn (X)",
            fg="#2c7be5"
        )

if __name__ == "__main__":
    TicTacToe()
