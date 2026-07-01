# -*- coding: utf-8 -*-
"""
API客户端基类

提供统一的HTTP请求接口，支持:
- 多种HTTP方法（GET, POST, PUT, DELETE等）
- 自动重试机制
- 请求/响应日志记录
- 响应异常处理
- 请求头/参数/Body的统一管理
"""

import json
from typing import Dict, Any
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from framework.config.settings import Settings
from framework.utils.logger import logger


class APIClient:
    """API客户端

    Attributes:
        base_url: API基础URL
        timeout: 请求超时时间
        headers: 请求头
        session: 请求会话
    """

    def __init__(
        self,
        base_url: str = None,
        timeout: int = None,
        headers: Dict[str, str] = None,
    ):
        """初始化API客户端

        Args:
            base_url: API基础URL，默认使用Settings.BASE_URL
            timeout: 请求超时时间，默认使用Settings.API_TIMEOUT
            headers: 自定义请求头
        """
        self.base_url = base_url or Settings.BASE_URL
        self.timeout = timeout or Settings.API_TIMEOUT
        self.headers = headers or {"Content-Type": "application/json"}

        # 创建会话并配置重试策略
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """创建带重试策略的会话

        Returns:
            配置好重试策略的Session对象
        """
        session = requests.Session()

        # 配置重试策略
        retry_strategy = Retry(
            total=Settings.REQUEST_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _build_url(self, endpoint: str) -> str:
        """构建完整URL

        Args:
            endpoint: 端点路径

        Returns:
            完整URL
        """
        return urljoin(self.base_url, endpoint)

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """记录请求信息

        Args:
            method: HTTP方法
            url: 请求URL
            **kwargs: 其他参数
        """
        logger.info(f"📤 [{method.upper()}] {url}")
        if "params" in kwargs and kwargs["params"]:
            logger.debug(f"   Params: {kwargs['params']}")
        if "json" in kwargs and kwargs["json"]:
            logger.debug(f"   Body: {json.dumps(kwargs['json'], indent=2)}")
        if "data" in kwargs and kwargs["data"]:
            logger.debug(f"   Data: {kwargs['data']}")

    def _log_response(self, response: requests.Response) -> None:
        """记录响应信息

        Args:
            response: 响应对象
        """
        logger.info(f"📥 Status: {response.status_code}")
        try:
            logger.debug(f"   Response: {json.dumps(response.json(), indent=2)}")
        except (json.JSONDecodeError, ValueError):
            logger.debug(f"   Response: {response.text[:500]}")

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> requests.Response:
        """发送HTTP请求

        Args:
            method: HTTP方法
            endpoint: 端点路径
            **kwargs: 其他参数（params, json, data, headers等）

        Returns:
            响应对象

        Raises:
            requests.RequestException: 请求异常
        """
        url = self._build_url(endpoint)
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("headers", self.headers)

        self._log_request(method, url, **kwargs)

        try:
            response = self.session.request(method, url, **kwargs)
            self._log_response(response)
            response.raise_for_status()  # 如果状态码>=400，抛出异常
            return response
        except requests.RequestException as e:
            logger.error(f"❌ Request failed: {str(e)}")
            raise

    def get(
        self,
        endpoint: str,
        params: Dict[str, Any] = None,
        **kwargs,
    ) -> requests.Response:
        """发送GET请求

        Args:
            endpoint: 端点路径
            params: 查询参数
            **kwargs: 其他参数

        Returns:
            响应对象
        """
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(
        self,
        endpoint: str,
        data: Dict[str, Any] = None,
        json: Dict[str, Any] = None,
        **kwargs,
    ) -> requests.Response:
        """发送POST请求

        Args:
            endpoint: 端点路径
            data: 表单数据
            json: JSON数据
            **kwargs: 其他参数

        Returns:
            响应对象
        """
        return self._request("POST", endpoint, data=data, json=json, **kwargs)

    def put(
        self,
        endpoint: str,
        data: Dict[str, Any] = None,
        json: Dict[str, Any] = None,
        **kwargs,
    ) -> requests.Response:
        """发送PUT请求

        Args:
            endpoint: 端点路径
            data: 表单数据
            json: JSON数据
            **kwargs: 其他参数

        Returns:
            响应对象
        """
        return self._request("PUT", endpoint, data=data, json=json, **kwargs)

    def patch(
        self,
        endpoint: str,
        data: Dict[str, Any] = None,
        json: Dict[str, Any] = None,
        **kwargs,
    ) -> requests.Response:
        """发送PATCH请求

        Args:
            endpoint: 端点路径
            data: 表单数据
            json: JSON数据
            **kwargs: 其他参数

        Returns:
            响应对象
        """
        return self._request("PATCH", endpoint, data=data, json=json, **kwargs)

    def delete(
        self,
        endpoint: str,
        **kwargs,
    ) -> requests.Response:
        """发送DELETE请求

        Args:
            endpoint: 端点路径
            **kwargs: 其他参数

        Returns:
            响应对象
        """
        return self._request("DELETE", endpoint, **kwargs)

    def close(self) -> None:
        """关闭会话"""
        self.session.close()
        logger.info("✅ Session closed")
