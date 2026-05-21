import logging
import os


class LogGen:

    @staticmethod
    def loggen():

        log_dir = "logs"

        os.makedirs(
            log_dir,
            exist_ok=True
        )

        logger = logging.getLogger()

        logger.setLevel(
            logging.INFO
        )

        # Prevent duplicate handlers
        if logger.hasHandlers():
            logger.handlers.clear()

        log_file = os.path.join(
            log_dir,
            "automation.log"
        )

        # =========================
        # LOG FORMAT
        # =========================

        formatter = logging.Formatter(
            fmt=
            "%(asctime)s | "
            "%(levelname)s | "
            "%(filename)s:%(lineno)d | "
            "%(message)s",

            datefmt=
            "%Y-%m-%d %H:%M:%S"
        )

        # =========================
        # FILE HANDLER
        # =========================

        file_handler = logging.FileHandler(
            log_file,
            mode="a",
            encoding="utf-8"
        )

        file_handler.setFormatter(
            formatter
        )

        logger.addHandler(
            file_handler
        )

        return logger