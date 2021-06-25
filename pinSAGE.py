from collections import Counter

path2 = 'C:/Users/PC/Desktop/node2vec/' + 'PinSAGE_user_relationship.txt'
file3 = open(path2, 'w')

# pinSAGE图重构
for i2 in range(0, 7):  # i2代表起始结点用户,range(0,重构用户数量)，这里取0,1,2,3,4,5,6号作示范
    path = 'C:/Users/PC/Desktop/node2vec/all_user_path/' + 'user_' + str(i2) + '.txt'
    file2 = open(path, 'r')
    presence_record = []  # 用于记录用户在路径中出现的记录
    for i in file2:
        # 将(u1,u2)  (u2,u3)...的形式改为['u1,u2','u2,u3',...]
        line = i.replace("\t", "").replace("\n", "").replace("(", '').replace(")", ' ')
        line = line.split(" ")
        # 将['u1,u2','u2,u3',...]中的u1,u2,...提取出来并保存到presence_record中
        for i3 in line:
            i3 = i3.split(",")
            # print(i3)
            try:
                presence_record.append(i3[1])
            except:
                continue
    file2.close()

    frequency = Counter(presence_record)  # 把列表换成字典统计
    k = frequency.most_common(len(frequency))  # 找出全部元素从大到小的元素频率以及对应的次数。
    print(k)

    # for i in k:
    #     print(str(i[0]) + " " + str(i[1]))
    # 将频率前5的与初始结点构成新的关系图

    top_k = 5  # 取出现频率前top_k个用户重构图
    for i3 in range(0, top_k):
        if str(k[i3][0]) != str(i2):  # u2不能与起始节点用户是同一个用户
            PinSAGE_rel = str(i2) + '\t' + str(k[i3][0]) + '\t' + '1' + '\n'
            file3.writelines(PinSAGE_rel)
        else:
            PinSAGE_rel = str(i2) + '\t' + str(k[5][0]) + '\t' + '1' + '\n'  # 若前5个出现过与起始结点用户相同id的用户，则第六个结点肯定不会再相同
            file3.writelines(PinSAGE_rel)

file3.close()
