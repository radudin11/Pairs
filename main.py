# Monitors problem:
# input = pairs of two numbers in binary
# output = yes/no if there is a sequence of pairs that can be connected
# so that the numbers resulted from the concatenation of the pairs are
# equal

# example: in images

# for explanaiton of the code see README.md

import copy
import argparse

MAX_ITTER = 10

class Seq:
    def __init__(self, topSeq, bottomSeq, idList):
        self.topSeq = topSeq
        self.bottomSeq = bottomSeq
        self.idList = idList

class Pair:
    def __init__(self, top, bottom, id):
        self.top = top
        self.bottom = bottom
        self.id = id

def readPairs(inputFile):
    step = 0
    pair = Pair([], [], 0)
    pairList = []
    for line in inputFile:
        step += 1
        if step % 2 == 1:
            # read top part of pair from uneven lines
            pair.top = [int(x) for x in line.split()]
        else:
            # read bottom part of pair from even lines
            pair.bottom = [int(x) for x in line.split()]
            pair.id = int(step / 2)
            # add pair to list
            pairList.append(pair)
            # reset pair
            pair = Pair([], [], 0)
    return pairList


        

def startSeq(pairList):
    # find all possible pairs that can start a sequence
    possibleSeq = []
    for pair in pairList:
        seq = Seq([], [], [])
        if pair.top[0] == pair.bottom[0]:
            # if the first numbers of each part of 
            # the pair are equal
            seq.topSeq.extend(pair.top)
            seq.bottomSeq.extend(pair.bottom)
            seq.idList.append(pair.id)
            possibleSeq.append(seq)
    return possibleSeq

def checkSeq(seq):
    # check if the sequence is valid
    # if the numbers until the shortest length
    # resulted from the concatenation of the pairs are
    # equal
    topSeq = ""
    bottomSeq = ""
    # convert the numbers to strings
    for nr in seq.topSeq:
        topSeq += str(nr)
    for nr in seq.bottomSeq:
        bottomSeq += str(nr)
    # get shorter sequence
    minLen = min(topSeq.__len__(), bottomSeq.__len__())

    if topSeq[:minLen] == bottomSeq[:minLen]:
        return 1
    else:
        return 0

def nextSeq(seq, pairList):
    # find all possible pairs that can be connected to the current sequence
    possibleSeq = []
    for pair in pairList:
        newSeq = Seq(copy.copy(seq.topSeq), copy.copy(seq.bottomSeq), copy.copy(seq.idList))  # copy the current sequence
        # take the shorter sequence and check for any matches
        if seq.topSeq.__len__() < seq.bottomSeq.__len__() and  pair.top[0] == seq.bottomSeq[seq.topSeq.__len__()]:
            # if the first number of the top part of the pair is equal to number in the bottom sequence at the same position
            newSeq.topSeq.extend(pair.top)
            newSeq.bottomSeq.extend(pair.bottom)
            newSeq.idList.append(pair.id)
            if checkSeq(newSeq):
                # if the sequence is valid
                possibleSeq.append(newSeq)
        elif seq.topSeq.__len__() > seq.bottomSeq.__len__() and pair.bottom[0] == seq.topSeq[seq.bottomSeq.__len__()]:
            # if the first number of the bottom part of the pair is equal to number in the top sequence at the same position
            newSeq.topSeq.extend(pair.top)
            newSeq.bottomSeq.extend(pair.bottom)
            newSeq.idList.append(pair.id)
            if checkSeq(newSeq):
                # if the sequence is valid
                possibleSeq.append(newSeq)
    return possibleSeq


def findSeq(seq, pairList, itter):
    # find the sequence of pairs that can be connected
    # so that the numbers resulted from the concatenation of the pairs are
    # equal
    
    # if we have reached the maximum number of itterations => no solution
    if (itter > MAX_ITTER):
        return False

    # get all possible pairs that can be connected to the current sequence
    possibleSeq = nextSeq(seq, pairList)

    # if there are no possible pairs => no solution
    if possibleSeq.__len__() == 0:
        return False

    for newSeq in possibleSeq:
        #debug print("Trying seq at itter " + str(itter))
        #debug print(newSeq.topSeq)
        #debug print(newSeq.bottomSeq)

        # check if the sequence is complete
        if newSeq.topSeq.__len__() == newSeq.bottomSeq.__len__():
            #debug print("Found it")
            #debug print(newSeq.topSeq)
            #debug print(newSeq.bottomSeq)
            #debug print("Id list:")
            #debug print(newSeq.idList)
            return True
        else:
            # if the sequence is not complete => continue
            if findSeq(newSeq, pairList, itter+1):
                return True

def printPairs(pairList):
    # print the pairs
    for pair in pairList:
        print(pair.top)
        print(pair.bottom)
        print("")
                

def parseArgs():
    parser = argparse.ArgumentParser(description='Find sequence of pairs that can be connected \
        so that the numbers resulted from the concatenation of the pairs are equal')

    parser.add_argument('--inputFile', '-f', type=argparse.FileType('r'), help='input file')
    parser.add_argument('--max-itter', type=int, help='maximum number of itterations, default is 10\n For the best performance \
        use the length of the sollution(if known) as the maximum number of itterations')

    return parser.parse_args()

def main():
    args = parseArgs()

    if args.max_itter:
        global MAX_ITTER
        MAX_ITTER = args.max_itter
    
    if args.inputFile:
        pairList = readPairs(args.inputFile)
    else:
        # read input
        filePath = input("Enter file path: ")
        inputFile = open(filePath, "r")
        pairList = readPairs(inputFile)

    #debug printPairs(pairList)

    # find all possible sequences that can start a sequence
    possibleSeq = startSeq(pairList)

    for currentSeq in possibleSeq:
        #debug print("Start seq")
        #debug print(currentSeq.topSeq)
        #debug print(currentSeq.bottomSeq)

        # find the sequence of pairs that can be connected
        # start from itteration 1
        if findSeq(currentSeq, pairList, 1):
            print("yes")
            return
    # if no sequence was found after MAX_ITTER itterations => no solution
    print("no")

if __name__ == "__main__":
    main()