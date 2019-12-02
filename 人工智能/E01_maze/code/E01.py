# -*- coding: utf-8 -*-


def bfs(maze_map, S, E, row, col):
    """利用广搜在迷宫图中寻找两点间最短路径

    :param maze_map: 二维列表，迷宫图
    :param S: [int, int] 起点坐标
    :param E: [int, int] 终点坐标
    :param row: int，迷宫图的行数
    :param col: int，迷宫图的列数
    :return: 有路则返回记录路线在各点的方向，否则返回None
    """
    move = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # 上右下左
    visited = [[0] * col for _ in range(row)]  # 记录点是否被访问过
    # visited = [[0] * col * row]
    visited[S[0]][S[1]] = 1                    # 标记起点
    directions = []                            # 走过的路线，在各点处的方向
    for r in range(row):
        a_row = [0] * col
        directions.append(a_row)

    nodes = [S]                                # BFS将要访问的点的队列

    while len(nodes) != 0:
        node = nodes[0]                        # 取第一个点
        # print(node)
        for i in range(1, 5):                  # 1，2，3，4分别代表上右下左
            x = node[0] + move[i-1][0]         # 探索临近的点
            y = node[1] + move[i-1][1]

            if x == E[0] and y == E[1]:        # 到达终点
                directions[x][y] = i
                return directions
            # 如果坐标合法且未被访问过且有路可走,
            # 这里python可以使用链式比较，为了不搞混还是使用C的写法
            if x >= 0 and y >= 0 and x < row and y < col \
                    and visited[x][y] == 0 and maze_map[x][y] == ' ':
                nodes.append([x, y])           # 将合理的点加入待访问队列
                visited[x][y] = 1              # 标记为已访问
                directions[x][y] = i           # 记录行走的方向
            # print(nodes)
        del (nodes[0])                         # 删除已访问过的点

    return None


filename = 'MazeData.txt'
maze = []
S = []
E = []
row = 0
col = 0
with open(filename, 'r', encoding='utf-8') as data:
    for line in data:
        line = line.strip()
        print(line)
        s_col = line.find('S')
        e_col = line.find('E')
        if s_col is not -1:
            S = [row, s_col]
            col = len(line)

        if e_col is not -1:
            E = [row, e_col]

        row += 1
        maze.append(list(line))

ans = bfs(maze, S, E, row, col)

if ans is None:
    print('No way to the end point.')
else:
    direction = ans[E[0]][E[1]]
    cur_x = E[0]
    cur_y = E[1]
    # for r in ans:
    #     print(r)
    # move = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # 上右下左
    path = [E]
    while direction != 0:
        if direction == 1:
            cur_x += 1

        if direction == 2:
            cur_y -= 1

        if direction == 3:
            cur_x -= 1

        if direction == 4:
            cur_y += 1

        path.append([cur_x, cur_y])
        direction = ans[cur_x][cur_y]
        maze[cur_x][cur_y] = '*'

    maze[S[0]][S[1]] = 'S'
    path = path[::-1]
    print('The path is: ', path)
    print('Total length of the path: ', len(path)-1)
    for l in maze:
        print(''.join(l))
