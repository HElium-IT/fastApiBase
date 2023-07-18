# function that instantiates a logger object with the info, warning and error methods
# to be used in the tests

from functools import wraps
import logging
import os
import sys
import time


Logger = []


def get_file_logger(path=["logs", "test.log"]):
    try:
        return Logger[0]
    except IndexError:
        pass

    # create a logger object
    logger = logging.getLogger("file_logger")
    # set the logging level
    logger.setLevel(logging.INFO)

    # create the logs directory if it doesn't exist
    if not os.path.exists(os.path.join(*path)):
        os.mkdir(os.path.join(*path))

    # create a file in the logs directory with the name test.log (using path)
    open(os.path.join(*path), "w").close()

    # create a handler object that appends in a file /logs/test.log (using path)
    handler = logging.FileHandler(
        filename=os.path.join(*path)
    )
    # create a formatter object
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # set the formatter to the handler
    handler.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(handler)
    Logger.append(logger)
    return logger


# decorator that logs the function name and the arguments passed to it before calling it
# then logs the function name and the return value after the function is called
# also logs any exception that is raised


def file_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_file_logger()
        logger.info(
            f"Calling function {func.__name__} with args {args} and kwargs {kwargs}")
        initial_time = time.time()
        try:
            result = func(*args, **kwargs)
            final_time = time.time()
            logger.info(
                f"Function {func.__name__} took {final_time - initial_time} seconds to execute")
            logger.info(f"Function {func.__name__} returned {result}")
            return result
        except Exception as e:
            exception_time = time.time()
            logger.error(
                f"Function {func.__name__} took {exception_time - initial_time} seconds to raise an exception")
            logger.error(f"Function {func.__name__} raised an exception: {e}")
            raise e
    return wrapper
