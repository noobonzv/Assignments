import math
from time import *


class Node(object):
    """ 决策树的节点 """
    def __init__(self, label=None, attribute=None, branches=None):
        self.attribute = attribute      # 当前节点划分的属性标签
        self.label = label              # 保存的是针对当前分支的类别划分结果，叶节点的该属性才重要
        self.branches = branches        # 分支的字典


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
            record[4] = int(record[4])
            record[10] = int(record[10])
            record[11] = int(record[11])
            record[12] = int(record[12])
            # 去除最后的点
            if record[-1][-1] == '.':
                record[-1] = record[-1][:-1]
            # 删除部分属性，删除后会前移
            del(record[2])
            del(record[2])
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
    # for data in train_data:
    #     print(data)
    # print(miss)
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
    预处理，划分连续属性，以及将缺失值填充为该属性出现次数最多的取值
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

    for record in dataset:
        # 年龄划分成7类
        if record[0] <= 20:
            record[0] = 1
        if 20 < record[0] <= 24:
            record[0] = 2
        if 24 < record[0] <= 34:
            record[0] = 3
        if 34 < record[0] <= 44:
            record[0] = 4
        if 44 < record[0] <= 54:
            record[0] = 5
        if 54 < record[0] <= 64:
            record[0] = 6
        if record[0] > 64:
            record[0] = 7

        # 关于资本的一些属性，分为2类
        if record[8] != 0:
            record[8] = 1

        if record[9] != 0:
            record[9] = 1

        # 一周工作时长，分3类
        if record[10] <= 36:
            record[10] = 1
        if 36 < record[10] <= 72:
            record[10] = 2
        if record[10] > 72:
            record[10] = 3

        if record[-1] == '<=50K':
            record[-1] = 0
        else:
            record[-1] = 1
    # 顺便返回有用属性的顺序列表，int
    attrs = []
    for i in range(len(dataset[0])-1):
        attrs.append(i)
    # for data in dataset:
    #     print(data)
    return dataset, attrs


def cal_InforEntropy(dataset):
    """
    计算当前子集的信息熵值
    :param dataset: 最后一列为标签值，其他为属性值
    :return: 返回信息熵的结果
    """
    total = len(dataset)
    label_counts = {}           # 统计各个label的数量，考虑可以用于多分类
    for record in dataset:
        label = record[-1]
        label_counts[label] = label_counts.get(label, 0) + 1

    InforEntropy = 0.0
    for item in label_counts.items():
        prob = float(item[1]) / total
        InforEntropy -= prob * math.log(prob, 2)
    # print(InforEntropy)
    return InforEntropy


def split_dataset(dataset, attribute, value):
    """
    根据选定的属性划分数据集
    :param dataSet:
    :param attribute: 选定属性的序号
    :param value: 该属性的取值
    :return: 在该属性上取该值的子集
    """
    # 遍历数据集，只要在该属性上取该值的数据，就取出来
    branch = []
    for record in dataset:
        if record[attribute] == value:
            branch.append(record)
    return branch


def select_best_attribute(dataset, attributes_domain, remaining_attributes):
    """
    计算信息增益，选出信息增益最大的属性，返回用于划分的属性序号
    :param dataset:
    :param attributes_domain: 每种属性的取值范围
    :param remaining_attributes: 还未用于划分的属性集
    :return: 返回用于划分的属性序号
    """
    total = len(dataset)                        # 总的数据条数
    rootEntropy = cal_InforEntropy(dataset)     # 根节点信息熵
    InforGain_list = []
    for attribute in remaining_attributes:
        InforEntropy = 0.0                      # 计算按该属性划分的信息熵
        for value in attributes_domain[attribute]:
            branch = split_dataset(dataset, attribute, value)
            # 该属性取值的数据集占总数的比例
            prob = len(branch) / total
            InforEntropy += prob * cal_InforEntropy(branch)
        InforGain_list.append((rootEntropy - InforEntropy, attribute))
    max_IG = max(InforGain_list, key=lambda IG: IG[0])
    return max_IG[1]


def build_tree(dataset, parent_label, remaining_attributes, attributes_domain):
    """
    递归建立决策树
    :param dataset:
    :param parent_label: 父节点label
    :param remaining_attributes: 还未用于划分的属性集
    :param attributes_domain: 每种属性的取值范围
    :return: 决策树节点
    """
    labels = [record[-1] for record in dataset]
    # 该分支无数据，为叶节点
    if len(dataset) < 5:
        return Node(label=parent_label, attribute=None, branches=None)
    # 样本全属于同一类
    if labels.count(labels[0]) == len(labels):
        return Node(label=labels[0], attribute=None, branches=None)
    # 全部属性都分完了，叶节点，其分类为其中样本数最多的类
    if len(remaining_attributes) == 0:
        # 出现频率最高，list.count 函数对象
        return Node(label=max(labels, key=labels.count), attribute=None, branches=None)
    # D中样本在剩余的属性集A上取值相同
    diff = False
    for attr in remaining_attributes:
        for record in dataset:
            if record[attr] != dataset[0][attr]:
                diff = True
                break
        if diff:
            break
    if not diff:
        return Node(label=max(labels, key=labels.count), attribute=None, branches=None)

    # 找到信息增益最大的属性，并准备用它来划分数据集，同时将该属性标记未已使用过
    best_attribute = select_best_attribute(dataset, attributes_domain, remaining_attributes)
    remaining_attributes.remove(best_attribute)
    branches = {}
    parent_label = max(labels, key=labels.count)
    # 把该属性每一个取值对应的数据集子集拿出来，递归建立子树，并记录到该节点的branches中
    for value in attributes_domain[best_attribute]:
        branch = split_dataset(dataset, best_attribute, value)
        branches[value] = build_tree(branch, parent_label, remaining_attributes[:], attributes_domain)

    return Node(attribute=best_attribute, label=parent_label, branches=branches)


def test(test_dataset, root):
    """
    在生成的决策树上测试，返回正确率
    :param test_dataset:
    :param root: 之前生成的决策树根节点
    :return: 正确率
    """
    right = 0
    for record in test_dataset:
        cur = root
        # 只要有分支就不是叶节点
        while cur.branches:
            # 流向 该条数据 在 该节点的属性 的取值 对应的分支
            cur = cur.branches[record[cur.attribute]]
        if cur.label == record[-1]:
            right += 1
    return right/len(test_dataset)


if __name__ == '__main__':
    train_data = load_data('adult.data')
    test_data = load_data('adult.test')      # 含标签

    train_data, attributes = precondition(train_data)
    test_data, a = precondition(test_data)
    attributes_domain = get_attributes_domain(train_data)
    # print(attributes)
    t1 = time()
    # 初始标签其实无所谓，此外，属性集上一开始所有属性都未用过
    root = build_tree(train_data, -1, attributes, attributes_domain)
    t2 = time()
    accuracy_train = test(train_data, root)
    accuracy_test = test(test_data, root)
    t3 = time()
    print('Accuracy on training data set: {:.4}%'.format(accuracy_train*100))
    print('Accuracy on testing data set: {:.4}%'.format(accuracy_test*100))
    print('Building decision tree time cost: {:.4}s'.format(t2 - t1))
    print('Testing time cost: {:.4}s'.format(t3 - t2))

