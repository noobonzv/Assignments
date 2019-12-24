import math
import numpy as np
from time import *


def load_data(filename):
    """
    加载训练和测试数据集，并做一些初步的处理，删除掉无关的属性
    :param filename: str
    :return: 数据集列表
    """
    with open(filename, 'r') as f:
        dataset = []
        for line in f.readlines()[:-1]:
            record = line.strip().split(', ')
            record[0] = int(record[0])
            record[2] = int(record[2])
            record[4] = int(record[4])
            record[10] = int(record[10])
            record[11] = int(record[11])
            record[12] = int(record[12])
            # 去除最后的点
            if record[-1][-1] == '.':
                record[-1] = record[-1][:-1].strip()
            dataset.append(record)
        return dataset


def get_miss_attributes(dataset):
    """
    返回数据集中有缺失值的属性，以及对应缺失次数
    :param dataset:
    :return: dict 键值是缺失属性的序号
    """
    miss = {}
    for record in dataset:
        for i in range(len(record)):
            if record[i] == '?':
                miss[i] = miss.get(i, 0) + 1
    return miss


def get_attributes_domain(dataset):
    """
    返回每种属性的取值范围
    :param dataset: 数据集
    :return: dict 每种属性的取值范围
    """
    num = len(dataset[0]) - 1
    attribute_domain = {}
    # 遍历属性，遍历数据集，记录所有取值情况
    for i in range(num):
        domain = set()
        for record in dataset:
            domain.add(record[i])
        attribute_domain[i] = domain
    return attribute_domain


def get_attributes_max_branch(dataset):
    """
    每个属性取值出现次数最多的取值，用于填充
    :param dataset:
    :return: dict 有缺失的属性的出现最频繁的值
    """
    # 首先找到哪些属性有缺失
    miss_attributes = get_miss_attributes(dataset)
    miss_attributes_max_branches = {}
    # 遍历有缺失值的属性, 统计找出有缺失值的属性取值最频繁的值，用于后面填充
    for i in miss_attributes.keys():
        count = {}
        for record in dataset:
            count[record[i]] = count.get(record[i], 0) + 1
        # 出现频率最高
        max_branch = max(count.items(), key=lambda x: x[1])
        miss_attributes_max_branches[i] = max_branch[0]
    return miss_attributes_max_branches

# miss_attributes_max_branches = get_attributes_max_branch(train_data)
# print(miss_attributes_max_branches)


def precondition(dataset):
    """
    预处理，将缺失值填充为该属性出现次数最多的取值
    :param dataset: 数据集，列表
    :return: 处理后的数据集 list， 有用属性序号列表
    """
    # 得到有缺失的属性，以及该属性出现次数最多的取值
    miss_attributes_max_branches = get_attributes_max_branch(dataset)
    # print(miss_attributes_max_branches)
    for record in dataset:
        for i in miss_attributes_max_branches.keys():
            if record[i] == '?':
                record[i] = miss_attributes_max_branches[i]
    return dataset


