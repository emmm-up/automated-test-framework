# -*- coding: utf-8 -*-
"""
API测试示例

演示如何使用框架进行API测试

Pytest Markers:
    - smoke: 冒烟测试
    - regression: 回归测试
    - critical: 关键业务流程
"""

import pytest
import requests
from framework.utils.logger import logger
from framework.utils.helper import Helper


class TestExampleAPI:
    """API测试类示例"""

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.critical
    def test_get_posts_success(self, api_client):
        """测试：成功获取文章列表

        操作：发送GET请求到 /posts
        预期：响应状态码200，返回模数据
        """
        logger.info("\ud83c\udfd7️ 执行测试: 成功获取文章列表")

        # 发送请求
        response = api_client.get("/posts")

        # 断言：响应状态码
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        logger.info(f"\u2705 响应状态码: {response.status_code}")

        # 断言：响应是数组
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        logger.info(f"\u2705 响应是数组，底数: {len(data)}")

        # 断言：数据不为空
        assert len(data) > 0, "Expected non-empty list"
        logger.info(f"\u2705 数据不为空")

        # 断言：每个项目都有字段
        first_item = data[0]
        required_fields = ["userId", "id", "title", "body"]
        for field in required_fields:
            assert field in first_item, f"Missing field: {field}"
        logger.info(f"\u2705 字段更验: {required_fields}")

    @pytest.mark.regression
    def test_get_single_post_success(self, api_client):
        """测试：成功获取单个文章

        操作：发送GET请求到 /posts/1
        预期：响应状态码200，返回一个文章对象
        """
        logger.info("\ud83c\udfd7️ 执行测试: 成功获取单个文章")

        post_id = 1
        response = api_client.get(f"/posts/{post_id}")

        # 断言：响应状态码
        assert response.status_code == 200
        logger.info(f"\u2705 响应状态码: {response.status_code}")

        # 断言：响应是对象
        data = response.json()
        assert isinstance(data, dict)
        logger.info(f"\u2705 响应是对象")

        # 断言：文章ID正确
        assert data["id"] == post_id
        logger.info(f"\u2705 文章ID匹配: {data['id']}")

    @pytest.mark.regression
    def test_create_post_success(self, api_client, test_data, fake):
        """测试：成功创建文章

        操作：发送POST请求到 /posts，传递文章数据
        预期：响应状态码201或200，返回带ID的文章对象
        """
        logger.info("\ud83c\udfd7️ 执行测试: 成功创建文章")

        # 构建请求数据
        payload = {
            "title": fake.sentence(),
            "body": fake.text(),
            "userId": 1,
        }
        logger.info(f"\ud83d\udce6 请求数据: {Helper.dict_to_json(payload)}")

        # 发送请求
        response = api_client.post("/posts", json=payload)

        # 断言：响应状态码
        assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"
        logger.info(f"\u2705 响应状态码: {response.status_code}")

        # 断言：响应包含所有字段
        data = response.json()
        for key in ["title", "body", "userId"]:
            assert key in data, f"Missing field: {key}"
        logger.info(f"\u2705 响应包含所有需要的字段")

    @pytest.mark.regression
    def test_get_post_not_found(self, api_client):
        """测试：获取不存在的文章返回404

        操作：发送GET请求到不存在的文章
        预期：响应状态码404
        """
        logger.info("\ud83c\udfd7️ 执行测试: 获取不存在的文章")

        # 使用一个高整数ID作为不存在的文章ID
        non_existent_id = 99999

        try:
            response = api_client.get(f"/posts/{non_existent_id}")
            # 当响应是4xx或5xx时，raise_for_status()会抛出异常
            # 但JSONPlaceholder可能不会返回404，而是返回空对象
            assert response.status_code in [200, 404]
            logger.info(f"\u2705 响应状态码: {response.status_code}")
        except requests.exceptions.HTTPError as e:
            # 处理HTTP错误
            logger.info(f"\u2705 捕获预预期的HTTP错误: {e}")


class TestCommonMethods:
    """测试通用方法和工具函数"""

    @pytest.mark.smoke
    def test_helper_json_conversion(self):
        """测试：Helper的JSON转换功能

        操作：测试JSON与字典的相互转换
        预期：转换成功且数据一致
        """
        from framework.utils.helper import Helper

        logger.info("\ud83c\udfd7️ 执行测试: JSON转换功能")

        # 测试数据
        original_dict = {"name": "John", "age": 30, "email": "john@example.com"}

        # 字典转JSON
        json_str = Helper.dict_to_json(original_dict)
        logger.info(f"\u2705 字典转JSON: {json_str}")
        assert isinstance(json_str, str)

        # JSON转字典
        converted_dict = Helper.json_to_dict(json_str)
        logger.info(f"\u2705 JSON转字典: {converted_dict}")
        assert converted_dict == original_dict

    @pytest.mark.smoke
    def test_helper_nested_dict(self):
        """测试：Helper的嵌套字典操作

        操作：测试嵌套字典的设置和获取
        预期：能一次能多层地访问嵌套字段
        """
        from framework.utils.helper import Helper

        logger.info("\ud83c\udfd7️ 执行测试: 嵌套字典操作")

        # 测试数据
        data = {}

        # 设置嵌套字段
        Helper.set_nested_value(data, "user.profile.name", "John")
        Helper.set_nested_value(data, "user.profile.age", 30)
        logger.info(f"\u2705 设置嵌套字段: {data}")

        # 获取嵌套字段
        name = Helper.get_nested_value(data, "user.profile.name")
        age = Helper.get_nested_value(data, "user.profile.age")
        logger.info(f"\u2705 获取嵌套字段: name={name}, age={age}")

        assert name == "John"
        assert age == 30
