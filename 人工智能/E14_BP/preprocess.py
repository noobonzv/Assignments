#coding=utf-8
import numpy as np
import pandas as pd
np.set_printoptions(threshold=np.inf)

# 新建一个长度为len_vec的向量，除了第idx位为1外，其余位置的元素都是0
def onehot(idx, len_vec):
	vec = [0] * len_vec
	vec[idx] = 1
	return vec

# 初步处理训练集，把所有问号换成nan，其余不变
with open('horse-colic.data', 'r') as fr:
	train_set = []
	for line in fr.readlines():
		data = []
		splitted = line.strip().split(' ')
		for idx, x in enumerate(splitted):
			if x == '?':
				data.append(np.nan)
			else:
				data.append(x)
		train_set.append(data)
train_set = np.array(train_set)

# 初步处理测试集，把所有问号换成nan，其余不变
with open('horse-colic.test', 'r') as fr:
	test_set = []
	for line in fr.readlines():
		data = []
		splitted = line.strip().split(' ')
		for idx, x in enumerate(splitted):
			if x == '?':
				data.append(np.nan)
			else:
				data.append(x)
		test_set.append(data)
test_set = np.array(test_set)

# DataFrame中的列名
columns = ['surgery', 'age', 'hospital number', 'rectal temperature', 'pulse', 'respiratory rate', 'temperature of extremities', 'peripheral pulse', 'mucous membranes', 'capillary refill time', 'pain', 'peristalsis', 'abdominal distension', 'nasogastric tube', 'nasogastric reflux', 'nasogastric reflux PH', 'rectal examination', 'abdomen', 'packed cell volume', 'total protein', 'abdominocentesis appearance', 'abdomcentesis total protein', 'outcome', 'surgical lesion', 'lesion type1', 'lesion type2', 'lesion type3', 'cp_data']

# 生成训练集的DataFrame
df_train = pd.DataFrame(train_set, columns = columns)
# 生成测试集的DataFrame
df_test = pd.DataFrame(test_set, columns = columns)
# 将训练集与测试集纵向合并，方便两者一起进行预处理
df_train = pd.concat([df_train, df_test])

# 删掉第3列，即'hospital number'这一列
df_train.drop('hospital number', axis = 1, inplace = True)
# 将第1列中的2都换成0
df_train.ix[df_train['surgery'] == '2', 'surgery'] = '0'
# 将第2列中的9都换成0
df_train.ix[df_train['age'] == '9', 'age'] = '0'

# 下面的for循环用于拆分原数据集第25、26、27这三列，比如将03111拆分成03、1、1、1
# 拆分的主要思想是先将这三列删掉，然后依次插入12列新数据
for i in range(1, 4, 1):
	name = 'lesion type' + str(i)
	idx = df_train.columns.tolist().index(name)
	series = df_train[name]
	new_cols = np.array([[x[:2], x[2], x[3], x[4]] for x in list(series)])
	df_train.drop(name, axis = 1, inplace = True)
	df_train.insert(idx, 'site' + str(i), new_cols[:, 0])
	df_train.insert(idx + 1, 'type' + str(i), new_cols[:, 1])
	df_train.insert(idx + 2, 'subtype' + str(i), new_cols[:, 2])
	df_train.insert(idx + 3, 'special code' + str(i), new_cols[:, 3])
columns = df_train.columns.tolist()

# 将训练集和测试集拆分
df_train, df_test = df_train.iloc[:300, :], df_train.iloc[300:, :]
train_set = df_train.values.astype('float')
test_set = df_test.values.astype('float')

print train_set.shape, test_set.shape

# 计算训练集每一列的均值
average = np.nanmean(train_set, axis = 0)
# 将训练集中为nan的值替换为相应的均值
for i in range(train_set.shape[0]):
	for j in range(train_set.shape[1]):
		if np.isnan(train_set[i][j]):
			train_set[i][j] = average[j]

# 将测试集中为nan的值替换为相应的均值
for i in range(test_set.shape[0]):
	for j in range(test_set.shape[1]):
		if np.isnan(test_set[i][j]):
			test_set[i][j] = average[j]

# 保存训练集和测试集
df_train = pd.DataFrame(train_set, columns = columns)
df_test = pd.DataFrame(test_set, columns = columns)
df_train.to_csv('horse-colic-data.csv', index = 0)
df_test.to_csv('horse-colic-test.csv', index = 0)
