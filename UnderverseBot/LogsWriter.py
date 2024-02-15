import os
import io
import datetime

class LogsWriter():

    def __init__(self):
        
        self.logsFilePath = ""
        self.criticalLogsFilePath = ""

        self.status = ["BOT","COMMAND","INFO","SUCCESS","ERROR"]
        self.niveau = 1
        self.niveauPrecedent = 1

        if os.path.exists(os.getcwd()+ "/other/logs.txt"):
            self.logsFilePath = os.getcwd()+ "/other/logs.txt"
        else:
            return False

        if os.path.exists(os.getcwd()+ "/other/critical_logs.txt"):
            self.criticalLogsFilePath = os.getcwd()+ "/other/critical_logs.txt"
        else:
            return False
        


    def addLog(self,niveau,status,message):
        logFile = io.open(self.logsFilePath,'a',encoding="utf-8")

        self.niveauPrecedent = self.niveau
        self.niveau = niveau
        msg = ""
        if self.niveau == 1:
            msg += "\n\n"
        if self.niveau < self.niveauPrecedent:
            
            msg += "\n"
        for i in range(self.niveau):
            msg += "\t"
        date = datetime.datetime.now()
        dateToDisplay = date.strftime("%d-%m-%Y %H:%M:%S")
        logFile.write(f"\n{msg}{dateToDisplay} [{status}]: {message}")

        logFile.close()
    

    def addCriticalLog(self,error):
        logFile = io.open(self.criticalLogsFilePath,'a', encoding='utf-8')

        date = datetime.datetime.now()
        dateToDisplay = date.strftime("%d-%m-%Y %H:%M:%S")
        logFile.write(f"\n{dateToDisplay} [ERROR]: {error}")

        logFile.close()

        

