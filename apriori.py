from numpy import *

def loadDataSet():
    """创建用于测试的简单数据集"""
    # simpDat = [['r', 'z', 'h', 'j', 'p'],
    #            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
    #            ['z'],
    #            ['r', 'x', 'n', 'o', 's'],
    #            ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    #            ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    # return simpDat
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createC1(dataSet):
    """大小为一的所有候选集的集合"""
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    return list(map(frozenset, C1))#use frozen set so we
                            #can use it as a key in a dict

def scanD(D, Ck, minSupport):
    """扫描数据集判断项集是否满足最小支持度的要求"""
    ssCnt = {}####空字典存储项集及对应出现次数
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt: ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(D))####数据集总长度（用于计算支持度）
    retList = []####存储所有满足最小支持度的项集
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)####首部插入新的集合
        supportData[key] = support
    return retList, supportData


##testing：
# dataSet = loadDataSet()
# print(dataSet)
# C1 = createC1(dataSet)
# print(C1)
# D = list(map(set, dataSet))
# L1, suppData0 = scanD(D, C1, 0.5)
# print(L1)
# print(suppData0)

#####Apriori算法
def aprioriGen(Lk, k): #creates Ck
    """创建候选集Ck"""
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2: #if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j]) #set union
    return retList

def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)#scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

# #testing:
# dataSet = loadDataSet()
# L, supportData = apriori(dataSet)
# print(L)
# print(supportData)


#####关联规则生成函数
def generateRules(L, supportData, minConf=0.7):  #supportData is a dict coming from scanD
    bigRuleList = []
    for i in range(1, len(L)):#only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    """对规则进行评估"""
    prunedH = [] #create new list to return
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
        if conf >= minConf:
            print (freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    """生成候选规则集合（合并相同项）"""
    m = len(H[0])
    if (len(freqSet) > (m + 1)): #try further merging
        Hmp1 = aprioriGen(H, m+1)#create Hm+1 new candidates
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):    #need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


###testing
dataSet = loadDataSet()
L, suppData = apriori(dataSet, minSupport=0.5)
rules = generateRules(L, suppData, minConf=0.5)
print(rules)
  

#######美国国会会议案
