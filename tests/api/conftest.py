# -*- coding: utf-8 -*-
"""
Pytest Fixtures配置

提供公共的测试fixtures，所有测试用例可以使用
"""

import pytest
from faker import Faker

from framework.base.api_client import APIClient
from framework.config.settings import Settings
from framework.utils.logger import logger


@pytest.fixture(scope="session")
def fake():
    """提供全局Faker实例，用于生成测试数据

    Returns:
        Faker实例
    """
    return Faker()


@pytest.fixture(scope="function")
def api_client():
    """提供API客户端实例

    不同环境自动使用不同配置

    Yields:
        APIClient实例
    """
    logger.info(f"\ud83d\udd9c Setting up API client for {Settings.APP_ENV} environment")
    client = APIClient()
    yield client
    client.close()
    logger.info("\ud83d\uded1 Tearing down API client")


@pytest.fixture(scope="function")
def test_data():
    """提供测试数据

    Returns:
        测试数据字典
    """
    data = {
        "user": {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
        },
        "product": {
            "id": 101,
            "name": "Test Product",
            "price": 99.99,
            "stock": 100,
        },
    }
    return data


@pytest.fixture(scope="function")
def config():
    """提供配置信息

    Returns:
        Settings对象
    """
    return Settings
