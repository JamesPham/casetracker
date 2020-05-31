
##########################################
# Case status client api class
##########################################

import os
import sys
import base64
import requests
from bs4 import BeautifulSoup


class ImmiStatusClient:
    
    def __init__(self):
        caseStatusUrlBase64 = 'aHR0cHM6Ly9lZ292LnVzY2lzLmdvdi9jYXNlc3RhdHVzL215Y2FzZXN0YXR1cy5kbw=='
        self.CaseStatusUrl = base64.b64decode(caseStatusUrlBase64)
        self.CaseStatusDivClass = 'appointment-sec'
        self.CaseStatusDivInnerClass = 'text-center'
        self.CaseTitleKey = 'title'
        self.CaseDescriptionKey = 'descr'
        
    
    ##########################################
    # Function to retrieve the raw status 
    # response
    ##########################################
    def getCaseStatusRaw(self, trackingNumber):
        try:
            # set request body
            caseStatusRequestBody = {'appReceiptNum': trackingNumber}
            # post request
            return requests.post(self.CaseStatusUrl, data = caseStatusRequestBody)
        except:
            return ''
        
        
    ##########################################
    # Function to retrieve the case status
    # data structure
    ##########################################
    def getCaseStatus(self, trackingNumber):
        try:
            # get raw status html
            rawStatusHtml = self.getCaseStatusRaw(trackingNumber)
            
            # parse raw status html
            soupRawHtml = BeautifulSoup(rawStatusHtml.text, "html.parser")
            
            # get status title
            statusTitle = soupRawHtml.find("div", {"class": self.CaseStatusDivClass}).find("div", {"class": self.CaseStatusDivInnerClass}).find('h1').text
            
            # get status description
            statusDescription = soupRawHtml.find("div", {"class": self.CaseStatusDivClass}).find("div", {"class": self.CaseStatusDivInnerClass}).find('p').text
            
            return { self.CaseTitleKey: statusTitle, self.CaseDescriptionKey: statusDescription }
              
        except:
            return None
