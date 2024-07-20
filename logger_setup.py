import asyncio
import logging
import functools
import os



# Configure the logging
def setup_logging():
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)  # Create the logs directory if it doesn't exist
    log_file_path = os.path.join(log_dir, 'log.log')

    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Set the logging format
        handlers=[
            logging.StreamHandler(),  # Log to console
            logging.FileHandler(log_file_path)  # Log to file
        ]
    )


def get_logger(name):
    setup_logging()
    return logging.getLogger(name)


# Logging decorator for fixtures
def log_fixture(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.info(f"Starting fixture: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Ending fixture: {func.__name__}")
        return result
    return wrapper


# Logging decorator for functions
def log_function(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"Starting function: {func.__name__}")
        result = func(*args, **kwargs)
        logger.debug(f"Ending function: {func.__name__}")
        return result
    return wrapper


def check_event_loop(func):
    logger = get_logger(func.__module__)
    try:
        loop = asyncio.get_event_loop()
        logger.debug(f"Existing event loop found: {loop}")
    except RuntimeError:
        logger.debug("No existing event loop")
