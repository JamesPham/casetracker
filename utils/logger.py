import os
import codecs
from datetime import datetime

class ConsoleLogger:
    def __init__(self, logFilePath):
        self.LogFile = None
        if logFilePath != '':
            os.path.normpath(logFilePath)
            self.LogFile = codecs.open(os.path.normpath(logFilePath), 'w', encoding = 'utf-8')
    
    def __del__(self):
        if self.LogFile != None:
            self.LogFile.close()
    
    def log(self, text):
        l = datetime.now().strftime("%Y/%m/%d, %H:%M:%S") + ' - ' + text
        print(l)
        if self.LogFile != None:
            self.LogFile.write(l + '\n')
      