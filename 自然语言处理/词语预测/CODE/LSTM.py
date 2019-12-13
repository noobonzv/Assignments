# -*- coding: UTF-8 -*-
import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import jieba
import re

TRAINING_DATA_PATH = './预处理结果去停止词/{:d}.txt'
TRAINING_TEXT_NUM = 1000
TESTING_DATA_PATH = 'questions.txt'
ANSWER_PATH = 'answer.txt'
STOPWORDS_PATH = '停止词.txt'
WORD_DICT_PATH = 'word_dict.txt'


# 方便调参
# 设置学习率
leaning_rate_base = 1e-3
leaning_rate_decay = 0.9

time_steps = 25
Embedding_Size = 300
Batch_Size = 100
epochs = 4000

stop_words = []
answers = []
word2num = {}
num2word = {}

# 读取停止词
with open(STOPWORDS_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        stop_words.append(line.strip())
# 读取答案
with open(ANSWER_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        answers.append(line.split()[0])


class TrainingText2Vec:
    def __init__(self, file_name, text_num, max_sentence_len):
        """
        :param file_name: 训练文本的位置/文件名
        :param text_num: 训练文本的数量
        :param max_sentence_len: 一个句子最大长度，超过就截断，不足就padding, 传入时+1的！！！！
        """

        self.max_sentence_len = max_sentence_len       # 一个句子的最大长度
        self.input = []                     # 网络的输入
        self.output = []                    # 网络的预期输出
        self.length = []                    # 输入向量的实际长度
        self.mask = []                      # 长度跟输入一样，padding的位置上置零，其余为1
        self.batch_start_pos = 0            # 开始读取的位置，为取batch用
        self.training_sentence_num = 0      # 训练句子的数量

        self.encode(file_name, text_num)    # 将训练文本转成向量
        self.generate_mask()                # 生成掩码

    def encode(self, file_name, text_num):
        """
        将文本转换成向量
        :param file_name: 训练文本的位置
        :param text_num: 训练文本的数量
        """

        for i in range(1, text_num):
            with open(file_name.format(i), 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.split()
                    # 句向量, 每个词替换为 id
                    sen2vec = [word2num.get(word, 0) for word in line]
                    # 保持句向量长度一致
                    l = len(sen2vec)
                    if l <= 1:
                        continue
                    # max_sentence_len 传入时+1了，所以这些地方都要注意-1
                    if l < self.max_sentence_len:   # 不足就增加
                        sen2vec += [0] * (self.max_sentence_len - l)
                        self.length.append(l-1)
                    else:                           # 多了就删除
                        sen2vec = sen2vec[:self.max_sentence_len]
                        self.length.append(self.max_sentence_len - 1)
                    self.input.append(sen2vec[: self.max_sentence_len - 1])     # [x1, x2,...,xn-1]
                    self.output.append(sen2vec[1: self.max_sentence_len])       # 对应x的输出 [x2,x3,...,xn]

        self.training_sentence_num = len(self.input)

    def generate_mask(self):
        """
        input对应位置实际输入的位置置一，padding位置置零
        :return:
        """
        for i in range(self.training_sentence_num):
            t = [1] * self.length[i] + [0] * (self.max_sentence_len - 1 - self.length[i])
            self.mask.append(t)

    def next_batch(self, batch_size):
        """
        返回下一批的数据
        :param batch_size: 批量读取大小
        :return: 批量数据
        """

        end_pos = (self.batch_start_pos + batch_size) % self.training_sentence_num
        # 从头开始
        if self.batch_start_pos > end_pos:
            input_batch = self.input[self.batch_start_pos:] + self.input[: end_pos]
            output_batch = self.output[self.batch_start_pos:] + self.output[: end_pos]
            length_batch = self.length[self.batch_start_pos:] + self.length[: end_pos]
            mask_batch = self.mask[self.batch_start_pos:] + self.mask[: end_pos]
        else:
            input_batch = self.input[self.batch_start_pos: end_pos]
            output_batch = self.output[self.batch_start_pos: end_pos]
            length_batch = self.length[self.batch_start_pos: end_pos]
            mask_batch = self.mask[self.batch_start_pos: end_pos]

        self.batch_start_pos = end_pos                      # 更新下次读取的位置

        return input_batch, output_batch, length_batch, mask_batch


class TestingText2Vec:
    def __init__(self, file_name, max_sentence_len):
        """
        :param file_name: 测试文本位置
        :param max_sentence_len: 句子最大长度
        """
        self.input = []
        self.length = []                                # 句向量实际长度
        self.max_sentence_len = max_sentence_len        # 一个句子的最大长度
        self.test_num = 0                               # 测试数据即句子的数量

        self.encode(file_name, max_sentence_len)        # 将测试文本转成向量

    def encode(self, file_name, max_sentence_len):
        """
        将文本转换成向量
        :param file_name: 测试文本位置
        :param max_sentence_len: 句子最大长度
        """
        jieba.add_word('[MASK]')
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                # 注意要包含空格
                pos = line.find('[MASK]')
                # mask 前后的词语
                pre = line[:pos]
                # 去数字，符号，停止词，划分词语
                pre = re.sub(r'[^\u4e00-\u9fa5]', '', pre)
                pre_cut = list(jieba.cut(pre, cut_all=False))
                sentence = [word for word in pre_cut if word not in stop_words]

                # mask 前面的词的向量
                sen2vec = [word2num.get(word, 0) for word in sentence]
                l = len(sen2vec)
                # 少补增删, 同上
                if l > max_sentence_len:
                    sen2vec = sen2vec[-max_sentence_len:]
                    self.length.append(max_sentence_len)
                else:
                    sen2vec += [0] * (max_sentence_len - l)
                    self.length.append(l)

                self.input.append(sen2vec)

        self.test_num = len(self.length)

    def get_processed_data(self):
        """
        :return: 测试数据
        """
        output = np.zeros([self.test_num, self.max_sentence_len])       # 占位
        mask = np.zeros([self.test_num, self.max_sentence_len])         # 占位
        return self.input, output, self.length, mask


class LSTM:
    def __init__(self, embedding_size, time_steps, batch_size):
        """
        :param embedding_size: embedding后词语的向量维度
        :param time_steps: LSTM的时间节点个数
        :param batch_size: 每次喂入网络数据的数量
        """
        self.accuracy = 0                                       # 记录最高准确率
        self.vocab_size = len(word2num)
        self.embedding_size = embedding_size
        self.time_steps = time_steps
        self.nhidden = embedding_size
        self.batch_size = batch_size
        self.global_step = tf.Variable(0, trainable=False)      # 初始值为0，不想该变量被优化
        # 指数衰减的学习率
        self.learning_rate = tf.train.exponential_decay(leaning_rate_base,
                                                        self.global_step,
                                                        100,
                                                        leaning_rate_decay,
                                                        staircase=True)
        # placeholders 占位用
        # 输入
        self.x = tf.placeholder(shape=[self.batch_size, self.time_steps], dtype=tf.int32)
        # 输出
        self.y = tf.placeholder(shape=[self.batch_size, self.time_steps], dtype=tf.int32)
        # 原句子长度
        self.length = tf.placeholder(shape=[self.batch_size], dtype=tf.int32)
        # 掩码
        self.mask = tf.placeholder(shape=[self.batch_size, self.time_steps], dtype=tf.float32)
        # 用于计算dropout
        self.keep_prob = tf.placeholder(dtype=tf.float32)

        # embedding layer
        # vocab_size * embedding_size 的矩阵，每一行表示其编码，random_uniform [-1,1] 平均分布
        self.embedding_mat = tf.Variable(tf.random_uniform([self.vocab_size, self.embedding_size], -1, 1))
        # 在 embedding 张量列表中查找 ids, 编码
        self.inputs = tf.nn.embedding_lookup(self.embedding_mat, self.x)
        # keep_prob：一个标量Tensor,它与x具有相同类型，保留每个元素的概率，也就是用来遗忘的
        self.dinputs = tf.nn.dropout(self.inputs, keep_prob=self.keep_prob)

        # LSTM layer
        # 基础的LSTM循环网络单元，偏置增加了遗忘门
        self.lstm_cell = rnn.BasicLSTMCell(self.nhidden, forget_bias=1.0, state_is_tuple=True)
        # 遗忘门
        self.lstm = rnn.DropoutWrapper(self.lstm_cell, output_keep_prob=self.keep_prob)
        # 初始全0
        self.initial_state = self.lstm.zero_state(self.batch_size, dtype=tf.float32)
        # 通过动态生成的RNN网络
        self.output, _ = tf.nn.dynamic_rnn(self.lstm, self.dinputs, initial_state=self.initial_state,
                                           dtype=tf.float32, time_major=False)
        # 将tensor变换为  [batch_size * time_steps, nhidden]
        self.reshape_output = tf.reshape(self.output, [self.batch_size*self.time_steps, self.nhidden])

        # full connect layer
        # 权重与偏执
        self.w = tf.Variable(tf.truncated_normal([self.nhidden, self.vocab_size]), dtype=tf.float32)
        self.b = tf.Variable(tf.zeros([self.vocab_size]))
        # 矩阵乘法
        self.prob = tf.matmul(self.reshape_output, self.w) + self.b
        self.reshape_prob = tf.reshape(self.prob, [self.batch_size, self.time_steps, self.vocab_size])

        # 损失函数 求loss平均值
        self.loss = tf.contrib.seq2seq.sequence_loss(
            self.reshape_prob,
            self.y,
            self.mask,
            average_across_timesteps=False,
            average_across_batch=True)
        self.mloss = tf.reduce_mean(self.loss)
        self.cost = tf.reduce_sum(self.loss)
        # 返回需要训练的变量
        tvars = tf.trainable_variables()
        # 限制梯度
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, tvars), 5)
        # 应用处理过后的梯度进行训练
        self.train = tf.train.AdamOptimizer(self.learning_rate).apply_gradients(
            zip(grads, tvars), global_step=self.global_step)

    def test(self, sess, x, y, l, m):
        accuracy = 0
        predictions = []
        size = len(x)
        output = sess.run(self.reshape_prob, feed_dict={self.x: x, self.y: y, self.length: l,
                                                        self.mask: m, self.keep_prob: 1.0})
        for i in range(size):
            prediction = np.argmax(output[i, l[i]-1, :])
            prediction = num2word[prediction]
            predictions.append(prediction)
            if prediction == answers[i]:
                print(prediction)
                accuracy += 1

        # 如果本次的准确率较高就保存
        if accuracy > self.accuracy:
            self.accuracy = accuracy
            predictions = '\n'.join(predictions)
            with open('rnn_predictions', 'w', encoding='utf-8') as f:
                f.write(predictions)

        return float(accuracy) / float(size)


def map_word():
    """
    建立词与id的映射
    :return: 两个字典
    """
    word_to_id = {}
    id_to_word = {}
    with open(WORD_DICT_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.split()
            word_to_id[line[1]] = int(line[0])
    word_to_id['Unknown'] = 0
    for key, value in word_to_id.items():
        id_to_word[value] = key
    return word_to_id, id_to_word


if __name__ == '__main__':
    # 原文向量化
    word2num, num2word = map_word()
    train_data = TrainingText2Vec(TRAINING_DATA_PATH, TRAINING_TEXT_NUM + 1, time_steps + 1)
    test_data = TestingText2Vec(TESTING_DATA_PATH, time_steps)
    # 处理过后的的测试数据
    test_x, test_y, test_actual_lens, test_mask = test_data.get_processed_data()
    model = LSTM(Embedding_Size, time_steps, Batch_Size)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(epochs + 1):
            input_batch, output_batch, length_batch, mask_batch = train_data.next_batch(Batch_Size)
            # 第一个参数就是要计算的东西，最后会返回他们
            _, loss, step = sess.run([model.train, model.mloss, model.global_step],
                                     feed_dict={model.x: input_batch, model.y: output_batch,
                                                model.length: length_batch, model.mask: mask_batch,
                                                model.keep_prob: 1.0})

            if i % 50 == 0:
                print('Epoch: {:d}, Loss {:f}'.format(step-1, loss))
                print('Accuracy: {:.2%}'.format(model.test(sess, test_x, test_y, test_actual_lens, test_mask)))
                print()

