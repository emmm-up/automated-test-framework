# -*- coding: utf-8 -*-
"""
配置管理模块

支持多环境配置切换（dev/test/stage/prod）
配置优先级：环境变量 > .env文件 > 默认值
"""

import os
from pathlib import Path
from typing import Optional, Any, Dict
from dotenv import load_dotenv


class Settings:
    """全局配置类"""

    # 加载.env文件
    _env_path = Path(__file__).parent.parent.parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)

    # ==================== 应用配置 ====================
    APP_ENV: str = os.getenv("APP_ENV", "test")
    """应用环境：dev/test/stage/prod"""

    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    """调试模式"""

    # ==================== API配置 ====================
    BASE_URL: str = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
    """API基础URL"""

    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    """API请求超时时间（秒）"""

    REQUEST_RETRIES: int = int(os.getenv("REQUEST_RETRIES", "3"))
    """请求重试次数"""

    # ==================== 日志配置 ====================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    """日志级别：DEBUG/INFO/WARNING/ERROR/CRITICAL"""

    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    """日志目录"""

    # 确保日志目录存在
    Path(LOG_DIR).mkdir(exist_ok=True)

    # ==================== 报告配置 ====================
    REPORT_DIR: str = os.getenv("REPORT_DIR", "allure-results")
    """报告目录"""

    ALLURE_ENABLED: bool = os.getenv("ALLURE_ENABLED", "true").lower() == "true"
    """是否启用Allure报告"""

    # 确保报告目录存在
    Path(REPORT_DIR).mkdir(exist_ok=True)

    # ==================== 测试数据配置 ====================
    TEST_DATA_PATH: str = os.getenv("TEST_DATA_PATH", "tests/data")
    """测试数据目录"""

    FAKE_SEED: int = int(os.getenv("FAKE_SEED", "42"))
    """Faker种子（用于数据生成的可重复性）"""

    # ==================== 认证配置 ====================
    API_KEY: Optional[str] = os.getenv("API_KEY")
    """API密钥"""

    API_SECRET: Optional[str] = os.getenv("API_SECRET")
    """API密钥"""

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        return getattr(cls, key, default)

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """转换为字典

        Returns:
            配置字典
        """
        return {k: v for k, v in vars(cls).items() if not k.startswith("_")}

    @classmethod
    def is_prod(cls) -> bool:
        """是否为生产环境"""
        return cls.APP_ENV == "prod"

    @classmethod
    def is_test(cls) -> bool:
        """是否为测试环境"""
        return cls.APP_ENV == "test"

    @classmethod
    def is_dev(cls) -> bool:
        """是否为开发环境"""
        return cls.APP_ENV == "dev"


if __name__ == "__main__":
    # 打印当前配置
    print("=" * 50)
    print("当前配置信息")
    print("=" * 50)
    for k, v in Settings.to_dict().items():
        print(f"{k}: {v}")
