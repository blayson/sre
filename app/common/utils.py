import logging


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('logs/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def propagate_args(common_args, resp):
    for key, val in common_args.items():
        if val is not None:
            resp[key] = val
    return resp
