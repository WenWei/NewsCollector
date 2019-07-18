import os
import logging
import logging.handlers
import errno

project_name = 'NewsCollector'

def init():
    logPath = os.getenv(project_name + 'LogPath', '/var/log/'+project_name)
    logLevel = getLogLevel()
    fileName = project_name

    try:
        if not os.path.exists(logPath):
            os.makedirs(logPath, exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    logging.basicConfig(
    level=logLevel,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        # logging.FileHandler("{0}/{1}.log".format(logPath, fileName)),
        logging.handlers.TimedRotatingFileHandler(
            filename= "{0}/{1}.log".format(logPath, fileName),
            when='d',
            interval= 1,
            backupCount=5),
        logging.StreamHandler()
    ])
    logger = logging.getLogger()
    logger.info('Logger initialized.')

def getLogLevel():
    logLevel = os.getenv(project_name + 'LogLevel', 'info').upper()
    if logLevel == 'CRITICAL':
        return logging.CRITICAL
    if logLevel == 'ERROR':
        return logging.ERROR
    if logLevel == 'WARNING':
        return logging.WARNING
    if logLevel == 'INFO':
        return logging.INFO
    if logLevel == 'DEBUG':
        return logging.DEBUG
    return logging.INFO

if __name__ == '__main__':
    init()