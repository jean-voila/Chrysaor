import StudentLogging
import json

class PegasusData():
    def __init__(self):
        self.success = False
        self.cookie  = ""
        self.name    = ""

    def __GetData__(self, credentialFile="data/credentials", cookieFile="data/cookie", verboseOutput=True):
        loggingData = StudentLogging.log(credentialFile, cookieFile, verboseOutput)
        self.success = bool(loggingData["success"])
        self.cookie  = loggingData["cookie"]
        self.name    = loggingData["name"]


studentData = PegasusData()
studentData.__GetData__()






