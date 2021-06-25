import networkx as nx
from node2vec import Node2Vec
from matplotlib import pyplot as plt
import numpy as np

graph = nx.fast_gnp_random_graph(n=100, p=0.5)  # 快速随机生成一个无向图
node2vec = Node2Vec(graph, dimensions=64, walk_length=30, num_walks=100, p=0.3, q=0.7, workers=4)  # 初始化模型
model = node2vec.fit()  # 训练模型

with open('./PinSAGE/Data/douban_user_nei.txt', 'r') as f:
    edges = []  # 初始数据集
    user_set = set()
    for line in f:
        a = line.split()
        edges.append((int(a[0]), int(a[1])))
        user_set.add(int(a[0]))

# 利用networs构建图
plt.figure(figsize=(80, 50))
G = nx.Graph()
G.add_nodes_from(list(user_set))
G.add_edges_from(edges)
pos = nx.spring_layout(G, pos=None,  # (list or None optional (default=None))
                       k=0.9,  # 设置node间距 默认节点个数的1/(n^2)  n的平方分之一，n时node节点个数，
                       fixed=None,  # 固定初始化
                       # iterations=50,生成layout应用默认弹力算法，每次默认遍历50各点
                       # threshold,#float optional (default = 1e-4)当画图点单node位置更改误差小于这个值时便不再修改n单ode得位置
                       weight=1,  # 给边设置权重，默认1
                       scale=30,  # 当pos参数None时才有用，设置画图比例影响因子，默认1
                       center=None  # 设置重心点，默认None fixed 为None设置才有用
                       # dim= # (int) – Dimension of layout. 布局尺寸
                       # seed 随机种子数，default None ，使用Random模式，
                       )
labels = {x: x for x in G.nodes()}
nx.draw_networkx_nodes(G, pos, nodelist=list(user_set), node_color='r', node_size=100, )
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
nx.draw_networkx_labels(G, pos, labels, font_size=5)
# plt.show()

# 节点的度
with open('./PinSAGE/Data/douban_degree.txt', 'r') as f1:
    degree = []
    a = f1.read()
    a = a.split()
    # print(a, end='\n')
    for i in range(6):
        degree.append(int(a[i][:-1]))

# 计算比率
ratio = []
for i in degree:
    ratio.append(i / len(degree))


# 归一化

def maxmin(x):
    return [(float(i - min(x))) / float(max(x) - min(x)) for i in x]


ratio_s = maxmin(ratio)


# 找中位数
def get_median(data):
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2


median = get_median(ratio_s)

# 计算每个节点的q
q_l = []
for i in range(len(ratio_s)):
    if ratio_s[i] > median:
        q_l.append(np.exp(ratio_s[i]))
    else:
        q_l.append(np.exp(ratio_s[i] - 1))

file1 = open('./PinSAGE/Data/user_Id.txt')
num = 0  # q值下标
for user_Id in file1:
    q = q_l[num]  # q值在此输入
    user_Id = user_Id.replace('\n', '')
    path = './PinSAGE/all_user_path/' + 'user_' + user_Id + '.txt'
    file2 = open(path, 'w')
    node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=30, p=2, q=q, workers=4)
    walk_route = node2vec.walks
    for i in walk_route:
        if i[0] == user_Id:
            relationship = []
            for k1 in range(0, 30):
                if k1 <= 27:
                    rel = '(' + str(i[k1]) + ',' + str(i[k1 + 1]) + ')' + '\t'
                    relationship.append(rel)
                elif k1 == 28:
                    rel = '(' + str(i[k1]) + ',' + str(i[k1 + 1]) + ')' + '\n'
                    relationship.append(rel)
            print(relationship)
            file2.writelines(relationship)
    num = num + 1
    file2.close()
