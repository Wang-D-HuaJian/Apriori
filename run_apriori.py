import time
start = time.clock()
import sys
sys.path.append("F:/pythonTest")
from Apriori_algorithm.apriori import *

dataSet = loadDataSet()
#print(dataSet)
#C1 = createC1(dataSet)
#print(C1)

#D = list(map(set,dataSet))
#print(D)

#L1,suppData0 = scanD(D, C1, 0.5)
#print(L1)

L,suppData = apriori(dataSet)
print(L)
#print(suppData)

#result = aprioriGen(L[0], 2)
#print(result)


#L,suppData = apriori(dataSet,minSupport=0.5)
#rules = generateRules(L,suppData,minConf=0.7)
#print(rules)


#mushDatSet = [line.split() for line in open('mushroom.dat').readlines()]

#L,suppData = apriori(mushDatSet, minSupport=0.3)
#print(L)
#for item in L[1]:
#    if item.intersection('2'):
#        print(item)
end = time.clock()
print("The running time is %s Seconds!" % (end-start))