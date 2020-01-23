# -*- coding: UTF-8 -*-
from copy import deepcopy


class VariableElimination:
    @staticmethod
    def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
        # Your code here
        # restrict factors
        # ev 是字符,某个变量名，其字典值为取值
        for ev in evidenceList.keys():
            value = evidenceList[ev]
            for i, factor in enumerate(factorList):
                # 某节点只要有该变量就限制该变量取值，用restrict后的节点替换该节点
                if ev in factor.varList:
                    factorList[i] = factor.restrict(ev, value)

        # 依次消除变量
        for var in orderedListOfHiddenVariables:
            # 找到所有包含该变量的节点
            factor_include_var = [factor for factor in factorList if var in factor.varList]
            # 先 multiply， 再 sumout
            if len(factor_include_var) > 0:
                g = factor_include_var[0]
                temp = factor_include_var[0]
                for factor in factor_include_var[1:]:
                    g = g.multiply(factor)
                    factorList.remove(factor)

                g = g.sumout(var)
                factorList.remove(temp)
                if len(g.varList) > 0:
                    factorList.append(g)

        print("RESULT:")
        res = factorList[0]
        for factor in factorList[1:]:
            res = res.multiply(factor)
        total = sum(res.cpt.values())
        res.cpt = {k: v/total for k, v in res.cpt.items()}
        res.printInf()

    @staticmethod
    def printFactors(factorList):
        for factor in factorList:
            factor.printInf()


class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.varList = var_list
        # cpt:  每一行是 变量取值列表(01字符串):概率
        self.cpt = {}

    def setCpt(self, cpt):
        self.cpt = cpt

    def printInf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.varList))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        # print(self.cpt.items())
        print("")

    def multiply(self, factor):
        """function that multiplies with another factor"""
        # 两个factor中相同变量的项作乘积
        # Your code here
        new_cpt = {}
        new_var_list = deepcopy(self.varList)
        # print(self.varList, factor.varList)
        same_variables_index_tup = []
        # 记录相同变量在2个factor中的对应下标元组
        for i in range(len(self.varList)):
            for j in range(len(factor.varList)):
                if self.varList[i] == factor.varList[j]:
                    same_variables_index_tup.append((i, j))

        # 以本身为标准，把另一个factor中新变量按顺序加在原变量后面
        for var in factor.varList:
            if var not in new_var_list:
                new_var_list.append(var)

        # 遍历两个cpt，只有共同元素取值相同时才做乘积
        for row1, prob1 in self.cpt.items():
            for row2, prob2 in factor.cpt.items():
                same = True
                # 每一对共同元素都相同才行
                for tup in same_variables_index_tup:
                    i = tup[0]
                    j = tup[1]
                    if row1[i] != row2[j]:
                        same = False
                        break
                if same:
                    new_row = row1
                    # 按之前去确定的变量属性加入，一定要对应
                    for index in range(len(row2)):
                        if factor.varList[index] not in self.varList:
                            new_row += row2[index]
                    new_cpt[new_row] = prob1 * prob2

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        # print("mul: ", new_var_list, new_node.cpt.items())
        return new_node

    def sumout(self, variable):
        """function that sums out a variable given a factor"""
        # 对传进来的变量合并，也就是合并除了该变量，其他都相同的项，最后的表就不含这个变量了
        # Your code here
        i = self.varList.index(variable)
        new_var_list = self.varList[:i] + self.varList[i + 1:]

        new_cpt = {}
        for row, prob in self.cpt.items():
            new_row = row[:i] + row[i+1:]
            # 对该变量的取值概率求和 !!!
            new_cpt[new_row] = new_cpt.get(new_row, 0) + prob

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        # print("sumout: ", new_var_list, new_node.cpt.items())
        return new_node

    def restrict(self, variable, value):
        """function that restricts a variable to some value
        in a given factor"""
        # 只保留CPT中 variable变量取值为value的项
        # Your code here
        # cpt:  每一行是 变量取值列表(01字符串):概率
        # eg:  123 (即a=1,b=2,c=3) : 0.9
        # 找到该变量在字符串中的位置
        i = self.varList.index(variable)
        new_cpt = {}
        # 只保留符合要求的
        for row, prob in self.cpt.items():
            # row是012..字符串
            if int(row[i]) == value:
                # print(variable,value)
                new_cpt[row[:i]+row[i+1:]] = prob

        # 在变量列表中删除该变量
        new_var_list = self.varList[:i] + self.varList[i + 1:]

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        # print("res: ", new_var_list, new_node.cpt.items())
        return new_node


PatientAge = Node("PatientAge", ["PatientAge"])
CTScanResult = Node("CTScanResult", ["CTScanResult"])
MRIScanResult = Node("MRIScanResult", ["MRIScanResult"])
Anticoagulants = Node("Anticoagulants", ["Anticoagulants"])

