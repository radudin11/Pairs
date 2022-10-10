# repo: https://github.com/radudin11/Pairs


# Pairs problem:
# input = pairs of two numbers in binary
# output = yes/no if there is a sequence of pairs that can be connected
# so that the numbers resulted from the concatenation of the pairs are
# equal

# example: in images

# for explanaiton of the code see README.md

import copy
import argparse
from io import BufferedReader
import time
import sys
from tokenize import String

MAX_ITTER = 10
DEBUG = False


class Pair:
    def __init__(self, top: list, bottom: list, id: int):
        self.top = top
        self.bottom = bottom
        self.id = id

    def __str__(self) -> str:
        return "Pair: " + str(self.id) + "\n" + str(self.top) + "\n" + str(self.bottom) + "\n"

    def __repr__(self) -> str:
        return self.__str__()


class Seq:
    def __init__(self, topSeq: list, bottomSeq: list, idList: list):
        self.topSeq = topSeq
        self.bottomSeq = bottomSeq
        self.idList = idList

    def __eq__(self, other: 'Seq') -> bool:
        if self.topSeq == other.topSeq and self.bottomSeq == other.bottomSeq:
            return True
        return False

    def __str__(self) -> str:
        return str(self.topSeq) + "\n" + str(self.bottomSeq) + "\nId list:\n" + str(self.idList) + "\n"

    def __repr__(self) -> str:
        return self.__str__()

    def isExtendable(self, pair: Pair) -> bool:
        if self.topSeq.__len__() > self.bottomSeq.__len__() \
                and pair.bottom[0] == self.topSeq[self.bottomSeq.__len__()]:
            return True
        if self.topSeq.__len__() < self.bottomSeq.__len__() \
                and pair.top[0] == self.bottomSeq[self.topSeq.__len__()]:
            return True
        return False

    def extend(self, pair: Pair):
        self.topSeq.extend(pair.top)
        self.bottomSeq.extend(pair.bottom)
        self.idList.append(pair.id)


def readPairs(inputFile: BufferedReader) -> list:
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


def startSeq(pairList: list) -> list:
    # find all possible pairs that can start a sequence
    # return a list of sequences
    possibleSeq = []
    for pair in pairList:
        seq = Seq([], [], [])
        if pair.top[0] == pair.bottom[0]:
            # if the first numbers of each part of
            # the pair are equal
            seq.extend(pair)
            possibleSeq.append(seq)
    return possibleSeq


def checkSeq(seq: Seq) -> bool:
    # check if the sequence is valid

    # if the numbers until the shortest length resulted
    # from the concatenation of the pairs are equal

    minLen = min(seq.topSeq.__len__(), seq.bottomSeq.__len__())

    if seq.topSeq[:minLen] == seq.bottomSeq[:minLen]:
        return True
    else:
        return False


def nextSeq(seq: Seq, pairList: list) -> list:
    # find all possible pairs that can be connected to the current sequence
    # return a list of the extended sequences

    possibleSeq = []
    for pair in pairList:
        newSeq = Seq(copy.copy(seq.topSeq), copy.copy(seq.bottomSeq),
                     copy.copy(seq.idList))  # copy the current sequence
        # take the shorter sequence and check for any matches
        # check if the pair can be connected to the current sequence
        if newSeq.isExtendable(pair):
            newSeq.extend(pair)  # extend the sequence with the pair
            if checkSeq(newSeq):
                # if the sequence is valid
                possibleSeq.append(newSeq)
    return possibleSeq


def printPairs(pairList: list):
    # print the pairs
    for pair in pairList:
        print(str(pair))


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Find sequence of pairs that can be connected \
        so that the numbers resulted from the concatenation of the pairs are equal')

    parser.add_argument('--inputFile', '-f',
                        type=argparse.FileType('r'), help='input file')
    parser.add_argument('--max-itter', "-max-itter", type=int, help='maximum number of itterations, default is 10\n For the best performance \
        use the length of the sollution(if known) as the maximum number of itterations(matters only in DFS)')
    parser.add_argument('--algorithm', '-a', type=str, help='algorithm to use, default is BFS\n \
        Available algorithms: DFS, BFS,', default='BFS')
    parser.add_argument(
        "-d", "--debug", help="increase output verbosity", action="store_true")
    parser.add_argument('--outputFile', '-o',
                        type=argparse.FileType('w'), help='output file')
    parser.add_argument("--starting-sequence", "-starting-sequence",
                        type=argparse.FileType('r'), help="file containing the starting sequence(s)")
    return parser.parse_args()


