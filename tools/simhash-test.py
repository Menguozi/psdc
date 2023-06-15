from simhash import Simhash
import sys

class smallFile:
    def __init__(self):
        self.st_ino = 0
        self.srcpath = ""
        self.st_size = 0
        self.simhash = 0
        self.index = 0

def hamming(a, b):
    # compute and return the Hamming distance between the integers
    return bin(int(a) ^ int(b)).count("1")

def takeHash(elem):
    return elem.simhash.value

fileList = []
str1 = "st_ino:"
str2 = "i_srcpath:"
str3 = "st_size:"
file_txt = open("small_file.txt", "r")
listOfLines = file_txt.readlines()
index = 0

for line in listOfLines:
    #print(line.strip())
    fileList.append(smallFile())
    index1 = line.find(str1)
    index2 = line.find(str2)
    index3 = line.find(str3)
    #print(tmp[0])
    fileList[index].st_ino = int(line[index1 + 7 : index2].strip("\s"))
    fileList[index].srcpath = line[index2 + 10 : index3].strip()
    #fileList[index].srcpath = re.sub('\t','',fileList[index].srcpath)
    # print(fileList[index].srcpath)
    fileList[index].st_size = int(line[index3 + 8 : ])
    with open(fileList[index].srcpath, encoding='ISO-8859-1') as file:
        content = file.read()
        fileList[index].simhash = Simhash(content)
        #print(index)
        #print(fileList[index].simhash.value)
        #print(fileList[index].srcpath)
    index = index + 1
    #print(type(fileList[index].st_size))

file_txt.close()

origin = open("hash-origin.txt", "w+")
originDistanceSum = 0
for i in range(len(fileList) - 1) :
    hammingDistance = hamming(fileList[i].simhash.value, fileList[i + 1].simhash.value)
    origin.write(str(hammingDistance))
    origin.write("\n")
    # print(hammingDistance)
    originDistanceSum = originDistanceSum + hammingDistance
originDistanceAvg = originDistanceSum / (len(fileList) - 1)
print("originDistanceAvg:")
print(originDistanceAvg)
origin.close()


hashMin = fileList[0].simhash.value
minIndex = 0
hashList = []
fileLen = len(fileList)
for i in range(1, fileLen) :
    if fileList[i].simhash.value < hashMin :
        minIndex = i
        hashMin = fileList[i].simhash.value

hashList.append(fileList.pop(minIndex))
#print(hashList[0].simhash.value)
while len(fileList) :
    # print("in")
    nextHashIndex = 0
    minDistance = sys.maxsize
    tmpHashList = []
    tmpHashList.append(hashList[-1])
    fileListLen = len(fileList)
    for j in range(0, fileListLen) :
        fileList[j].index = j
        hammingDistance = hamming(hashList[-1].simhash.value, fileList[j].simhash.value)
        if hammingDistance < minDistance :
            tmpHashList.clear()
            tmpHashList.append(fileList[j])
            minDistance = hammingDistance
        elif hammingDistance == minDistance :
            tmpHashList.append(fileList[j])
    if len(tmpHashList) == 1 :
        hashList.append(fileList.pop(tmpHashList[0].index))
    elif len(tmpHashList) > 1 :
        # tmpHashList.sort(key = takeHash, reverse = True)
        tmpLen = len(tmpHashList)
        for k in range(tmpLen) :
            # print(tmpHashList[k].index)
            # print(len(fileList))
            hashList.append(fileList.pop(tmpHashList[k].index - k))
        # minHashValue = sys.maxsize
        # minHashIndex = 0
        # for k in range(0, len(tmpHashList)) :
        #     if tmpHashList[k].simhash.value < minHashValue :
        #         minHashIndex = k
        # hashList.append(fileList.pop(tmpHashList[minHashIndex].index))
    # print(len(fileList))
# print(len(hashList))
sim = open("hash-sim.txt", "w+")
simDistanceSum = 0
for i in range(len(hashList) - 1) :
    hammingDistance = hamming(hashList[i].simhash.value, hashList[i + 1].simhash.value)
    sim.write(str(hammingDistance))
    sim.write("\n")
    # print(hammingDistance)
    simDistanceSum = simDistanceSum + hammingDistance
simDistanceAvg = simDistanceSum / (len(hashList) - 1)
print("simDistanceAvg:")
print(simDistanceAvg)
sim.close()

fileHash = open("small_file_simhash.txt", "w+")
for i in range(len(hashList)) :
    # line = "st_ino:" + str(hashList[i].st_ino) + "\ti_srcpath:" + hashList[i].srcpath + "\tst_size:" \
    #         + str(hashList[i].st_size) + "\n"
    fileHash.write(str(hashList[i].st_ino))
    fileHash.write("\n")
    fileHash.write(hashList[i].srcpath)
    fileHash.write("\n")
    fileHash.write(str(hashList[i].st_size))
    fileHash.write("\n")
    # print(hammingDistance)

fileHash.close()
