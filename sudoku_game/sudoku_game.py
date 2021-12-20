import tkinter as tk
import tkinter.filedialog as fd
import json
import numpy as np

# from solve_algorithm import solve

BOARD_DIM = 9
test_f = []
grid = []

# TODO: fix xy position on board


def possible(row, col, n):
    global grid
    for i in range(0, 9):
        if grid[row][i] == n:
            print(f"exists on column {i}")
            return False
    for i in range(0, 9):
        if grid[i][col] == n:
            print("exists on row x")
            return False

    ts_row = (row // 3) * 3
    ts_col = (col // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[ts_row + i][ts_col + j] == n:
                print("exists on small cube")
                return False

    return True


def solve():
    global grid
    for row in range(9):
        for col in range(9):
            print(f"Value field (row:{row},col:{col})={grid[row][col]}")
            if grid[row][col] == 0:
                for n in range(1, 10):
                    print(f"try insert {n}")
                    if possible(row, col, n):
                        print(f"Value is possible {n}")
                        grid[row][col] = n
                        print(np.matrix(grid))
                        solve()
                        print("setup 0")
                        grid[row][col] = 0
                        print(np.matrix(grid))
                return
    print(np.matrix(grid))


def clean_board():
    for x in test_f:
        x.delete(0, tk.END)


def disable_board():
    for x in test_f:
        x.config(state="disabled")
    global grid
    grid = get_board_val_to_array(test_f)
    print(grid)
    solve()


def validate(x):
    if x == "" or (len(x) <= 1 and x.isdigit()):
        return True
    else:
        return False


def get_board_val_to_array(entry_list):
    _l = [int(x.get()) if x.get() else 0 for x in entry_list]
    arr = [x.tolist() for x in np.array_split(np.array(_l), BOARD_DIM)]
    return arr


def export_board(filename):
    pass


def import_board():
    # file type
    filetypes = (("text files", "*.json"), ("All files", "*.*"))
    # show the open file dialog
    f = fd.askopenfile(filetypes=filetypes)
    # read the text file and show its content on the Text
    board = json.loads(f.read())
    flatList = [item for elem in board for item in elem]
    flatList_str = [str(x) if x != 0 else "" for x in flatList]
    for i, x in enumerate(test_f, start=0):
        x.insert(0, flatList_str[i])


window = tk.Tk()
window.title("Simple sudoku game")
window.rowconfigure(0, minsize=50, weight=1)
window.columnconfigure([0, 1], minsize=80, weight=3)
frm_sudoku_board = tk.Frame(master=window)
frm_btns = tk.Frame(master=window)
btn_clean = tk.Button(master=frm_btns, text="Clean", command=clean_board)
btn_disable = tk.Button(master=frm_btns, text="Disable", command=disable_board)
btn_open_file = tk.Button(
    master=frm_btns, text="Open file", command=import_board
)

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
btn_open_file.grid(row=2, column=0, sticky="nsew")

window.mainloop()
