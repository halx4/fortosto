import logging


class Properties:
    ##### DevMode ######
    developmentMode = False

    ##### Logging #####

    logLevel = logging.DEBUG
    dependenciesLogLevel = logging.WARN

    delimiter = ','
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


if Properties.developmentMode:
    print("#######################")
    print("####### DEV MODE ######")
    print("#######################")