def get_freq(dataset):
    """
    统计各个属性各个取值在不同分类下出现的频数，对于连续型属性，返回训练集上的均值和方差
    :param dataset:
    :return: list, [ [{attr_value: n (第一类),...} {attr_value: n (第二类),...} ]， [{}{}], ...]
    """
    total_records_num = len(dataset[0])
    # [ [{attr_value: n (第一类),...} {attr_value: n (第二类),...} ]， [{},{}], ...]
    # 每个属性用两个字典记录，第一个是在第一类中计数，第二个是在第二类中计数
    freqs = [[{}, {}] for i in range(total_records_num)]
    for record in dataset:
        # 离散型属性，直接统计
        for i in [1, 3, 5, 6, 7, 8, 9, 13, 14]:
            value = record[i]
            # 第一类下计数
            if record[-1] == '<=50K':
                freqs[i][0][value] = freqs[i][0].get(value, 0) + 1
            # 第二类下计数
            else:
                freqs[i][1][value] = freqs[i][1].get(value, 0) + 1

    # 处理连续型属性
    continuous_index = [0, 2, 4, 10, 11, 12]
    # 先取出这些属性的取值，方便后面用np求均值和方差
    # 同样，每个属性用两个列表记录，第一个是在第一类中计数，第二个是在第二类中计数
    continuous_attr = [[[], []] for i in range(6)]
    for record in dataset:
        if record[-1] == '<=50K':
            for i in range(6):
                index = continuous_index[i]
                continuous_attr[i][0].append(record[index])
        else:
            for i in range(6):
                index = continuous_index[i]
                continuous_attr[i][1].append(record[index])

    # 计算连续型属性取值的均值和方差
    for i in range(6):
        freqs[continuous_index[i]][0]['mean'] = np.mean(continuous_attr[i][0])
        freqs[continuous_index[i]][0]['var'] = np.var(continuous_attr[i][0])
        freqs[continuous_index[i]][1]['mean'] = np.mean(continuous_attr[i][1])
        freqs[continuous_index[i]][1]['var'] = np.var(continuous_attr[i][1])

    # for freq in freqs:
    #     print('--------------------------')
    #     for k, v in freq[0].items():
    #         print(k,v)
    #     print('=========================')
    #     for k, v in freq[1].items():
    #         print(k, v)
    #     print('')
    # print(len(freqs))

    return freqs


def gaussian(x, u, var):
    """
    输入均值方差，得到高斯函数，用它当作概率密度函数计算变量为x时的概率
    :param x: float,取值
    :param u: float，均值
    :param var: float，方差
    :return: float，概率
    """
    y = np.exp(-(x - u) ** 2 / (2 * var)) / (math.sqrt(2 * math.pi * var))
    return y


def test(test_dataset, freqs):
    """
    在生成的决策树上测试，返回正确率
    :param test_dataset:
    :param probs:
    :return: 正确率
    """
    right = 0
    less_50 = freqs[-1][0]['<=50K']
    more_50 = freqs[-1][1]['>50K']
    py1 = less_50 / (less_50 + more_50)
    py2 = more_50 / (less_50 + more_50)
    for record in test_dataset:
        label = '<=50K'
        prob1 = py1
        prob2 = py2
        # 计算 P(xi|y）
        for i in range(len(test_dataset[0])-1):
            # 连续型属性
            if i in [0, 2, 4, 10, 11, 12]:
                m1 = freqs[i][0]['mean']
                v1 = freqs[i][0]['var']
                p1 = gaussian(record[i], m1, v1)
                prob1 = prob1 * p1

                m2 = freqs[i][1]['mean']
                v2 = freqs[i][1]['var']
                p2 = gaussian(record[i], m2, v2)
                prob2 = prob2 * p2
            # 离散型属性
            else:
                # 加1法处理，注意没出现的算一次，其他的每个取值增加1次
                p1 = (freqs[i][0].get(record[i], 0) + 1) / (less_50 + len(freqs[i][0].keys()))
                prob1 = prob1 * p1

                p2 = (freqs[i][1].get(record[i], 0) + 1) / (more_50 + len(freqs[i][1].keys()))
                prob2 = prob2 * p2
            # print('##', prob1, prob2)

        if prob2 > prob1:
            label = '>50K'
        if label == record[-1].strip():
            right += 1
    # print(right, len(test_dataset))
    return right/len(test_dataset)


if __name__ == '__main__':
    train_data = load_data('adult.data')
    test_data = load_data('adult.test')      # 含标签

    train_data = precondition(train_data)
    test_data = precondition(test_data)
    attributes_domain = get_attributes_domain(train_data)
    frequencies = get_freq(train_data)
    t2 = time()
    accuracy_train = test(train_data, frequencies)
    accuracy_test = test(test_data, frequencies)
    # print(test_data[0][-1] == '<=50K', test_data[2][-1] == '>50K')
    t3 = time()
    print('Accuracy on training data set: {}%'.format(accuracy_train*100))
    print('Accuracy on testing data set: {}%'.format(accuracy_test*100))
    print('Testing time cost: {:.4}s'.format(t3 - t2))

