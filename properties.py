import logging


class Properties:
    applicationVersion = '0.1.1'

    ##### DevMode ######
    developmentMode = False

    ##### Logging #####

    logLevel = logging.DEBUG
    dependenciesLogLevel = logging.WARN

    fileEncoding = "utf-8-sig"

    #####
    schema = ''
    dbname = ''
    user = ''
    password = ''
    host = ''
    port = ''
    filename = ''
    table = ''
    delimiter = ','

    filenamePattern = ''
    dropTableIfExists = False  # this is not a default value. It will always be replaced by the initializer
    castNumbers = False  # this is not a default value. It will always be replaced by the initializer

    batchSize = 30000


if Properties.developmentMode:
    print("#######################")
    print("####### DEV MODE ######")
    print("#######################")
