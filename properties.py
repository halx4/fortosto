import logging


class Properties:
    applicationVersion = '1.0.0' #keep here

    ##### DevMode ######
    developmentMode = False #keep here

    ##### Logging #####

    logLevel = logging.INFO #keep here
    dependenciesLogLevel = logging.WARN #keep here

    fileEncoding = "utf-8-sig" #keep here

    # #####
    # schema = ''
    # dbname = ''
    # user = ''
    # password = ''
    # host = ''
    # port = ''
    # target = ''
    # table = ''
    # delimiter = ','
    # tableNamePrefix = ''
    # primaryKey = ''
    #
    # filenamePattern = ''
    # dropTableIfExists = False  # this is not a default value. It will always be replaced by the initializer
    # castNumbers = False  # this is not a default value. It will always be replaced by the initializer


    verboseLogging = False #keep here

    batchSize = 30000 #keep here

    jsonlFileExtensions = {'.jsonl'} #keep here


if Properties.developmentMode:
    print("#######################")
    print("####### DEV MODE ######")
    print("#######################")
