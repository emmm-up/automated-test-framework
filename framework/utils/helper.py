# -*- coding: utf-8 -*-
"""
通用工具函数模块

提供常用的辅助函数
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta


class Helper:
    """通用工具函数集合"""

    @staticmethod
    def json_to_dict(json_str: str) -> Dict[str, Any]:
        """JSON字符串转字典

        Args:
            json_str: JSON字符串

        Returns:
            字典对象
        """
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

    @staticmethod
    def dict_to_json(data: Dict[str, Any], indent: int = 2) -> str:
        """字典转JSON字符串

        Args:
            data: 字典对象
            indent: JSON缩进

        Returns:
            JSON字符串
        """
        return json.dumps(data, indent=indent, ensure_ascii=False)

    @staticmethod
    def get_nested_value(data: Dict[str, Any], keys: str, separator: str = ".") -> Any:
        """获取嵌套字典的值

        Args:
            data: 字典对象
            keys: 键路径（如"user.name"）
            separator: 分隔符

        Returns:
            值

        Example:
            >>> data = {"user": {"name": "John"}}
            >>> Helper.get_nested_value(data, "user.name")
            "John"
        """
        for key in keys.split(separator):
            if isinstance(data, dict):
                data = data.get(key)
            else:
                return None
        return data

    @staticmethod
    def set_nested_value(
        data: Dict[str, Any],
        keys: str,
        value: Any,
        separator: str = ".",
    ) -> Dict[str, Any]:
        """设置嵌套字典的值

        Args:
            data: 字典对象
            keys: 键路径（如"user.name"）
            value: 值
            separator: 分隔符

        Returns:
            更新后的字典

        Example:
            >>> data = {}
            >>> Helper.set_nested_value(data, "user.name", "John")
            {"user": {"name": "John"}}
        """
        key_list = keys.split(separator)
        current = data

        for key in key_list[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[key_list[-1]] = value
        return data

    @staticmethod
    def list_to_dict(data: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
        """将列表转换为字典，使用指定字段作为键

        Args:
            data: 字典列表
            key: 用作键的字段

        Returns:
            字典对象

        Example:
            >>> data = [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
            >>> Helper.list_to_dict(data, "id")
            {1: {"id": 1, "name": "John"}, 2: {"id": 2, "name": "Jane"}}
        """
        return {item[key]: item for item in data if key in item}

    @staticmethod
    def get_time_delta(days: int = 0, hours: int = 0, minutes: int = 0) -> datetime:
        """获取相对于当前时间的时间差

        Args:
            days: 天数
            hours: 小时数
            minutes: 分钟数

        Returns:
            datetime对象
        """
        return datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)

    @staticmethod
    def format_time(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """格式化时间

        Args:
            dt: datetime对象
            fmt: 格式字符串

        Returns:
            格式化后的时间字符串
        """
        return dt.strftime(fmt)

    @staticmethod
    def is_contains(text: str, substrings: List[str], case_sensitive: bool = False) -> bool:
        """检查文本是否包含指定的任何子字符串

        Args:
            text: 文本
            substrings: 子字符串列表
            case_sensitive: 是否区分大小写

        Returns:
            是否包含
        """
        if not case_sensitive:
            text = text.lower()
            substrings = [s.lower() for s in substrings]

        return any(s in text for s in substrings)

    @staticmethod
    def dict_difference(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """比较两个字典的差异

        Args:
            dict1: 第一个字典
            dict2: 第二个字典

        Returns:
            差异字典 {"added": {}, "removed": {}, "modified": {}}
        """
        differences = {"added": {}, "removed": {}, "modified": {}}

        # 找出新增的键
        for key in dict2:
            if key not in dict1:
                differences["added"][key] = dict2[key]
            elif dict1[key] != dict2[key]:
                differences["modified"][key] = {"old": dict1[key], "new": dict2[key]}

        # 找出删除��键
        for key in dict1:
            if key not in dict2:
                differences["removed"][key] = dict1[key]

        return differences
