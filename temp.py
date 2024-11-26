from hashlib import new
from tkinter import *
from random import randint
from tkinter import messagebox

cell_size = 60 #pixels
ms = 7 # rows and columns
row = 7
column = 6
visited_cells = []
walls = []


map =  [['*' for _ in range(ms)]for _ in range(ms)]

class Maze():
    def __init__(self):
        scr = randint(1, ms-2)
        scc = randint(1, ms-2)
        self.start_color = 'Green'
        ccr, ccc = scr, scc

        map[ccr][ccc] = '+'
        finished = False
        while not finished:
            visitable_neighbours = self.check_neighbours(ccr, ccc)
            if len(visitable_neighbours) != 0:
                d = randint(1, len(visitable_neighbours))-1
                ncr, ncc = visitable_neighbours[d]
                map[ncr][ncc] = '+'
                visited_cells.append([ncr, ncc])
                ccr, ccc = ncr, ncc
            if len(visitable_neighbours) == 0:
                try:
                    ccr, ccc = visited_cells.pop()
                except:
                    finished = True


        self.window = Tk()
        self.window.title('Maze')
        self.canvas_side = ms*cell_size
        self.ffs = Canvas(self.window, width = self.canvas_side, height = self.canvas_side, bg = 'grey')
        self.ffs.pack()


        self.create()
        self.draw(scr, scc, self.start_color)
        
    def do(self):
        self.ffs.delete("all")
        global map,visited_cells
        map.clear()
        visited_cells.clear()
        map = [['*' for _ in range(ms)]for _ in range(ms)]
        scr = randint(1, ms-2)
        scc = randint(1, ms-2)
        self.start_color = 'Green'
        ccr, ccc = scr, scc

        map[ccr][ccc] = '+'
        finished = False
        while not finished:
            visitable_neighbours = self.check_neighbours(ccr, ccc)
            if len(visitable_neighbours) != 0:
                d = randint(1, len(visitable_neighbours))-1
                ncr, ncc = visitable_neighbours[d]
                map[ncr][ncc] = '+'
                visited_cells.append([ncr, ncc])
                ccr, ccc = ncr, ncc
            if len(visitable_neighbours) == 0:
                try:
                    ccr, ccc = visited_cells.pop()
                except:
                    finished = True
        self.create()
        self.draw(scr, scc, self.start_color)
       

    def create(self):
        for row in range(ms):
            for col in range(ms):
                if map[row][col] == '+':
                    color = 'White'
                elif map[row][col] == '*':
                    color = 'black'
                self.draw(row, col, color)
        print("======================")
        for r in map:
            for c in r:
                print(c,end = " ")
            print()

    def draw(self,row, col, color):
        x1 = col*cell_size
        y1 = row*cell_size
        x2 = x1+cell_size
        y2 = y1+cell_size
        self.ffs.create_rectangle(x1, y1, x2, y2, fill=color,outline=color)



    def check_neighbours(self,ccr, ccc):
        neighbours = [[ccr, ccc-1, ccr-1, ccc-2, ccr, ccc-2, ccr+1, ccc-2, ccr-1, ccc-1, ccr+1, ccc-1], #left
                    [ccr, ccc+1, ccr-1, ccc+2, ccr, ccc+2, ccr+1, ccc+2, ccr-1, ccc+1, ccr+1, ccc+1], #right
                    [ccr-1, ccc, ccr-2, ccc-1, ccr-2, ccc, ccr-2, ccc+1, ccr-1, ccc-1, ccr-1, ccc+1], #top
                    [ccr+1, ccc, ccr+2, ccc-1, ccr+2, ccc, ccr+2, ccc+1, ccr+1, ccc-1, ccr+1, ccc+1]] #bottom
        visitable_neighbours = []           
        for i in neighbours:                                                                        #find neighbours to visit
            if i[0] > 0 and i[0] < (ms-1) and i[1] > 0 and i[1] < (ms-1):
                if map[i[2]][i[3]] == '+' or map[i[4]][i[5]] == '+' or map[i[6]][i[7]] == '+' or map[i[8]][i[9]] == '+' or map[i[10]][i[11]] == '+':
                    walls.append(i[0:2])                                                                                               
                else:
                    visitable_neighbours.append(i[0:2])
        return visitable_neighbours

a = Maze()
but_map = Button(a.window,text="Create a random map",command=a.do)
but_map.pack()
a.window.mainloop()