def findSeqDFS(seq: Seq, pairList: list, itter: int) -> bool:
    # returns True if a valid sequence is found and False if not

    # if we have reached the maximum number of itterations => no solution
    if (itter > MAX_ITTER):
        return False

    #

    # get all possible pairs that can be connected to the current sequence
    possibleSeq = nextSeq(seq, pairList)

    # if there are no possible pairs => no solution
    if possibleSeq.__len__() == 0:
        return False

    for newSeq in possibleSeq:
        if DEBUG:
            print("Trying seq at itter " + str(itter))
            print(newSeq)

        # check if the sequence is complete
        if newSeq.topSeq.__len__() == newSeq.bottomSeq.__len__():
            if DEBUG:
                print("Found solution")
                print(newSeq)
            return True
        else:
            # if the sequence is not complete => continue
            if findSeqDFS(newSeq, pairList, itter+1):
                return True


def hasSequenceDFS(pairList: list, possibleSeq: list):
    for currentSeq in possibleSeq:
        if DEBUG:
            print("Start seq")
            print(currentSeq)
        # find the sequence of pairs that can be connected
        # start from itteration 1
        if findSeqDFS(currentSeq, pairList, 1):
            print("yes")
            return
    # if no sequence was found after MAX_ITTER itterations => no solution
    print("no")


def findSequenceBFS(pairList: list, possibleSeq: list, itter: int) -> bool:
    # returns True if a valid sequence is found and False if not

    if itter > MAX_ITTER:
        return False
    if possibleSeq.__len__() == 0:
        return False

    if DEBUG:
        print("Itter " + str(itter) + ":\n")

    nextPossibleSeq = []
    i = 1  # counter for the number of sequences
    for currentSeq in possibleSeq:
        if DEBUG:
            print("seq " + str(i))
            print(str(currentSeq))
        if currentSeq.topSeq.__len__() == currentSeq.bottomSeq.__len__():
            # if the sequence is complete => solution found
            if DEBUG:
                print("Found it")
                print(str(currentSeq))
            return True
        else:
            # if the sequence is not complete => continue
            nextPossibleSeq.extend(nextSeq(currentSeq, pairList))
        i += 1

    if findSequenceBFS(pairList, nextPossibleSeq, itter+1):
        return True


def hasSequenceBFS(pairList: list, possibleSeq: list):
    if findSequenceBFS(pairList, possibleSeq, 1):
        print("yes")
        return
    # if no sequence was found after MAX_ITTER itterations => no solution
    print("no")


def parseStartingSequence(line, pairList: list) -> Seq:
    # parse the starting sequence from a file
    # return a Seq object

    seq = Seq([], [], [])
    for pairID in line.split():
        pair = pairList[int(pairID) - 1]
        seq.extend(pair)
    return seq


def readSeqFromFile(file: argparse.FileType, pairList: list) -> list:
    # read the starting sequences from a file
    # return a list of sequences

    seqList = []
    lineNum = 0
    for line in file:
        lineNum += 1
        line = line.strip("[,]")
        if line == "":
            continue
        seq = parseStartingSequence(line, pairList)
        if checkSeq(seq):
            seqList.append(seq)
        else:
            print("Invalid starting sequence at line " + str(lineNum))
    print("")
    return seqList


def main():
    start_time = time.time()
    args = parseArgs()

    if args.max_itter:
        global MAX_ITTER
        MAX_ITTER = args.max_itter
    if args.debug:
        global DEBUG
        DEBUG = True

    if args.outputFile:
        sys.stdout = args.outputFile

    if args.inputFile:
        pairList = readPairs(args.inputFile)
    else:
        # read input
        filePath = input("Enter file path: ")
        inputFile = open(filePath, "r")
        pairList = readPairs(inputFile)
    if DEBUG:
        printPairs(pairList)

    # find all possible sequences that can start a sequence
    if args.starting_sequence:
        possibleSeq = readSeqFromFile(args.starting_sequence, pairList)
    else:
        possibleSeq = startSeq(pairList)
    if possibleSeq.__len__() == 0:
        print("no")
        return

    # select the algorithm
    if args.algorithm:
        if args.algorithm == "DFS":
            if DEBUG:
                print("Using DFS...\n")
            hasSequenceDFS(pairList, possibleSeq)
        elif args.algorithm == "BFS":
            if DEBUG:
                print("Using BFS...\n")
            hasSequenceBFS(pairList, possibleSeq)
        else:
            print("Invalid algorithm")
    if DEBUG:  # print the execution time
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
