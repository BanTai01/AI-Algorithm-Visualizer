import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")

        self.board = [" " for _ in range(9)]  # 9 cells on the board
        self.current_player = "X"  # X always starts
        self.game_over = False

        self.buttons = []
        for i in range(9):
            button = tk.Button(master, text=" ", width=10, height=3, font=('normal', 20),
                               command=lambda i=i: self.make_move(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=3, column=0, columnspan=3, pady=10)

    def make_move(self, index):
        if self.board[index] == " " and not self.game_over:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            if self.check_winner(self.current_player):
                self.game_over = True
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                return

            if " " not in self.board:
                self.game_over = True
                messagebox.showinfo("Game Over", "It's a draw!")
                return

            # Switch player
            self.current_player = "O" if self.current_player == "X" else "X"
            if self.current_player == "O":
                self.computer_move()

    def check_winner(self, player):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False

    def computer_move(self):
        _, best_move = self.minimax(self.board, "O")
        if best_move is not None:
            self.make_move(best_move)

    def minimax(self, board, player, alpha=-float('inf'), beta=float('inf')):
        opponent = "O" if player == "X" else "X"

        # Check base cases
        if self.check_winner("O"):
            return 1, None
        elif self.check_winner("X"):
            return -1, None
        elif " " not in board:
            return 0, None

        moves = [i for i, x in enumerate(board) if x == " "]
        best_move = None

        if player == "O":  # Maximizing (AI)
            best_score = -float('inf')
            for move in moves:
                board[move] = player
                score, _ = self.minimax(board, opponent, alpha, beta)
                board[move] = " "

                if score > best_score:
                    best_score = score
                    best_move = move

                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta cut-off
        else:  # Minimizing (human)
            best_score = float('inf')
            for move in moves:
                board[move] = player
                score, _ = self.minimax(board, opponent, alpha, beta)
                board[move] = " "

                if score < best_score:
                    best_score = score
                    best_move = move

                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha cut-off

        return best_score, best_move

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.game_over = False
        for button in self.buttons:
            button.config(text=" ")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
