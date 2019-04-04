from Queue import PriorityQueue

RIGHT = 'r'
LEFT = 'l'
UP = 'u'
DOWN = 'd'
ttarget = RIGHT

def dis(i, j):
    return abs(i['x']-j['x'])+abs(i['y']-j['y'])

class nod():
    def __init__(self,h,g,x,y,target):
        self.h = h
        self.g = g
        self.f = h + g
        self.x = x
        self.y = y
        self.target = target
    def geth(self):
        return self.h
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def gett(self):
        return self.target
    def __lt__(self,other):
        if self.f == other.f:
            if self.target == ttarget:
                return True
            elif other.target == ttarget:
                return False
            else:
                return True
        return self.f<other.f
    def __str__(self):
        return 'h:' + str(self.h)+ ' g:' + str(self.g)

def shortest_path_to(x1, y1, x2, y2, mapjz,width,height):
    # solver_init()

    mapai = [['n'] * 50 for i in range(50)]
    mapvisit = [['n'] * 50 for i in range(50)]
    queue = PriorityQueue()
    visited = set()

    s = abs(x2 - x1) + abs(y2 - y1)
    first_nod = nod(0, s, x1, y1, 'u')
    queue.put(first_nod)
    while not queue.empty():
        cnod = queue.get()
        pos = [cnod.getx(), cnod.gety()]
        if (pos[0], pos[1]) in visited:
            continue
        mapvisit[pos[0]][pos[1]] = cnod.gett()
        ttarget = cnod.gett()
        visited.add((pos[0], pos[1]))
        cstep = cnod.geth()
        if pos[0] == x2 and pos[1] == y2:
            x = x2
            y = y2
            while True:
                if x == x1 and y == y1:
                    break
                if mapvisit[x][y] == RIGHT:
                    y += 1
                    mapai[x][y] = LEFT
                elif mapvisit[x][y] == LEFT:
                    y -= 1
                    mapai[x][y] = RIGHT
                elif mapvisit[x][y] == DOWN:
                    x += 1
                    mapai[x][y] = UP
                elif mapvisit[x][y] == UP:
                    x -= 1
                    mapai[x][y] = DOWN
            return (True, mapai)
        else:
            if mapjz[pos[0] + 1][pos[1]] != 1 and (pos[0] + 1, pos[1]) not in visited:
                if pos[0] + 1 >= 0 and pos[0] + 1 <= width and pos[1] >= 0 and pos[1] <= height :
                    h = cstep + 1
                    g = abs(x2 - (pos[0] + 1)) + abs(y2 - (pos[1]))
                    nnod = nod(h, g, pos[0] + 1, pos[1], UP)
                    queue.put(nnod)

            if mapjz[pos[0]][pos[1] + 1] != 1 and (pos[0], pos[1] + 1) not in visited:
                if pos[0] >= 0 and pos[0] <= width and pos[1] + 1 >= 0 and pos[1] + 1 <= height :
                    h = cstep + 1
                    g = abs(x2 - (pos[0])) + abs(y2 - (pos[1] + 1))
                    nnod = nod(h, g, pos[0], pos[1] + 1, LEFT)
                    queue.put(nnod)

            if mapjz[pos[0] - 1][pos[1]] != 1 and (pos[0] - 1, pos[1]) not in visited:
                if pos[0] - 1 >= 0 and pos[0] - 1 <= width  and pos[1] >= 0 and pos[1] <= height :
                    h = cstep + 1
                    g = abs(x2 - (pos[0] - 1)) + abs(y2 - (pos[1]))
                    nnod = nod(h, g, pos[0] - 1, pos[1], DOWN)
                    queue.put(nnod)

            if mapjz[pos[0]][pos[1] - 1] != 1 and (pos[0], pos[1] - 1) not in visited:
                if pos[0] >= 0 and pos[0] <= width  and pos[1] - 1 >= 0 and pos[1] - 1 <= height :
                    h = cstep + 1
                    g = abs(x2 - (pos[0])) + abs(y2 - (pos[1] - 1))
                    nnod = nod(h, g, pos[0], pos[1] - 1, RIGHT)
                    queue.put(nnod)
    return (False, mapai)


def mybfs(data):
    height = data['board']['height']
    width = data['board']['width']
    mapjz = [[0] * 50 for i in range(50)]
    apple = data['board']['food']
    head = data['you']['body'][0]
    tail = data['you']['body'][-1]
    virtualmapjz = [[0] * 50 for i in range(50)]

    for var in data['board']['snakes']:
        for i in var['body']:
            mapjz[int(i['x'])][int(i['y'])] = 1

    for i in range(len(apple)):
        for j in range(i+1,len(apple)):
            if dis(apple[i],head) > dis(apple[j],head):
                t = apple[i]
                apple[i] = apple[j]
                apple[j] = t

    for var in apple:
        t = shortest_path_to(head['x'],head['y'],var['x'],var['y'],mapjz,width,height)
        if t[0]:
            mapai = t[1]
            if mapai[head['x']][head['y']] == UP:
                return 'left'
            if mapai[head['x']][head['y']] == DOWN:
                return 'right'
            if mapai[head['x']][head['y']] == LEFT:
                return 'up'
            if mapai[head['x']][head['y']] == RIGHT:
                return 'down'

    return 'up'