from pomegranate import *

# 已知概率
Burglary = DiscreteDistribution({'B': 0.001, '!B': 0.999})
Earthquake = DiscreteDistribution({'E': 0.002, '!E': 0.998})

# 条件依赖
Alarm = ConditionalProbabilityTable(
       [['B', 'E', 'A', 0.95],
        ['B', 'E', '!A', 0.05],
        ['B', '!E', 'A', 0.94],
        ['B', '!E', '!A', 0.06],
        ['!B', 'E', 'A', 0.29],
        ['!B', 'E', '!A', 0.71],
        ['!B', '!E', 'A', 0.001],
        ['!B', '!E', '!A', 0.999]],
        [Burglary, Earthquake])

JohnCalls = ConditionalProbabilityTable(
       [['A', 'J', 0.9],
        ['A', '!J', 0.1],
        ['!A', 'J', 0.05],
        ['!A', '!J', 0.95]],
        [Alarm])

MaryCalls = ConditionalProbabilityTable(
       [['A', 'M', 0.7],
        ['A', '!M', 0.3],
        ['!A', 'M', 0.01],
        ['!A', '!M', 0.99]],
        [Alarm])

# 5个节点
s1 = State(Burglary, name="Burglary")
s2 = State(Earthquake, name="Earthquake")
s3 = State(Alarm, name="Alarm")
s4 = State(JohnCalls, name="JohnCalls")
s5 = State(MaryCalls, name="MaryCalls")

model = BayesianNetwork("E09_1")

model.add_states(s1, s2, s3, s4, s5)

# 依赖  (Parent, Child)
model.add_transition(s1, s3)
model.add_transition(s2, s3)
model.add_transition(s3, s4)
model.add_transition(s3, s5)

model.bake()

T311 = model.predict_proba({})[2].parameters[0]['A']
print('P(A) = ', T311)

T312 = model.probability([['B', 'E', 'A', 'J', '!M'],
                         ['!B', 'E', 'A', 'J', '!M'],
                         ['B', '!E', 'A', 'J', '!M'],
                         ['!B', '!E', 'A', 'J', '!M'],
                         ['B', 'E', '!A', 'J', '!M'],
                         ['!B', 'E', '!A', 'J', '!M'],
                         ['B', '!E', '!A', 'J', '!M'],
                         ['!B', '!E', '!A', 'J', '!M']]).sum()

print('P(J&&~M) = ', T312)

T313 = model.predict_proba({'JohnCalls': 'J', 'MaryCalls': '!M'})[2].parameters[0]['A']
print("P(A |J&&~M) = ", T313)

T314 = model.predict_proba({'Alarm': 'A'})[0].parameters[0]['B']
print("P(B |A) = ", T314)

T315 = model.predict_proba({'JohnCalls': 'J', 'MaryCalls': '!M'})[0].parameters[0]['B']
print("P(B |J&&~M) = ", T315)


P_J_notM_notB = T312 * (1 - T315)
T316 = P_J_notM_notB / 0.999
print("P(J&&~M |~B) = ", T316)