StrokeType = Node("StrokeType", ["CTScanResult", "MRIScanResult", "StrokeType"])
Mortality = Node("Mortality", ['StrokeType', "Anticoagulants", "Mortality"])
Disability = Node("Disability", ["StrokeType", "PatientAge", "Disability"])


# PatientAge:['0-30','31-65','65+']    [0,1,2]
# CTScanResult:['Ischemic Stroke','Hemmorraghic Stroke']   [0,1]
# MRIScanResult: ['Ischemic Stroke','Hemmorraghic Stroke']  [0,1]
# StrokeType: ['Ischemic Stroke','Hemmorraghic Stroke', 'Stroke Mimic']  [0,1,2]
# Anticoagulants: ['Used','Not used']   [1,0]
# Mortality:['False', 'True']   [0,1]
# Disability: ['Negligible', 'Moderate', 'Severe']    [0,1,2]

PatientAge.setCpt({'0': 0.10, '1': 0.30, '2': 0.60})
CTScanResult.setCpt({'0': 0.70, '1': 0.30})
MRIScanResult.setCpt({'0': 0.70, '1': 0.30})
Anticoagulants.setCpt({'0': 0.50, '1': 0.50})


# CTS IS:0  HS:1
# MRI IS:0  HS:1
# Str IS:0  HS:1  SM:2
StrokeType.setCpt({'000': 0.8, '010': 0.5,
                   '100': 0.5, '110': 0.0,

                   '001': 0.0, '011': 0.4,
                   '101': 0.4, '111': 0.9,

                   '002': 0.2, '012': 0.1,
                   '102': 0.1, '112': 0.1})

# Str IS:0  HS:1  SM:2
# Ant U:1   N:0
# Mor T:1   F:0
Mortality.setCpt({'010': 0.28, '110': 0.99,
                  '210': 0.10, '000': 0.56,
                  '100': 0.58, '200': 0.05,

                  '011': 0.72, '111': 0.01,
                  '211': 0.90, '001': 0.44,
                  '101': 0.42, '201': 0.95})

# Str IS:0    HS:1     SM:2
# Pat 0-30:0  31-65:1  65+:2
# Dis N:0     M:1      S:2
Disability.setCpt({'000': 0.80, '100': 0.70, '200': 0.90,
                   '010': 0.60, '110': 0.50, '210': 0.40,
                   '020': 0.30, '120': 0.20, '220': 0.10,

                   '001': 0.10, '101': 0.20, '201': 0.05,
                   '011': 0.30, '111': 0.40, '211': 0.30,
                   '021': 0.40, '121': 0.20, '221': 0.10,

                   '002': 0.10, '102': 0.10, '202': 0.05,
                   '012': 0.10, '112': 0.10, '212': 0.30,
                   '022': 0.30, '122': 0.60, '222': 0.80})


factors = [PatientAge, CTScanResult, MRIScanResult, Anticoagulants, StrokeType, Mortality, Disability]
print("p1 = P(Mortality='True' && CTScanResult='IS' | PatientAge='31-65')")
print("CTS IS:0  HS:1    Mortality T:1 F:0")
VariableElimination.inference(deepcopy(factors),
                              ["Mortality", "CTScanResult"],
                              ["MRIScanResult", "Anticoagulants", "StrokeType", "Disability"],
                              {"PatientAge": 1})


print("p2 = P(Disability='M' && CTScanResult='HS' | PatientAge='65+' &&  MRIScanResult='HS')")
print("CTS IS:0  HS:1    Disability N:0 M:1 S:2")
VariableElimination.inference(deepcopy(factors),
                              ["Disability", "CTScanResult"],
                              ["Anticoagulants", "StrokeType", "Mortality"],
                              {"PatientAge": 2, "MRIScanResult": 1})


print("p3 = P(StrokeType='HS' | PatientAge='65+' && CTScanResult='HS' && MRIScanResult='IS')")
print("StrokeType IS:0  HS:1  SM:2")
VariableElimination.inference(deepcopy(factors),
                              ["StrokeType"],
                              ["Mortality", "Disability", "Anticoagulants"],
                              {"PatientAge": 2, "CTScanResult": 1, "MRIScanResult": 0})

print("p4 = P(Anticoagulants='Used' | PatientAge='31-65')")
print("Anticoagulants U:1   N:0")
VariableElimination.inference(deepcopy(factors),
                              ["Anticoagulants"],
                              ["CTScanResult", "MRIScanResult", "StrokeType", "Mortality", "Disability"],
                              {"PatientAge": 1})

print("p5 = P(Disability='Negligible')")
print("Disability N:0 M:1 S:2")
VariableElimination.inference(deepcopy(factors),
                              ["Disability"],
                              ["PatientAge", "CTScanResult", "MRIScanResult",
                               "Anticoagulants", "StrokeType", "Mortality"],
                              {})

