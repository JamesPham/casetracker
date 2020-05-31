
##########################################
# Case status crawler class
##########################################

import os
import sys
sys.path.insert(1, '../utils')

import time
import codecs
import requests
from logger import *
from ImmiStatusClient import *
from helper import readTsvToDict, getTsvElement, createDirIfNotExist


class ImmiStatusCrawler:
    
    def __init__(self, logger):
        self.MaxCases = 20000
        self.MaxSequentialCases = 500
        self.CaseTitleKey = 'title'
        self.CaseDescriptionKey = 'descr'
        self.SuffixSize = 4
        self.TimeSleepBetweenRequests = 0.100
        self.MaxSeqEmptyResCount = 10
        self.Logger = logger
        
    
    ##########################################
    # Function to retrieve status cases
    ##########################################
    def retrieveCases(self, casesFile, outputFile):
        self.searchCases('', casesFile, 1, outputFile)
    
    
    ##########################################
    # Function to compare status cases
    ##########################################
    def compareCases(self, controlCasesFile, treatmentCasesFile):
        # read control file
        controlLines = readTsvToDict(controlCasesFile, 0)
        # if no treatment file, retrieve from server
        if treatmentCasesFile == '':
            treatmentCaseNumbers = controlLines.keys()
            treatmentCases = self.searchCasesAll('', treatmentCaseNumbers, 1)
            treatmentLines = { el.split('\t')[0] : el for el in treatmentCases }
        else:
            treatmentLines = readTsvToDict(treatmentCasesFile, 0)
        # compare control and treatment
        self.Logger.log("=============== Updates found ===============")
        diffCount = 0
        for ck, cv in treatmentLines.items():
            if ck in controlLines:
                treatmentStatus = getTsvElement(cv, 1)
                controlStatus = getTsvElement(controlLines[ck], 1)
                if treatmentStatus != controlStatus:
                    diffCount += 1
                    self.Logger.log(ck + '\t' + controlStatus + '\t--->\t' + treatmentStatus)
        if diffCount == 0:
            self.Logger.log("No update found")
    
    ##########################################
    # Function to search for status cases
    # given list of all cases
    ##########################################
    def searchCasesAll(self, searchMatch, caseNumbers, numCases):
        allCases = []
        reqCounter = 0
        # instanciate immigration status client
        immiStatusClient = ImmiStatusClient()
        # process file line by line
        for line in caseNumbers:
            # read seed case number line
            lineParts = line.split('\t')
            if len(lineParts) > 0 and lineParts[0] != '':
                emptyResponseCounter = 0
                # the seed case number is located at column 0
                caseNumber = lineParts[0]
                # extract integer number from seed case number
                caseNumberPrefix = caseNumber[:-self.SuffixSize]
                caseNumberSuffix = caseNumber[-self.SuffixSize:]
                startNumberSuffix = int(caseNumberSuffix)
                # search all case numbers following the seed number
                for i in range(startNumberSuffix, startNumberSuffix + min(numCases, self.MaxSequentialCases)):
                    # reconstruct case number
                    currentCaseNumber = caseNumberPrefix + str(i).zfill(self.SuffixSize)
                    if reqCounter <= self.MaxCases:
                        # pause not to send too frequent requests to server
                        time.sleep(self.TimeSleepBetweenRequests)
                        # request case status
                        currentCase = immiStatusClient.getCaseStatus(currentCaseNumber)
                        self.Logger.log("Retrieved status information: " + currentCaseNumber)
                        reqCounter += 1
                        if currentCase != None and self.CaseTitleKey in currentCase and self.CaseDescriptionKey in currentCase:
                            # searching condition
                            if searchMatch == '':
                                allCases.append(currentCaseNumber + '\t' + currentCase[self.CaseTitleKey] + '\t' + currentCase[self.CaseDescriptionKey])
                            elif currentCase[self.CaseTitleKey].lower().find(searchMatch.lower()) != -1 or currentCase[self.CaseDescriptionKey].lower().find(searchMatch.lower()) != -1:
                                allCases.append(currentCaseNumber + '\t' + currentCase[self.CaseTitleKey] + '\t' + currentCase[self.CaseDescriptionKey])
                            # increment empty response counter
                            if currentCase[self.CaseTitleKey] == '' and currentCase[self.CaseDescriptionKey] == '':
                                emptyResponseCounter += 1
                            else:
                                emptyResponseCounter = 0
                            # check if max empty response reached
                            if emptyResponseCounter >= self.MaxSeqEmptyResCount:
                                self.Logger.log("Maximum number of empty responses reached. Stopping case search...")
                                break
                    else:
                        self.Logger.log("Maximum number of requests reached. Stopping case search...")
                        break
        return allCases
    
    ##########################################
    # Function to search for status cases
    # given a file with all cases
    ##########################################
    def searchCases(self, searchMatch, seedCasesFile, numCases, outputFile):
        allCases = []
        # open seed cases file
        with codecs.open(os.path.normpath(seedCasesFile), 'r', encoding = 'utf-8') as f:
            reqCounter = 0
            # read all file lines
            allLines = f.read().splitlines()
            # get cases status
            allCases = self.searchCasesAll(searchMatch, allLines, numCases)
        
        # save all cases to output file
        createDirIfNotExist(os.path.normpath(outputFile))
        with codecs.open(os.path.normpath(outputFile), 'w', encoding = 'utf-8') as f:
            for case in allCases:
                f.write(case + '\n')
        self.Logger.log("Cases and their status were successfuly saved to: " + os.path.normpath(outputFile))
