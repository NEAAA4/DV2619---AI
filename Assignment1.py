"""Linnea Conradsson Sjöberg - LICO22"""

import matplotlib.pyplot as plt
import numpy as np
from collections import deque


def graph(matrix, path, algorithm):
    plt.ion()
    maze = np.array(matrix)

    plt.figure(figsize=(7, 5))
    x, y = np.where(maze == 0)

    colors = ['black'] * len(x)

    start = (0, 1)
    end = (9, 18)

    for index, (i, j) in enumerate(zip(x, y)):
        if (i, j) == end:
            colors[index] = 'blue'
        elif (i, j) == start:
            colors[index] = 'red'

        if maze[i][j] == 0:
            if j < len(maze[i]) - 1 and maze[i][j + 1] == 0:
                plt.plot([j, j + 1], [-i, -i], color='black', lw=2)

            if i < len(maze) - 1 and maze[i + 1][j] == 0:
                plt.plot([j, j], [-i - 1, -i], color='black', lw=2)

    for (a, b) in path:
        for index, (i, j) in enumerate(zip(x, y)):
            if (a, b) == (i, j):
                colors[index] = 'magenta'
                plt.scatter(y, -x, color=colors, s=100)
                plt.title(algorithm)
                plt.pause(0.3)

    plt.xticks([])
    plt.yticks([])
    plt.show()
    plt.ioff()
    plt.show()


def breadthfirst(matrix, start, end):
    rows, columns = len(matrix), len(matrix[0])
    showed = [[False] * columns for _ in range(rows)]

    steps = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    que = deque([(start, [start])])
    x, y = start
    showed[x][y] = True

    while que:
        new, path = que.popleft()
        x, y = new

        if new == end:
            graph(matrix, path, 'Breadth First Search')
            print(len(path))
            return path

        for dx, dy in steps:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < columns and not showed[nx][ny] and matrix[nx][ny] == 0:
                que.append(((nx, ny), path + [(nx, ny)]))
                showed[nx][ny] = True

    return "No Path Exists"


def depthfirst(matrix, start, end):

    rows, columns = len(matrix), len(matrix[0])
    stack = [(start, [start])] 
    showed = [[False] * columns for _ in range(rows)]

    while stack:
        node, path = stack.pop() 
        x, y = node
        showed[x][y] = True

        if node == end:
            graph(matrix, path, "Depth First Search")
            print(len(path))
            return path

        steps = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in steps:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < columns and not showed[nx][ny] and matrix[nx][ny] == 0:
                stack.append(((nx, ny), path + [(nx, ny)]))

    return "No Path Exists"


def astar(matrix, start, end):
    olist = []
    clist = []
    g = {}
    h = {}
    f = {}

    olist.append(start)
    g[start] = 0
    h[start] = np.sqrt((end[0] - start[0])**2) + ((end[1] - start[1])**2)
    f[start] = g[start] + h[start]

    parent = {}
    parent[start] = None

    while len(olist) > 0:
        node = olist[0]
        for i in olist:
            if f[i] < f[node]:
                i = node

        if node == end:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
                path = path[::-1]

            print(len(path))
            graph(matrix, path, 'A* Search')
            return path

        olist.remove(node)
        clist.append(node)

        steps = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for walk in steps:
            position = (node[0] + walk[0], node[1] + walk[1])

            if position[0] > (len(matrix) - 1) or position[0] < 0 or position[1] > (len(matrix[0]) - 1) or position[1] < 0:
                continue
            if matrix[position[0]][position[1]] != 0:
                continue
            if position in clist:
                continue

            nodeG = (g[node] + 1)
            h[position] = np.sqrt((position[0] - end[0])**2) + ((position[1] - end[1])**2)
            f[position] = nodeG + h[position]

            if position not in olist:
                olist.append(position)
                parent[position] = node
                g[position] = nodeG

            elif nodeG < g[position]:
                parent[position] = node
                g[position] = nodeG
                f[position] = g[position] + h[position]

    return "No Path Exists"


def main():
    matrix = [
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0],
        [1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,1,0],
        [1,1,1,1,1,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0],
        [1,1,1,1,1,0,1,1,1,1,1,1,0,1,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1],
        [1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1]]

    start = (0, 1)
    end = (9, 18)

    breadthfirst(matrix, start, end)
    depthfirst(matrix, start, end)
    astar(matrix, start, end)


if __name__ == "__main__":
    main()
