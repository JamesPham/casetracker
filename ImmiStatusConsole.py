import os
import sys
sys.path.insert(1, './lib')
sys.path.insert(1, './utils')

from ImmiStatusCrawler import *
from configparser import ConfigParser


def run():
    if len(sys.argv) >= 2:
        # read config
        config = ConfigParser()
        config.read(sys.argv[1])
        logFile = ''
        if config.has_section('General') and \
           config.has_option('General', 'LogFile'):
            logFile = config.get('General', 'LogFile')
        
        # instanciate logger
        consoleLogger = ConsoleLogger(logFile)
        
        # instanciate case status tracker
        immiStatusCrawler = ImmiStatusCrawler(consoleLogger)
    
        if config.has_section('SearchCases'):
            consoleLogger.log("Run process in SearchCases mode")
            if config.has_option('SearchCases', 'SeedCasesFilePath') and \
               config.has_option('SearchCases', 'NumberSequentialCases') and \
               config.has_option('SearchCases', 'OutputFilePath'):
                # set search cases variables
                seedCasesFilePath = config.get('SearchCases', 'SeedCasesFilePath')
                numCases = config.getint('SearchCases', 'NumberSequentialCases')
                outputFilePath = config.get('SearchCases', 'OutputFilePath')
                searchMatch = ''
                if config.has_option('SearchCases', 'SearchMatch'):
                    searchMatch = config.get('SearchCases', 'SearchMatch')
                    consoleLogger.log("SearchCases - SearchMatch = " + searchMatch)
                # print params
                consoleLogger.log("SearchCases - SeedCasesFilePath = " + seedCasesFilePath)
                consoleLogger.log("SearchCases - NumberSequentialCases = " + str(numCases))
                consoleLogger.log("SearchCases - OutputFilePath = " + outputFilePath)
                # search cases
                immiStatusCrawler.searchCases(searchMatch, seedCasesFilePath, numCases, outputFilePath)
            else:
                consoleLogger.log("Error in config: SearchCases section should contain the \
                                  following parameters: 'SeedCases', 'NumberSequentialCases' \
                                      and 'OutputFilePath'")
    
        if config.has_section('RetrieveCases'):
            consoleLogger.log("Run process in RetrieveCases mode")
            if config.has_option('RetrieveCases', 'CasesFilePath') and \
               config.has_option('RetrieveCases', 'OutputFilePath'):
                # set retrieve cases variables
                casesFilePath = config.get('RetrieveCases', 'CasesFilePath')
                outputFilePath = config.get('RetrieveCases', 'OutputFilePath')
                # print params
                consoleLogger.log("RetrieveCases - CasesFilePath = " + casesFilePath)
                consoleLogger.log("RetrieveCases - OutputFilePath = " + outputFilePath)
                # retrieve cases
                immiStatusCrawler.retrieveCases(casesFilePath, outputFilePath)
            else:
                consoleLogger.log("Error in config: RetrieveCases section should contain the \
                                  following parameters: 'CasesFilePath', and 'OutputFilePath'")
                                  
        if config.has_section('CompareCases'):
            consoleLogger.log("Run process in CompareCases mode")
            if config.has_option('CompareCases', 'ControlCasesFile'):
                # set compare cases variables
                controlCasesFile = config.get('CompareCases', 'ControlCasesFile')
                consoleLogger.log("CompareCases - ControlCasesFile = " + controlCasesFile)
                treatmentCasesFile = ''
                if config.has_option('CompareCases', 'TreatmentCasesFile'):
                    treatmentCasesFile = config.get('CompareCases', 'TreatmentCasesFile')
                    consoleLogger.log("CompareCases - TreatmentCasesFile = " + treatmentCasesFile)
                # compare cases
                immiStatusCrawler.compareCases(controlCasesFile, treatmentCasesFile)
            else:
                consoleLogger.log("Error in config: CompareCases section should contain the \
                                  following parameters: 'ControlCasesFile'")
  
    
if __name__ == "__main__":
    run()