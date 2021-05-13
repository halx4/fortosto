import logging


class Properties:
    applicationVersion = '1.1.0' #keep here

    ##### DevMode ######
    developmentMode = False #keep here

    ##### Logging #####

    logLevel = logging.INFO #keep here
    dependenciesLogLevel = logging.WARN #keep here

    fileEncoding = "utf-8-sig" #keep here

    verboseLogging = False #keep here

    batchSize = 30000 #keep here

    jsonlFileExtensions = {'.jsonl'} #keep here


if Properties.developmentMode:
    print("#######################")
    print("####### DEV MODE ######")
    print("#######################")
