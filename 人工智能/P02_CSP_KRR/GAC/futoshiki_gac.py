# -*- coding: UTF-8 -*-
import time
from copy import deepcopy
board_size = 0


def read_data(filename):
    """根据文件名读取board

    :param filename:
    :return:
    """
    board = []
    # 限制分为大于，小于两部分存，为了后面检查限制的时候更方便
    comparison_constraint = []
    with open(filename) as f:
        global board_size
        board_size = int(f.readline())
        for i in range(board_size):
            line = f.readline()
            row = [int(num) for num in line.split(' ')]
            board.append(row)
        # 读取比较限制
        lines = f.readlines()
        for line in lines:
            constraint = [int(num) for num in line.split(' ')]
            comparison_constraint.append(constraint)
    # print(comparison_constraint)
    return board, comparison_constraint


def initial(board):
    """根据读出的board信息，初始化值域和赋值情况

    :param board: 二维列表
    :return: 初始化值域和赋值情况
    """
    domain = []
    assigned = []
    for i in range(board_size):
        row = []
        for j in range(board_size):
            if board[i][j] != 0:
                row.append(True)
            else:
                row.append(False)
        assigned.append(row)
    # 初始化值域
    for row in board:
        domain_each_row = []
        for grid in row:
            # 未赋值
            if grid == 0:
                grid_domain = [v for v in range(1, board_size + 1)]
                domain_each_row.append(grid_domain)
            else:
                domain_each_row.append([grid])
        domain.append(domain_each_row)
    return (domain, assigned)


def print_board(board):
    for row in board:
        for i in row:
            print(i, end=' ')
        print('')


def MRV(domain, assigned):
    """寻找值域最小的格子，返回其坐标，若都已赋值则返回 [-1,-1]

    :param domain: 所有格子的值域
    :param assigned: 所有格子的赋值情况
    :return: 返回值域最小的格子的坐标，若都已赋值则返回 [-1,-1]
    """
    least_domain_len = 99999
    x = -1
    y = -1
    for r in range(board_size):
        for c in range(board_size):
            domain_len = len(domain[r][c])
            if not assigned[r][c] and domain_len < least_domain_len:
                x = r
                y = c
                least_domain_len = domain_len
    return (x, y)


def compare_check(domain, comparison, x, y, cur_value):
    """对比较限制的检查

    :param domain: 格子值域，每个格子一个列表，board由一个二维列表构成，故为三维列表
    :param comparison: 比较限制列表，二维列表，每一行表示一个大小限制
    :param x: 当前坐标
    :param y: 当前坐标
    :param cur_value: 当前取值
    :return: 限制可满足则返回True，否则False
    """
    n = 0
    satisfied = 0
    # 遍历限制，有多少限制就要满足多少，否则为不满足
    for constraint in comparison:
        if x == constraint[0] and y == constraint[1]:
            n += 1
            for value in domain[constraint[2]][constraint[3]]:
                if cur_value < value:
                    satisfied += 1
                    break
        elif x == constraint[2] and y == constraint[3]:
            n += 1
            for value in domain[constraint[0]][constraint[1]]:
                if cur_value > value:
                    satisfied += 1
                    break
    return n == satisfied


def recursive_check(domain, comparison, row_or_col, cur_index, num_checked, visited):
    """主要为了检查all-diff，也就是该行该列是否能各不相同，因为board_size会变，才写成递归

    :param domain: 格子值域，每个格子一个列表，board由一个二维列表构成，故为三维列表
    :param comparison: 比较限制列表，二维列表，每一行表示一个大小限制
    :param row_or_col: 0或1，指明正在做行检查还是列检查，0表示行检查
    :param cur_index: 如果当前在做行检查，作为行坐标，否则为列坐标，检查时，该值不变，另一个坐标会在 0~board_size-1变化
    :param num_checked: 该行或该列已检查过的坐标数
    :param visited: 该行该列哪些值已经取了，列表
    :return: 所有条件都满足时返回 True
    """
    if num_checked == board_size:
        return True
    if row_or_col == 0:
        x = cur_index
        y = num_checked
    else:
        x = num_checked
        y = cur_index
    # 检查该行或该列第num_checked格子
    for value in domain[x][y]:
        # 该行或列已经有这个值了，或者未通过大小限制的检查，则继续检查下一个值
        compare_satisfied = compare_check(domain, comparison, x, y, value)
        if visited[value] or not compare_satisfied:
            continue
        # 如果通过了大小检查，也保证了该行或列没有相同的值
        # 则标记该值已有，继续赋值下一个
        visited[value] = True
        if recursive_check(domain, comparison, row_or_col, cur_index, num_checked + 1, visited):
            return True
        visited[value] = False
    # 如果所有值都不行，则返回上一层，重新赋值，重新检查
    return False


