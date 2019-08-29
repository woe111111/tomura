import logging

from logging import _StderrHandler

import json
from logging import Logger
from tomura.config import Config

class CusLogger(Logger):

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs):

        if extra is not None:
            extra.update(**kwargs)
        else:
            extra = kwargs

        if extra != {}:
            msg = msg + " - extra : " + json.dumps(extra)
        super()._log(level, msg, args, exc_info=None, extra=extra, stack_info=False)


def get_logger(name, fmt=None, level=Config.LOGGER_LEVEL):
    logging.setLoggerClass(CusLogger)
    logger = logging.getLogger(name)

    for i in logger.handlers:
        logger.removeHandler(i)

    std = _StderrHandler()
    std.setLevel(level)

    if fmt == None:
        fmt = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(name)s - %(levelname)s: %(message)s")
    std.setFormatter(fmt)

    logger.addHandler(std)

    logger.setLevel(logging.DEBUG)

    return logger


if __name__ == '__main__':
    logger = get_logger("test")

    logger.info("test")
