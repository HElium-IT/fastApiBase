# function that instantiates a logger object with the info, warning and error methods
# to be used in the tests

from functools import wraps
import logging
import os
import time

from app.core.config import settings


logger = None


def get_logger(path=["logs", "test.log"]):
    global logger
    if logger is not None:
        return logger

    # create a logger object
    logger = logging.getLogger("file_logger")
    # set the logging level reading the LOG_LEVEL environment variable string
    logger.setLevel(
        getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    )

    # create the logs directory if it doesn't exist
    if not os.path.exists(os.path.dirname(os.path.join(*path))):
        os.makedirs(os.path.dirname(os.path.join(*path)))

    # create the log file if it doesn't exist
    if not os.path.exists(os.path.join(*path)):
        open(os.path.join(*path), "w").close()

    # create a handler object that appends to the log file
    handler = logging.FileHandler(
        filename=os.path.join(*path),
        mode="a",
    )
    # create a formatter object
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s")
    # set the formatter to the handler
    handler.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(handler)

    return logger


# decorator that logs the function name and the arguments passed to it before calling it
# then logs the function name and the return value after the function is called
# also logs any exception that is raised


def log(func, print_timing=True, print_input=True, print_output=True):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger = get_logger()
        if print_input:
            to_print_args = [arg.__dict__ if hasattr(
                arg, "__dict__") else arg for arg in args]
            to_print_kwargs = {k: v.__dict__ if hasattr(
                v, "__dict__") else v for k, v in kwargs.items()}
        logger.info(
            f"[{func.__name__}] called" + f" with arguments {to_print_args} and keyword arguments {to_print_kwargs}" if print_input else "")
        if print_timing:
            initial_time = time.time()
        try:
            result = await func(*args, **kwargs)
            if print_timing:
                final_time = time.time()
                logger.info(
                    f"[{func.__name__}] took {final_time - initial_time} seconds to execute")
            if print_output:
                if hasattr(result, "__dict__"):
                    to_print_result = result.__dict__
                else:
                    to_print_result = result
                logger.info(f"[{func.__name__}] returned {to_print_result}")
            logger.info(f"[{func.__name__}] finished")
            return result
        except Exception as e:
            exception_time = time.time()
            if print_timing:
                logger.error(
                    f"[{func.__name__}] took {exception_time - initial_time} seconds to raise an exception")
            logger.error(f"[{func.__name__}] raised an exception: {e}")
            raise e
    return wrapper
