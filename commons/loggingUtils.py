import logging
from properties import Properties

# CRITICAL	50
# ERROR		40
# WARNING	30
# INFO		20
# DEBUG		10
# NOTSET	0

# log.debug('This is a debug message')
# log.info('This is an info message')
# log.warning('This is a warning message')
# log.error('This is an error message')
# log.critical('This is a critical message')

logger = logging.getLogger()


def getRootLogger():
    return logger


def setLevel(newLevel):
    logger.debug("Log level set to: " + str(Properties.logLevel))
    logging.basicConfig(level=newLevel, format='%(asctime)s %(levelname)-8s %(message)s')
    logger.setLevel(newLevel)


setLevel(Properties.logLevel)



logging.getLogger('boto3').setLevel(Properties.dependenciesLogLevel)
logging.getLogger('botocore').setLevel(Properties.dependenciesLogLevel)
logging.getLogger('s3transfer').setLevel(Properties.dependenciesLogLevel)
logging.getLogger('urllib3').setLevel(Properties.dependenciesLogLevel)


def logLambdaInvocation(event, context):
    headers = event['headers']

    logger.info("invoked lambda: " + str(context.function_name) + " - version: " + str(context.function_version))
    logger.info("with headers: " + str(headers))
