# SYSU 人工智能 
只上传了部分实验，有的实验只是完成某些函数，自己写的内容不多的实验就没有上传了。
每个实验的文件夹下有一个PDF，里面是实验要求和实验中一些要注意的地方。

对于部分实验可能会用到一些工具，比如E06会用到 Swi-Prolog 运行Prolog代码文件， E07可能会用到FF Planner，这些工具的安装与使用可参考 `人工智能工具安装说明v3.0.pdf`.

### E01 走迷宫(BFS) | Python
给定地图，找到一条从起点到终点的路径并输出。
* MaseData.txt：迷宫地图，包含起点(S)和终点(E)

### E02 15数码问题(A* 算法) | Python
4x4数字版拼图，移动方块，使得方块按顺序放置。

### E04 Futoshiki(Forword checking) | C++
有点像数独的游戏，填充数字，使得每行每列不能有相同数字，并且满足一些不等式限制。
* board.txt: 初始状态
* constraint.txt: 限制条件

### E06 Queries | Prolog
用 Prolog 实现对知识库中的某些信息的查询，如 哪些餐厅的分店数最少？
* Restaurants.pl: 代码文件

### E07 FF Planner | PDDL
使用PDDL解决8数码问题和积木世界问题。
* E07_block_domain.pddl: 积木世界问题相关谓词的定义。
* E07_block_prob.pddl: 积木世界问题相关变量的定义，初始化状态以及目标状态的定义。
* E07_puzzle_domain.pddl: 8数码问题相关谓词的定义。
* E07_puzzle_prob.pddl: 8数码问题相关变量的定义，初始化状态以及目标状态的定义。

### E09 贝叶斯网络 | Python
利用pomegranate库构建贝叶斯网络，计算概率。

### E11 决策树 | Python
实现决策树算法，对给定数据集建立决策树并进行预测。

### E12 朴素贝叶斯 | Python
用朴素贝叶斯在E11中的数据集上进行预测。
