import numpy as np
from PIL import Image

class Queue:
    def __init__(self):
        self.q = []

    def __len__(self):
        return len(self.q)

    def enqueue(self, x):
        self.q.append(x)

    def dequeue(self):
        return self.q.pop(0)

#Converting 3d array[x,y,RGBA] to 2d array[x,y]
def createMap(pix):
    map = np.zeros((pix.shape[0],pix.shape[1]), dtype='uint8')

    for x in range(len(pix)):
        for y in range(len(pix[x])):
                if pix[x,y,0] == 255 and pix[x,y,1] == 255 and pix[x,y,2] == 255:
                    map[x,y] = 1
                elif pix[x,y,0] == 0 and pix[x,y,1] == 255 and pix[x,y,2] == 0:
                    map[x,y] = 0
                    origin = (x,y)
                elif pix[x,y,0] == 255 and pix[x,y,1] == 0 and pix[x,y,2] == 0:
                    map[x,y] = 0
                    end = (x,y)
    return map, origin, end

def revertMap(map, origin, end):
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x,y] == 1:
                pix[x,y,:3] = 255
            elif map[x,y] == 2:
                pix[x,y,:3] = 125

    #Put start and end back in
    pix[origin] = [0,255,0,255]
    pix[end] = [255,0,0,255]

    return pix

def bfs(start, end):
    prev = solve(start)
    return reconstructPath(start, end, prev)

def toIndex(k):
    return k[0]*map.shape[1]+k[1] #Makes a unique index based on position on board

def solve(s):
    q = Queue()
    q.enqueue(s)

    visited = [False for _ in range(map.size)]
    visited[toIndex(s)] = True

    prev = [None for _ in range(map.size)]
    while len(q) > 0:
        x, y = q.dequeue()

        if y != 0 and map[(x, y-1)] == 0: #Left
            next = toIndex((x,y-1))
            if visited[next] == False:
                q.enqueue((x, y-1))
                visited[next] = True
                prev[next] = (x, y)
        if y != map.shape[1]-1 and map[(x, y+1)] == 0: #Right
            next = toIndex((x,y+1))
            if visited[next] == False:
                q.enqueue((x, y+1))
                visited[next] = True
                prev[next] = (x, y)
        if x != 0 and map[(x-1, y)] == 0: #Up
            next = toIndex((x-1,y))
            if visited[next] == False:
                q.enqueue((x-1, y))
                visited[next] = True
                prev[next] = (x, y)
        if x != map.shape[0]-1 and map[(x+1, y)] == 0: #Down
            next = toIndex((x+1,y))
            if visited[next] == False:
                q.enqueue((x+1, y))
                visited[next] = True
                prev[next] = (x, y)
    return prev

def reconstructPath(start, end, prev):
    path = []
    currentNode = prev[toIndex(end)]
    while currentNode != None:
        path.insert(0, currentNode) #Reverse the path as we started from end
        currentNode = prev[toIndex(currentNode)]

    #Check to make sure our path reaches the start (from the end)
    if len(path) > 0 and path[0] != start:
        path = None

    return path


pic = Image.open("pathfind.png")
pix = np.array(pic)
pic.close()

map, origin, end = createMap(pix) #Convert from 3d to 2d for easier management
path = bfs(origin, end) #Find path using bfs

if path != None: #Only make a new image if path exists
    for pos in path:
        if pos != None:
            map[pos] = 2

    #Length of path == Shortest Distance
    print("Path Length: {}".format(len(path)))

    pix = revertMap(map, origin, end) #Turn 2d back into 3d to be able to save as a png


    newPic = Image.fromarray(pix)
    newPic.save("pathfound.png", "PNG")
    newPic.close()
