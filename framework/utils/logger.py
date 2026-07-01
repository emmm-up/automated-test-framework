# -*- coding: utf-8 -*-
"""
日志工具模块

使用loguru进行日志管理，提供彩色输出和文件记录
"""

import sys
from pathlib import Path
from loguru import logger as _logger

from framework.config.settings import Settings

# 移除默认处理器
_logger.remove()

# 配置控制台输出
_logger.add(
    sys.stdout,
    level=Settings.LOG_LEVEL,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
)

# 配置文件输出
log_file = Path(Settings.LOG_DIR) / "test_{time:YYYY-MM-DD_HH-mm-ss}.log"
_logger.add(
    str(log_file),
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="500 MB",  # 文件大小达到500MB时轮换
    retention="7 days",  # 保留7天的日志
)

logger = _logger

if __name__ == "__main__":
    # 测试日志
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
