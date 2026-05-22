import logging
import os
from pathlib import Path


class LogGen:

    @staticmethod
    def loggen():

        project_root = Path(__file__).resolve().parents[1]

        log_dir = project_root / "logs"

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