def constraints_check(domain, comparison, row_or_col, cur_index, x, y, value):
    """调用递归检查，做all_diff检查和比较限制检查

    :param domain: 格子值域，每个格子一个列表，board由一个二维列表构成，故为三维列表
    :param comparison: 比较限制列表，二维列表，每一行表示一个大小限制
    :param row_or_col: 0或1，指明正在做行检查还是列检查，0表示行检查
    :param cur_index: 如果当前在做行检查，作为行坐标，否则为列坐标，检查时，该值不变，另一个坐标会在 0~board_size-1变化
    :param x: 坐标
    :param y: 坐标
    :param value: 当前格子的取值
    :return: 如果能找到一些赋值，满足两方面的限制就返回True
    """
    visited = [False for i in range(board_size+1)]
    domain_copy = deepcopy(domain[x][y])
    domain[x][y] = [value]
    can_be_satisfied = recursive_check(domain, comparison, row_or_col, cur_index, 0, visited)
    domain[x][y] = deepcopy(domain_copy)
    return can_be_satisfied


def GAC_Enforce(domain, comparison, x, y):
    """检查限制条件，并去掉不合适的值

    :param domain: 格子值域，每个格子一个列表，board由一个二维列表构成，故为三维列表
    :param comparison: 比较限制列表，二维列表，每一行表示一个大小限制
    :param x: 坐标
    :param y: 坐标
    :return: 某个坐标值域被删空了就返回True，表示发生了DWO
    """
    GACQueue = []
    # 0表示行检查，1表示列检查
    # 大小比较每次都会做，所以没有单独再入队。如果反之，每次是大小限制入队的话，会很慢！！！
    # 因为一个格子的坐标发生了变化，会影响行列，所以都是成对出现的
    # 初始入队 (0, x)表示对x行进行行检查，(1, y)表示对y列进行列检查
    GACQueue.append((0, x))
    GACQueue.append((1, y))
    while GACQueue:
        row_or_col_check, cur_index = GACQueue[0]
        del(GACQueue[0])
        # 检查该行或该列的所有格子

        for other_index in range(board_size):
            if row_or_col_check == 0:
                x = cur_index
                y = other_index
            else:
                x = other_index
                y = cur_index
            cur_domain = domain[x][y]
            for value in cur_domain:
                # 如果不能满足条件则去掉该值，这里会做all-diff检查和大小限制检查
                if not constraints_check(domain, comparison, row_or_col_check, cur_index, x, y, value):
                    domain[x][y] = [v for v in domain[x][y] if v != value]
                    # 如果值域为空则，返回True，表示发生了 DWO
                    if not domain[x][y]:
                        return True
                    # 如果值域不为空，且相关限制不在队列中则将相关限制加入队列
                    # r=1,则变化的是[O,C]处, 有 (0,O), (1,C)入队
                    # r=0,则变化的是[C,O]处, 有 (0,C), (1,O)入队
                    else:
                        if (row_or_col_check, cur_index) not in GACQueue:
                            GACQueue.append((row_or_col_check, cur_index))
                        if (1 - row_or_col_check, other_index) not in GACQueue:
                            GACQueue.append((1 - row_or_col_check, other_index))
    return False


def GAC(domain, comparison, assigned, board):
    """GAC算法，赋值，调用GAC_Enforce做检查去值，每次调用代表赋值一个格子

    :param domain: 格子值域，每个格子一个列表，board由一个二维列表构成，故为三维列表
    :param comparison: 比较限制列表，二维列表，每一行表示一个大小限制
    :param assigned: 所有格子是否赋值的情况，二维bool列表
    :param board: 棋盘，二维列表
    :return: 找到解就返回True，否则返回False
    """
    # 找值域最小的赋值
    (x, y) = MRV(domain, assigned)
    # 若全部都完成赋值
    if (x, y) == (-1, -1):
        return True

    assigned[x][y] = True
    values = domain[x][y]
    # 暂存值域
    temp_domain = deepcopy(domain)
    for value in values:
        board[x][y] = value
        # 赋值，也就去掉其他的值
        domain[x][y] = [value]
        # 如果没有 DWO
        if not GAC_Enforce(domain, comparison, x, y):
            find_solution = GAC(domain, comparison, assigned, board)
            if find_solution:
                return True
        # 恢复值域
        domain = deepcopy(temp_domain)
    assigned[x][y] = False
    return False


def run_test(filename):
    board, comparison = read_data(filename)
    print_board(board)
    print("-----------------------")
    domain, assigned = initial(board)
    begin = time.time()
    GAC(domain, comparison, assigned, board)
    end = time.time()
    print_board(board)
    print('Time cost:', end - begin, 's')


if __name__ == '__main__':
    run_test('4.txt')
    print('\n')
    run_test('5.txt')
    print('\n')
    run_test('6.txt')
    print('\n')
    run_test('7.txt')
    print('\n')
    run_test('8.txt')

