import tkinter as tk
import numpy as np
from tkinter import messagebox
from tkinter import Grid


WIDTH = 4
HEIGHT = 4
GAME_NAME = "Pyatnashki"

class Point:
    def __init__(self, array, x, y):
        self.array = array
        self.x = x
        self.y = y

    def is_valid(self):
        return 0 <= self.x < WIDTH and 0 <= self.y < HEIGHT

    def is_empty(self):
        return self.array[self.x, self.y] <= 0


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.buttons = []
        self.grid()
        self.createWidgets()

        for i in range(WIDTH):
            Grid.columnconfigure(self, i, weight=1)

        for i in range(HEIGHT+1):
            Grid.rowconfigure(self, i, weight=1)

        self.createBoard()


    def createBoard(self):
        self.initArr()
        self.redraw()

    def initArr(self):
        arr = np.arange(WIDTH * HEIGHT)
        np.random.shuffle(arr)
        # for checking win window
        # arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 13, 14, 11, 0])
        while not self.checkForSolution(arr):
            arr = np.arange(WIDTH * HEIGHT)
            np.random.shuffle(arr)
        arr.resize((WIDTH, HEIGHT))
        self.arr = arr

    def checkForSolution(self, arr):
        total_sum = 0
        for i in range(WIDTH * HEIGHT):
            n_numbers_that_less_i = 0
            for j in range(i + 1, WIDTH * HEIGHT):
                if arr[j] != 0 and arr[j] < arr[i]:
                    n_numbers_that_less_i += 1
            total_sum += n_numbers_that_less_i

        for i in range(WIDTH * HEIGHT):
            if arr[i] == 0:
                total_sum += i / 4 + 1
            return total_sum % 2 == 0

    def createWidgets(self):
        self.newButton = tk.Button(self, text='New', command=self.createBoard)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.newButton.grid(row=0, column=0, columnspan=2, sticky='NSEW')
        self.quitButton.grid(row=0, column=2, columnspan=2, sticky='NSEW')

    def redraw(self):
        self.destroyGrid()
        self.createGrid()

    def destroyGrid(self):
        for b in self.buttons:
            b.destroy()
        self.buttons = []

    def createGrid(self):


        for i in range(WIDTH):
            for j in range(HEIGHT):
                number = self.arr[i, j]
                if number <= 0:
                    continue
                b = tk.Button(self, text=str(number), width=10, height=5)
                b.grid(row=i + 1, column=j, sticky='NSEW')

                def proxy_click(i, j):
                    return lambda: self.onclick(i, j)

                b.config(command=proxy_click(i, j))
                self.buttons.append(b)

    def onclick(self, x, y):
        empty_cell = self.find_empty_cell(x, y)
        if empty_cell is None:
            return
        num_for_move = self.arr[x, y]
        self.arr[x, y] = 0
        self.arr[empty_cell.x, empty_cell.y] = num_for_move
        self.redraw()
        self.checkForWin()

    def checkForWin(self):
        if self.arr[WIDTH - 1, HEIGHT - 1] != 0:
            return
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if i == WIDTH - 1 and j == HEIGHT - 1:
                    continue
                if self.arr[i, j] != i * WIDTH + j + 1:
                    return
        messagebox.showinfo(GAME_NAME, "Congratulations!!!")
        self.createBoard()

    def find_empty_cell(self, x, y) -> Point:
        top = Point(self.arr, x, y + 1)
        right = Point(self.arr, x + 1, y)
        bottom = Point(self.arr, x, y - 1)
        left = Point(self.arr, x - 1, y)

        if top.is_valid() and top.is_empty():
            return top
        if right.is_valid() and right.is_empty():
            return right
        if bottom.is_valid() and bottom.is_empty():
            return bottom
        if left.is_valid() and left.is_empty():
            return left

        return None


if __name__ == '__main__':
    app = Application()
    app.master.title(GAME_NAME)
    app.mainloop()
