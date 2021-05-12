import logging
from ..properties import Properties

# CRITICAL	50
# ERROR		40
# WARNING	30
# INFO		20
# DEBUG		10
# TRACE     7 (custom)
# NOTSET	0

# log.trace('This is a trace message')
# log.debug('This is a debug message')
# log.info('This is an info message')
# log.warning('This is a warning message')
# log.error('This is an error message')
# log.critical('This is a critical message')

VERBOSE_LOG_LEVEL=5

logger = logging.getLogger()


def getRootLogger():
    return logger


def setLevel(newLevel):
    logger.debug("Log level set to: " + str(Properties.logLevel))
    logging.basicConfig(level=newLevel, format='%(asctime)s %(levelname)-8s %(message)s')
    logger.setLevel(newLevel)


# custom logging levels
TRACE_LOG_LEVEL = 7
logging.addLevelName(TRACE_LOG_LEVEL, "TRACE")
def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LOG_LEVEL):
        self._log(TRACE_LOG_LEVEL, message, args, **kws)
logging.Logger.trace = trace
######

setLevel(Properties.logLevel)


logging.getLogger('boto3').setLevel(Properties.dependenciesLogLevel)
logging.getLogger('botocore').setLevel(Properties.dependenciesLogLevel)
logging.getLogger('s3transfer').setLevel(Properties.dependenciesLogLevel)
logging.getLogger('urllib3').setLevel(Properties.dependenciesLogLevel)
