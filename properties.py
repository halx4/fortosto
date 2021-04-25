import logging


class Properties:
    applicationVersion = '0.1.2'

    ##### DevMode ######
    developmentMode = False

    ##### Logging #####

    logLevel = logging.INFO
    dependenciesLogLevel = logging.WARN

    fileEncoding = "utf-8-sig"

    #####
    schema = ''
    dbname = ''
    user = ''
    password = ''
    host = ''
    port = ''
    target = ''
    table = ''
    delimiter = ','
    tableNamePrefix = ''
    primaryKey = ''

    filenamePattern = ''
    dropTableIfExists = False  # this is not a default value. It will always be replaced by the initializer
    castNumbers = False  # this is not a default value. It will always be replaced by the initializer
    verboseLogging = False

    batchSize = 30000


if Properties.developmentMode:
    print("#######################")
    print("####### DEV MODE ######")
    print("#######################")
