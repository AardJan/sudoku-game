import tkinter as tk
import numpy as np

# from solve_algorithm import solve

BOARD_DIM = 9
test_f = []
grid = []


def possible(y, x, n):
    global grid
    for i in range(0, 9):
        if grid[y][i] == n:
            return False
    for i in range(0, 9):
        if grid[i][x] == n:
            return False

    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0 + i][x0 + j] == n:
                return False

    return True


def solve():
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(x, y, n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0

                return
    print(np.matrix(grid))


def clean_board():
    for x in test_f:
        x.delete(0, tk.END)


def disable_board():
    for x in test_f:
        x.config(state="disabled")
    global grid
    grid = ge_board_val_to_array(test_f)
    print(grid)
    solve()


def validate(x):
    if x == "" or (len(x) <= 1 and x.isdigit()):
        return True
    else:
        return False


def ge_board_val_to_array(entry_list):
    _l = [int(x.get()) if x.get() else 0 for x in entry_list]
    arr = [x.tolist() for x in np.array_split(np.array(_l), BOARD_DIM)]
    return arr


window = tk.Tk()
window.title("Simple sudoku game")
window.rowconfigure(0, minsize=50, weight=1)
window.columnconfigure([0, 1], minsize=80, weight=3)
frm_sudoku_board = tk.Frame(master=window)
frm_btns = tk.Frame(master=window)
btn_clean = tk.Button(master=frm_btns, text="Clean", command=clean_board)
btn_disable = tk.Button(master=frm_btns, text="Disable", command=disable_board)

for i in range(BOARD_DIM):
    frm_sudoku_board.columnconfigure(i, weight=1, minsize=1)
    frm_sudoku_board.rowconfigure(i, weight=1, minsize=1)

    for j in range(BOARD_DIM):
        label = tk.Entry(
            master=frm_sudoku_board,
            width=1,
            justify="center",
            validate="all",
            validatecommand=(frm_sudoku_board.register(validate), "%P"),
        )
        label.grid(row=i, column=j, ipadx=4, padx=2, pady=2)
        test_f.append(label)

frm_btns.grid(row=0, column=0)
frm_sudoku_board.grid(row=0, column=1, padx=5, pady=5)
btn_clean.grid(row=0, column=0, sticky="nsew")
btn_disable.grid(row=1, column=0, sticky="nsew")

window.mainloop()
