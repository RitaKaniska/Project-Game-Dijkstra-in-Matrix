import tkinter
import tkinter.font
import math
import queue
import time
from unittest import skip
from maze_gen_main import*
from turtle import distance, left, position
from shapely.geometry import Point, LineString
from shapely.geometry.polygon import Polygon

class myGUI():
    def __init__(self,app):
        top_frame = tkinter.Frame(app)
        bot_frame = tkinter.Frame(app)
        app.title("Dijkstra")
        # setting window size
        width=880
        height=720
        size_str = '%dx%d' % (width, height)
        app.geometry(size_str)
        app.resizable(width=False, height=False)

        self.graph_time, self.dijkstra_time, self.distance = -1,-1,-1
        self.res = []

        but_map = tkinter.Button(top_frame,text="RANDOM MAP",font=tkinter.font.Font(size=16),command=self.draw_graph, bg = '#ea9999')
        but_run = tkinter.Button(top_frame,text="RUN",font=tkinter.font.Font(size=16),command=self.VisibleMode, bg = '#f9ee9c')
        but_dji = tkinter.Button(top_frame,text="DIJKSTRA",font=tkinter.font.Font(size=16),command=self.dijkstra, bg = '#9fc5e8')

        but_vis = tkinter.Button(top_frame,text="VISIBLE",font=tkinter.font.Font(size=16),command=self.checkVisible,bg = '#93c47d')
        self.visible = False

        self.canvas = tkinter.Canvas(bot_frame,width=840,height=600,background='#CAFFF9')

        self.canvas.bind("<Button-1>", self.addStart)
        self.canvas.bind("<Button-3>", self.addEnd)
        self.checkStart, self.checkEnd, self.EinP,self.SinP,self.checkGraph, self.checkMap = False,False,False,False,False,False

        self.infoText = tkinter.Label(bot_frame, font=tkinter.font.Font(size=14),
                                             text="", bg="#69BF61", width=53, height=25)

        but_map.pack(side="left", fill="both", expand=True)
        but_vis.pack(side="left", fill="both", expand=True)
        but_dji.pack(side="left", fill="both", expand=True)
        self.canvas.pack()
        top_frame.pack()
        bot_frame.pack()
        self.infoText.pack()

        self.graph = {}
        self.vertices = {}

    def UpdateInfo(self):
        text = ""
        if self.checkStart:
            text = "Start point: [" + ("%.2f" % (maze.points[0][0]+1)) + (", %.2f" % (nrow - 1 - maze.points[0][1])) + "]   "
        if self.checkEnd:
            text += "End point: [" + ("%.2f" % (maze.points[1][0]+1)) + (", %.2f" % (nrow - 1 - maze.points[1][1]+1)) + "]\n"
        if self.graph_time != -1:
            text += "Graph Time: " + ("%.5f" % self.graph_time) + "s |"
        if self.dijkstra_time != -1:
            text += "  Dijkstra Time: " + ("%.5f" % self.dijkstra_time) + "s |"
        if self.dijkstra_time != -1 and self.graph_time != -1: 
            text += "  Total: " + ("%.5f" % (self.dijkstra_time + self.graph_time)) + "s\n"
        if self.distance != -1:
            text += "Distance: " + ("%.2f" % self.distance)
        self.infoText["text"] = text

    def gen_map(self):
        self.canvas.delete("all")
        maze.regen()
        self.graph.clear()
        self.vertices.clear()
        self.checkStart, self.checkEnd, self.EinP,self.SinP,self.checkGraph, self.checkMap = False,False,False,False,False,True
        self.graph_time, self.dijkstra_time, self.distance = -1,-1,-1
        self.res.clear()
        self.UpdateInfo()
        for i in range(len(maze.points)):
            self.graph[i]=[]
            self.vertices[i]=[]
        self.canvas.create_polygon(maze.pointsW[2:len(maze.pointsW)],fill = "#0099FF")
        self.visible = False
    
    def draw_graph(self, redraw = True):
        self.canvas.delete("all")
        if redraw: self.gen_map()
        else: self.canvas.create_polygon(maze.pointsW[2:len(maze.pointsW)],fill = "#0099FF")
        self.draw_line(0, 0, 0, nrow, "black", 2)
        self.draw_line(0, nrow, ncolumn, nrow, "black", 2)

        if (self.visible):
            for i in self.vertices:
                for j in self.vertices.get(i):
                    self.draw_line(maze.points[i][0] + 1, maze.points[i][1] + 1, maze.points[j][0] + 1, maze.points[j][1] + 1, "yellow", 1.25)

        if (self.checkStart):
            self.draw_point(maze.points[0][0] + 1, maze.points[0][1] + 1, "red", "S")
        if (self.checkEnd):
            self.draw_point(maze.points[1][0] + 1, maze.points[1][1] + 1, "#33FF00", "E")
        if self.res:
            for i in range(0,len(self.res)-1):
                x1, y1, x2, y2 = maze.points[self.res[i]][0]+1, maze.points[self.res[i]][1]+1, maze.points[self.res[i+1]][0]+1, maze.points[self.res[i+1]][1]+1
                self.draw_line(x1, y1, x2, y2, "black", 3)

        for i in range(1, nrow):
            self.draw_line(0, i, -0.15, i, color="black", w = 1, n = nrow - i)
        self.canvas.create_text(-0.15 * 40 + 30, nrow * 40 + 55, text= 0, font=tkinter.font.Font(size=14, weight='bold'))                   
        for i in range(1, ncolumn):
            self.draw_line(i, nrow, i, nrow + 0.15, color="black", w = 1, n = i)

    def draw_line(self, x1, y1, x2, y2, color="", w = 1, n = -1):
        self.canvas.create_line(x1 * 40 + 40, y1 * 40 + 40,
                                x2 * 40 + 40, y2 * 40 + 40,
                                fill=color, width=w)
        if (n!=-1): 
            if x1==0: self.canvas.create_text(x2 * 40 + 25, y2 * 40 + 40, text= n, font=tkinter.font.Font(size=14, weight='bold'))                   
            else: self.canvas.create_text(x2 * 40 + 40, y2 * 40 + 55, text= n, font=tkinter.font.Font(size=14, weight='bold'))
            
    def draw_point(self, x1, y1, color="", t = -1):
        self.canvas.create_oval(x1 * 40 + 36, y1 * 40 + 36,
                                x1 * 40 + 44, y1 * 40 + 44,
                                fill=color)
        self.canvas.create_text(x1 * 40 + 38 - 6, y1 * 40 + 38 - 6, text= t,
                                font=tkinter.font.Font(size=14, weight='bold'))
    
    def addStart(self, event):
        if self.checkMap:
            print(event.x, event.y)
            self.res.clear()
            maze.pointsW[0] = [event.x,event.y]
            location = [(event.x-40)/40 - 1, (event.y-40)/40 - 1]
            maze.points[0] = location
            self.checkStart = True
            self.UpdateInfo()
            self.VisibleMode(1)

    def addEnd(self, event):
        if self.checkMap:
            print(event.x, event.y)
            self.res.clear()
            maze.pointsW[1] = [event.x,event.y]
            location = [(event.x-40)/40 - 1, (event.y-40)/40 - 1]
            maze.points[1] = location
            self.checkEnd = True
            self.UpdateInfo()
            self.VisibleMode(1)

    def ResetSE(self,x):
        self.vertices[x].clear()
        self.graph[x].clear()
        for key, value in self.graph.items():
            for i in range(len(value)):
                if value[i][0] == x:
                    value.pop(i)
                    break
    
    def dijkstra(self):
        timeStart = time.time()
        if (self.checkStart and self.checkEnd and self.checkGraph and self.SinP and self.EinP):
            l = len(maze.points)
            D = [float('inf') for v in range(l+1)]
            D[0] = 0
            visited = [0 for i in range(l+1)]
            trace = [-1 for i in range(l+1)]
            trace[0] = 0
            pq = queue.PriorityQueue()
            pq.put((0, 0))
            while not pq.empty():
                (dist, current_vertex) = pq.get()
                visited[current_vertex] = 1
                if current_vertex == 1:
                    break
                for i in self.graph:
                    if (i == current_vertex):
                        for j in self.graph.get(i):
                            neighbor = j[0]
                            distance = j[1]

                            if visited[neighbor] == 0:
                                old_cost = D[neighbor]
                                new_cost = D[current_vertex] + distance
                                if new_cost < old_cost:
                                    pq.put((new_cost, neighbor))
                                    D[neighbor] = new_cost
                                    trace[neighbor] = current_vertex
            v = 1  # Trace
            while v != 0:
                self.res.append(v)
                x1, y1 = maze.points[v][0]+1,maze.points[v][1]+1
                v = trace[v]
                x2, y2 = maze.points[v][0]+1,maze.points[v][1]+1
                self.draw_line(x1, y1, x2, y2, "black", 3)
            self.res.append(v)
            self.draw_point(maze.points[0][0] + 1, maze.points[0][1] + 1, "red", "S")
            self.draw_point(maze.points[1][0] + 1, maze.points[1][1] + 1, "#33FF00", "E")

            self.dijkstra_time = time.time() - timeStart
            self.distance = D[1]
            print(self.res)
            self.UpdateInfo()

    def VisibleMode(self, event = 0): # mode 0 - graph w/o starting and ending point, mode 1/2 - update starting/ending point
        s = 0
        e = 0
        timeStart = time.time()
        self.visible = True
        l = len(maze.points)
        p = maze.pointsW[2:l]
        main_polygon = Polygon(p)
        if (event == 0):
            if (self.checkGraph == False): self.checkGraph = True
            s = 2
            e = l
            
        elif (event == 1 and self.checkGraph == True):
            s,e = 0,2
            self.ResetSE(0)
            self.ResetSE(1)
            if main_polygon.contains(Point(maze.pointsW[0][0],maze.pointsW[0][1])): self.SinP = True
            else: self.SinP = False
            if main_polygon.contains(Point(maze.pointsW[1][0],maze.pointsW[1][1])): self.EinP = True
            else: self.EinP = False
        for i in range(s,e):
            for j in range(i+1,l):
                path = LineString([maze.pointsW[i],maze.pointsW[j]])
                point = path.interpolate(0.5)
                if not path.crosses(main_polygon) and (main_polygon.contains(point) or (j-i==1 and i!=0 and i!=1) or (i == 2 and j == l-1)):
                        vertLen = [j, math.sqrt((maze.points[i][0]-maze.points[j][0])**2 + (maze.points[i][1]-maze.points[j][1])**2)]
                        self.graph[i].append(vertLen)
                        vertLen = [i, math.sqrt((maze.points[i][0]-maze.points[j][0])**2 + (maze.points[i][1]-maze.points[j][1])**2)]
                        self.graph[j].append(vertLen)
                        self.vertices[i].append(j)
        if (event == 0):
            self.graph_time = time.time() - timeStart
            self.UpdateInfo()
            if (self.checkStart or self.checkEnd): 
                self.VisibleMode(1)
                return
        self.draw_graph(False)

    def checkVisible(self):
        self.visible = not self.visible
        self.draw_graph(False)

app = tkinter.Tk() # Create the main window widget.
maze = Maze()
my_gui = myGUI(app)
app.mainloop()