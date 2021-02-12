import logging


class Properties:
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


if Properties.developmentMode:
    print("#######################")
    print("####### DEV MODE ######")
    print("#######################")
