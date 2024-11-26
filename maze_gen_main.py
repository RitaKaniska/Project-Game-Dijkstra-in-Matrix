from tkinter import *
from random import randint


nrow = 11
ncolumn = 17
visited_cells = []
walls = []

nrow += 2
ncolumn += 2
map =  [['0' for _ in range(ncolumn)]for _ in range(nrow)]

class Maze():        
    def __init__(self):
        self.points = []
        self.pointsW = []

    def set_up_maze(self):
        scr = randint(1, nrow-2)
        scc = randint(1, ncolumn-2)
        self.start_color = 'Green'
        ccr, ccc = scr, scc

        map[ccr][ccc] = '1'
        finished = False
        while not finished:
            visitable_neighbours = self.check_neighbours(ccr, ccc)
            if len(visitable_neighbours) != 0:
                d = randint(1, len(visitable_neighbours))-1
                ncr, ncc = visitable_neighbours[d]
                map[ncr][ncc] = '1'
                visited_cells.append([ncr, ncc])
                ccr, ccc = ncr, ncc
            if len(visitable_neighbours) == 0:
                try:
                    ccr, ccc = visited_cells.pop()
                except:
                    finished = True       
        self.create()

    def regen(self):
        global map,visited_cells
        map.clear()
        visited_cells.clear()
        map = [['0' for _ in range(ncolumn)]for _ in range(nrow)]
        self.points.clear()
        self.pointsW.clear()
        self.points.append([-1,-1]) #insert 2 initial START & END points
        self.points.append([-1,-1])
        self.set_up_maze()
        self.switch_to_tkinter()
       
    def create(self):
        print("======================")
        for r in map:
            for c in r:
                print(c,end = " ")
            print()

    def check_neighbours(self,ccr, ccc):
        neighbours = [[ccr, ccc-1, ccr-1, ccc-2, ccr, ccc-2, ccr+1, ccc-2, ccr-1, ccc-1, ccr+1, ccc-1], #left
                    [ccr, ccc+1, ccr-1, ccc+2, ccr, ccc+2, ccr+1, ccc+2, ccr-1, ccc+1, ccr+1, ccc+1], #right
                    [ccr-1, ccc, ccr-2, ccc-1, ccr-2, ccc, ccr-2, ccc+1, ccr-1, ccc-1, ccr-1, ccc+1], #top
                    [ccr+1, ccc, ccr+2, ccc-1, ccr+2, ccc, ccr+2, ccc+1, ccr+1, ccc-1, ccr+1, ccc+1]] #bottom
        visitable_neighbours = []           
        for i in neighbours:                                                                        #find neighbours to visit
            if i[0] > 0 and i[0] < (nrow-1) and i[1] > 0 and i[1] < (ncolumn-1):
                if map[i[2]][i[3]] == '1' or map[i[4]][i[5]] == '1' or map[i[6]][i[7]] == '1' or map[i[8]][i[9]] == '1' or map[i[10]][i[11]] == '1':
                    walls.append(i[0:2])                                                                                               
                else:
                    visitable_neighbours.append(i[0:2])
        return visitable_neighbours

    def switch_to_tkinter(self):
        found_p = False
        self.startP = [0,0]
        for i in range(0,ncolumn-1):
            for j in range(0,nrow-1):
                if (map[i+1][j+1] == '1'):
                    self.startP[0],self.startP[1] = j,i #warning: flipped (x=i & y=j)
                    found_p = True 
                    break
            if (found_p): break
        currentP = self.startP
        dir_prev = 3 #left,up,right,down = 0,1,2,3
        while(True):
            route = []
            pointNext = [[currentP[0],currentP[1]-1],[currentP[0]-1,currentP[1]],[currentP[0],currentP[1]+1],[currentP[0]+1,currentP[1]]]
            #left
            if not dir_prev == 2 and (map[currentP[0]][currentP[1]] == '1' or map[currentP[0]+1][currentP[1]] == '1'):
                route.append(0)
            #up
            if not dir_prev == 3 and (map[currentP[0]][currentP[1]] == '1' or map[currentP[0]][currentP[1]+1] == '1'):
                route.append(1)
            #right
            if not dir_prev == 0 and (map[currentP[0]][currentP[1]+1] == '1' or map[currentP[0]+1][currentP[1]+1] == '1'):
                route.append(2)
            #down
            if not dir_prev == 1 and (map[currentP[0]+1][currentP[1]] == '1' or map[currentP[0]+1][currentP[1]+1] == '1'):
                route.append(3)

            chosenR = [-1,-1]
            priority,dir = 4,-1
            for d in route:
                if (dir_prev+3)%4 == d and (priority>0):
                    chosenR = pointNext[d]
                    priority = 0
                    dir = d
                    break
                elif (d == dir_prev) and (priority>1):
                    chosenR = pointNext[d]
                    priority = 1
                    dir = d
                elif (priority>2): 
                    chosenR = pointNext[d] 
                    priority = 2
                    dir = d
            if (dir != dir_prev):
                self.points.append(currentP)
                dir_prev = dir
            currentP = chosenR

            if (self.startP == currentP): break
        
        for p in self.points:
            #p[0] = p[0] * 40 + 80
            #p[1] = p[1] * 40 + 80
            p[0],p[1] = p[1],p[0]
            self.pointsW.append([(p[0]+1)*40 + 40,(p[1]+1)*40 +40])'''

