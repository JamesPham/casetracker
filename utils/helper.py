import os
import codecs

##########################################
# Function to read tsv file and store in
# dictionary
##########################################
def readTsvToDict(filePath, keyCol):
    dictLines = {}
    with codecs.open(os.path.normpath(filePath), 'r', encoding = 'utf-8') as f:
        allLines = f.read().splitlines()
        for line in allLines:
            lineParts = line.split('\t')
            if len(lineParts) > keyCol:
                if not lineParts[keyCol] in dictLines:
                    dictLines[lineParts[keyCol]] = line
    return dictLines


##########################################
# Function to get tsv line element by
# column number
##########################################
def getTsvElement(tsvLine, colNbr):
    el = ''
    lineParts = tsvLine.split('\t')
    if len(lineParts) >= colNbr:
        el = lineParts[colNbr]
    return el


##########################################
# Function to create a folder given 
# a full path
##########################################
def createDirIfNotExist(fullPath):
    directory = os.path.dirname(fullPath)
    if not os.path.exists(directory):
        os.makedirs(directory)
