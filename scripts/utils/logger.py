# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: logger.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — LOGGER v1.0                        ║
║   Structured Logging for FGSS Production Pipeline            ║
╚══════════════════════════════════════════════════════════════╝
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

try:
    from paths import BASE_DIR
except ImportError:
    BASE_DIR = Path(__file__).resolve().parents[2]

# 1. Configuration
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 2. Formatter
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_logger(name: str):
    """Returns a configured logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        # Console Handler
        c_handler = logging.StreamHandler(sys.stdout)
        c_handler.setLevel(logging.INFO)
        c_format = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)
        
        # File Handler (Daily)
        log_file = LOG_DIR / f"fgss_{datetime.now().strftime('%Y%m%d')}.log"
        f_handler = logging.FileHandler(log_file, encoding='utf-8')
        f_handler.setLevel(logging.DEBUG)
        f_format = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)
        
    return logger

if __name__ == "__main__":
    test_log = get_logger("LOG_TEST")
    test_log.info("FGSS Logging System Initialized.")
    test_log.debug("Debug mode is active.")
