import tkinter as tk
import tkinter.filedialog as fd
from tkinter.messagebox import showerror
import json
import numpy as np
import copy

WINDOW_MIN_X = 300
WINDOW_MIN_Y = 230
BOARD_DIM = 9
board_fields = BOARD_DIM * BOARD_DIM
test_f = []
grid = []
org_grid = []


def possible(row, col, n):
    global grid
    for i in range(0, BOARD_DIM):
        if grid[row][i] == n:
            # print(f"exists on column {i}")
            return False
    for i in range(0, BOARD_DIM):
        if grid[i][col] == n:
            # print("exists on row x")
            return False

    ts_row = (row // 3) * 3
    ts_col = (col // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[ts_row + i][ts_col + j] == n:
                # print("exists on small cube")
                return False

    return True


def solve():
    global grid
    for row in range(BOARD_DIM):
        for col in range(BOARD_DIM):
            if grid[row][col] == 0:
                for n in range(1, BOARD_DIM + 1):
                    if possible(row, col, n):
                        grid[row][col] = n
                        solve()
                        # check all field are diffrent from 0
                        if np.count_nonzero(grid) != board_fields:
                            grid[row][col] = 0
                return


def clean_board():
    for x in test_f:
        x.delete(0, tk.END)
    # TODO: clean must clean formating and numbers


def resolve():
    for x in test_f:
        x.config(state="disabled")
    global grid, org_grid
    org_grid = get_board_val_to_array(test_f)
    grid = copy.deepcopy(org_grid)
    solve()
    for x in test_f:
        x.config(state="normal")
    if arr_eq(grid, org_grid):
        showerror(title="Error", message="Can't resolve this sudoku")
    else:
        fl_str = flat_board(grid)
        for i, x in enumerate(test_f, start=0):
            x.insert(0, fl_str[i])


def field_validate(x):
    if x == "" or (len(x) <= 1 and x.isdigit()):
        return True
    else:
        return False


def get_board_val_to_array(entry_list):
    _l = [int(x.get()) if x.get() else 0 for x in entry_list]
    arr = [x.tolist() for x in np.array_split(np.array(_l), BOARD_DIM)]
    return arr


def arr_eq(list1, list2):
    for z1, z2 in zip(list1, list2):
        for a, b in zip(z1, z2):
            if a != b:
                return False
    return True


def export_board():
    f = fd.asksaveasfile(mode="w", defaultextension=".json")
    if (
        f is None
    ):  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    global grid
    grid_json = json.dumps(grid, indent=4)
    f.write(grid_json)
    f.close()


def import_board():
    # file type
    filetypes = (("text files", "*.json"),)
    # show the open file dialog
    f = fd.askopenfile(filetypes=filetypes)
    # read the text file and show its content on the Text
    board = json.loads(f.read())
    flatList_str = flat_board(board)
    clean_board()
    for i, x in enumerate(test_f, start=0):
        x.insert(0, flatList_str[i])


def flat_board(board):
    fl = [item for elem in board for item in elem]
    fl_str = [str(x) if x != 0 else "" for x in fl]
    return fl_str


window = tk.Tk()
window.title("Simple sudoku game")
window.rowconfigure(0, minsize=50, weight=1)
window.columnconfigure([0, 1], minsize=80, weight=3)
window.minsize(WINDOW_MIN_X, WINDOW_MIN_Y)
window.maxsize(WINDOW_MIN_X, WINDOW_MIN_Y)
frm_sudoku_board = tk.Frame(master=window)
frm_btns = tk.Frame(master=window)
btn_clean = tk.Button(master=frm_btns, text="Clean", command=clean_board)
btn_resolve = tk.Button(master=frm_btns, text="Resolve", command=resolve)
btn_open_file = tk.Button(
    master=frm_btns, text="Open file", command=import_board
)
btn_save_file = tk.Button(
    master=frm_btns, text="Save to file", command=export_board
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
            validatecommand=(frm_sudoku_board.register(field_validate), "%P"),
        )
        label.grid(row=i, column=j, ipadx=4, padx=2, pady=2, sticky="nsew")
        test_f.append(label)

frm_btns.grid(row=0, column=0)
frm_sudoku_board.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
btn_clean.grid(row=0, column=0, sticky="nsew")
btn_resolve.grid(row=1, column=0, sticky="nsew")
btn_open_file.grid(row=2, column=0, sticky="nsew")
btn_save_file.grid(row=3, column=0, sticky="nsew")

window.mainloop()
