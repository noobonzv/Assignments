# coding=utf-8
import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# sigmoid的一阶导数
def sigmoid_prime(x):
    return sigmoid(x) * (1-sigmoid(x))


def onehot_encode(num, len):
    res = [0] * len
    res[num] = 1
    return res


class NeuralNetwork(object):
    def __init__(self, input_dim, hidden_node_num, output_dim):
        self.lr = 0.01                                        # 学习率
        self.input_dim = input_dim
        self.hidden_node_num = hidden_node_num
        self.output_dim = output_dim
        # 随机初始化
        self.w_ih = np.random.randn(input_dim, hidden_node_num) * 0.01
        self.b_ih = np.random.randn(hidden_node_num) * 0.01
        self.w_ho = np.random.randn(hidden_node_num, output_dim) * 0.01
        self.b_ho = np.random.randn(output_dim) * 0.01
        # 以下只是为了规范，在init()里面声明而已，初始值没有意义
        self.net_ih = np.zeros((hidden_node_num, 1))
        self.h_o = np.zeros((hidden_node_num, 1))
        self.net_ho = np.zeros((output_dim, 1))
        self.output = np.zeros((output_dim, 1))
        self.sensitivity_ho = np.zeros((output_dim, 1))
        self.x = np.zeros((input_dim, 1))

    # ================================================ 关键代码部分
    # 前向传播
    def forward(self, x, y):
        self.x = x
        self.net_ih = np.dot(x, self.w_ih) + self.b_ih               # 隐藏层wx+b 一维向量相加都是对应元素相加
        self.h_o = sigmoid(self.net_ih)                              # 激活
        self.net_ho = np.dot(self.h_o, self.w_ho) + self.b_ho        # 输出层wx+b
        self.output = sigmoid(self.net_ho)                           # 激活
        loss = np.sum((self.output - y) * (self.output - y)) / 2
        self.sensitivity_ho = (self.output - y) * sigmoid_prime(self.output)    # 灵敏度，会用到所以保存
        return loss, self.output                                     # 方便预测

    # 反向传播
    def backward(self):
        # 10x3  =  10x1 dot 1x3      一维向量只会做内积，所以reshape为矩阵
        delta_w_ho = np.dot(self.h_o.reshape(self.hidden_node_num, 1),
                            self.sensitivity_ho.reshape(1, self.output_dim))
        delta_b_ho = self.sensitivity_ho                             # 偏置的输入为1
        sensitivity_ih = np.dot(self.sensitivity_ho, self.w_ho.T) * sigmoid_prime(self.net_ih)
        # 36x10 = 36x1 dot 1x10
        delta_w_ih = np.dot(self.x.reshape(self.input_dim, 1),
                            sensitivity_ih.reshape(1, self.hidden_node_num))
        delta_b_ih = sensitivity_ih                                  # 偏置的输入为1

        # 更新参数
        self.w_ho -= self.lr * delta_w_ho
        self.b_ho -= self.lr * delta_b_ho
        self.w_ih -= self.lr * delta_w_ih
        self.b_ih -= self.lr * delta_b_ih

        # p = np.random.random()
        # if p > 0.8:
        #     self.lr = self.lr * 0.9
    # ================================================


def read_data(filename):
    """
    读取数据，并将分类标签放在最后一列
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        data = f.readlines()
        dataset = []
        output_index = data[0].split(',').index('outcome')
        for row in data[1:]:
            row = row.split(',')
            row = list(map(float, row))
            outcome = int(row[output_index])
            row = row[:output_index] + row[output_index+1:]
            row.append(outcome)
            dataset.append(row)
        # print('============================')
        # for d in dataset[0]:
        #     print(d)
        return dataset


def train(training_data, epoch, nn):
    for i in range(epoch):
        for data in training_data:
            x = np.array(data[:-1])
            y = onehot_encode(data[-1]-1, 3)
            y = np.array(y)
            loss, _ = nn.forward(x, y)
            nn.backward()
        print('Epoch {} Loss: {}'.format(i+1, loss))
    return nn


def test(testing_data, nn):
    """
    依次取数据喂入网络，得到输出结果与真正的标签对比
    :param testing_data:
    :param nn: 训练好的网络
    :return: 无
    """
    n = 0
    predictions = []
    for data in testing_data:
        x = np.array(data[:-1])
        y = [0, 0, 0]
        _, prediction = nn.forward(x, y)
        label = np.argmax(prediction, axis=0) + 1
        predictions.append(label)
        if label == data[-1]:
            n += 1
    print('Accuracy on testing dataset: {:.4}%'.format(100*n/len(testing_data)))
    print('Predictions:', predictions)


def feature_scaling(dataset):
    """
    对属性进行归一化处理
    :param dataset: 数据集
    :return: 归一化后的数据集
    """
    feature_num = len(dataset[0]) - 1
    maxs = [float('-inf')] * feature_num
    mins = [float('inf')] * feature_num
    res = []
    for data in dataset:
        for i in range(feature_num):
            if data[i] > maxs[i]:
                maxs[i] = data[i]
            if data[i] < mins[i]:
                mins[i] = data[i]
    # 归一化 使属性落到 [0,1]
    for data in dataset:
        for i in range(feature_num):
            if (maxs[i] - mins[i]) != 0:
                data[i] = (data[i] - mins[i]) / (maxs[i] - mins[i])
        res.append(data)
    return res


if __name__ == '__main__':
    training_data = read_data('horse-colic-data.csv')
    testing_data = read_data('horse-colic-test.csv')
    training_data = feature_scaling(training_data)
    testing_data = feature_scaling(testing_data)
    nn = NeuralNetwork(35, 10, 3)
    Epoch = 90
    nn = train(training_data, Epoch, nn)
    test(testing_data, nn)

    # for Epoch in range(50, 2000, 5):
    #     print('Epoch = {}'.format(Epoch))
    #     nn = NeuralNetwork(35, 10, 3)
    #     nn = train(training_data, Epoch, nn)
    #     test(testing_data, nn)








