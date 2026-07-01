# -*- coding: utf-8 -*-
"""
自动化测试框架包
"""

__version__ = "1.0.0"
__author__ = "emmm-up"

from framework.config.settings import Settings
from framework.base.api_client import APIClient
from framework.utils.logger import logger

__all__ = ["Settings", "APIClient", "logger"]
