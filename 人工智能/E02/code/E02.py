import sys
import copy


def h(node):
    """启发函数，估计到目标状态的距离

    :param node: 4x4二维列表，表示一种状态
    :return: 与目标状态的距离，采用曼哈顿距离
    """
    cost = 0
    # 遍历每个格子，计算与目标状态的距离
    for i in range(0, 16):
        cur_row = int(i / 4)
        cur_col = int(i % 4)
        tile = node[cur_row][cur_col]       # 格子里面的值，[0,15]
        # 根据格子里面的值计算在目标状态的坐标
        if tile == 0:
            goal_row = 3
            goal_col = 3
        else:
            goal_row = int((tile-1) / 4)
            goal_col = int((tile-1) % 4)
        # 计算距离
        dis_x = abs(cur_row - goal_row)
        dis_y = abs(cur_col - goal_col)
        cost += dis_x
        cost += dis_y
        # print(tile, goal_row,goal_col,cost)
    return cost
# test = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
# print(h(test))


def is_goal(node):
    """判断是否为目标状态

    :param node: 4x4二维列表，表示一种状态
    :return: 达到目标状态返回True，否则返回False
    """
    for i in range(4):
        for j in range(4):
            if node[i][j] != goal[i][j]:
                return False
    return True
# test = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
# print(is_goal(test))


def successors(node):
    """计算此状态可能的下一状态

    :param node: 4x4二维列表，表示一种状态
    :return: 返回可能达到的状态的列表，三维列表
    """
    row, col = 0, 0
    # 找到空白块的位置
    for i in range(4):
        for j in range(4):
            if node[i][j] == 0:
                row, col = i, j
    # 上右下左
    moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    succs = []
    for move in moves:
        s_row = row + move[0]
        s_col = col + move[1]
        if 0 <= s_row < 4 and 0 <= s_col < 4:
            temp_node = copy.deepcopy(node)
            temp_node[row][col], temp_node[s_row][s_col] = temp_node[s_row][s_col], temp_node[row][col]
            succs.append(temp_node)

    return sorted(succs, key=lambda x: h(x))
# test = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
# test = [[1, 2, 3, 4], [5, 0, 7, 8], [9, 10, 11, 12], [13, 14, 15, 6]]
# print(successors(test))


def search(path, g, bound):
    """向下探索路径

    :param path: 已走过的路径
    :param g: 走过的路径
    :param bound: 总路线长度估计值的下限
    :return: 如果到达目标状态就返回路径和花费，没有找到则继续探索其后继状态
    """
    node = path[-1]
    f = g + h(node)
    if f > bound:
        return f
    if is_goal(node):
        return (path, f)
    min_cost = sys.maxsize
    for succ in successors(node):
        if succ not in path:
            path.append(succ)
            t = search(path, g+1, bound)
            if type(t) == tuple:
                return t
            if t < min_cost:
                min_cost = t
            del(path[-1])
    return min_cost


def ida_star(root):
    """使用IDA*算法解决15puzzle问题

    :param root:初始状态，4x4二维列表
    :return:达到目标状态的每一步路径
    """
    bound = h(root)
    path = [root]

    while True:
        t = search(path, 0, bound)
        if type(t) == tuple:
            return t
        if t > 60:
            return ([], bound)
        bound = t


def is_possible(root):
    """用逆序对判断是否有解

    :param root: 初始状态，二维列表
    :return: 如果有解返回True，否则返回False
    """
    temp = sum(root, [])    # 转化为一维列表，方便判断
    n = 0
    # print(temp)
    for i in range(len(temp)):
        if temp[i] == 0:
            cur_row = int(i / 4)
            dis_x = abs(cur_row - 3)
            n += dis_x
            continue
        for j in range(i):
            if temp[j] > temp[i]:
                n += 1
    # 逆序数 + 空白格到目标状态的行数
    if n % 2 == 0:
        return True
    else:
        return False


if __name__=="__main__":
    # 目标状态
    goal = []
    tile = 1
    for i in range(4):
        temp = []
        for j in range(4):
            temp.append(tile)
            tile += 1
        goal.append(temp)
        # print(temp)
    goal[3][3] = 0
    # print(goal)
    # root = [[5, 1, 3, 4], [2, 7, 8, 12], [9, 6, 11, 15], [0, 13, 10, 14]] # 15
    # root = [[4, 11, 10, 1], [13, 14, 8, 2], [7, 5, 12, 6], [9, 3, 15, 0]] # 54
    # root = [[1, 2, 3, 4], [12, 9, 14, 11], [7, 8, 6, 15], [0, 5, 13, 10]] # 31
    # root = [[1, 3, 2, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]] # 无解
    # root = [[6, 10, 3, 15], [14, 8, 0, 11], [1, 9, 7, 2], [5, 13, 12, 4]] # 41
    root = [[6, 10, 3, 15], [14, 8, 7, 11], [5, 1, 0, 2], [13, 12, 9, 4]] # 48
    # root = [[14, 10 ,6, 0], [4, 9, 1, 8], [2, 3, 5, 11], [12, 13, 7, 15]] # 49

    for row in root:
        print(row)
    if is_possible(root):
        (path, bound) = ida_star(root)
        move = []
        for node in path:
            for i in range(4):
                for j in range(4):
                    if node[i][j] == 0:
                        move.append([i, j])
        del (move[0])

        print('The solution need: ', len(move), 'moves.')
        print('The path is:')
        for i in range(len(move)):
            x = move[i][0]
            y = move[i][1]
            print(path[i][x][y], end=' ')

    else:
        print("Impossible!!")



