# 自动化测试 (Automated Test Framework)

完整的Python自动化测试框架搭建示例，涵盖 **技术选型、环境部署、CI/CD集成** 三个核心阶段。

## 🎯 项目目标

- ✅ **框架搭建**：基于Pytest的可复用自动化测试框架
- ✅ **最佳实践**：展示API测试、配置管理、报告生成的最佳实践
- ✅ **CI/CD集成**：GitHub Actions完整工作流配置
- ✅ **容器化部署**：Docker + Docker-Compose支持
- ✅ **文档完善**：详细的技术选型、部署、任务分解文档

## 🏗️ 项目结构

```
automated-test-framework/
├── docs/                          # 文档
│   ├── 技术选型方案.md
│   ├── 环境部署指南.md
│   ├── CI_CD集成实践.md
│   └── 项目任务分解.md
├── framework/                     # 核心框架
│   ├── config/
│   │   └── settings.py           # 配置管理
│   ├── base/
│   │   └── api_client.py         # API客户端基类
│   ├── utils/
│   │   ├── logger.py             # 日志工具
│   │   └── helper.py             # 通用工具函数
│   └── __init__.py
├── tests/                         # 测试用例
│   ├── api/
│   │   ├── test_example_api.py   # API测试示例
│   │   ├── conftest.py           # fixtures配置
│   │   └── __init__.py
│   └── __init__.py
├── docker/                        # Docker配置
│   ├── Dockerfile
│   └── docker-compose.yml
├── .github/workflows/             # GitHub Actions
│   └── tests.yml
├── requirements.txt               # Python依赖
├── setup.py                       # 项目配置
├── pytest.ini                     # Pytest配置
├── .env.example                   # 环境变量模板
└── .gitignore                     # Git忽略文件
```

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/emmm-up/automated-test-framework.git
cd automated-test-framework
```

### 2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的测试环境配置
```

### 5. 本地运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/api/test_example_api.py

# 生成Allure报告
pytest --alluredir=allure-results
allure serve allure-results
```

### 6. 使用Docker运行
```bash
# 构建镜像
docker build -f docker/Dockerfile -t auto-test-framework .

# 或使用docker-compose
docker-compose -f docker/docker-compose.yml up
```

## 📚 文档指南

| 文档 | 说明 |
|------|------|
| [技术选型方案](docs/技术选型方案.md) | 框架、语言、工具的选型依据与对比 |
| [环境部署指南](docs/环境部署指南.md) | 本地、Docker、云环境的部署步骤 |
| [CI/CD集成实践](docs/CI_CD集成实践.md) | GitHub Actions工作流详解与最佳实践 |
| [项目任务分解](docs/项目任务分解.md) | 详细的开发任务清单与时间估算 |

## 🛠️ 核心依赖

- **pytest** - 测试框架
- **requests** - HTTP客户端
- **pytest-allure** - 报告生成
- **python-dotenv** - 环境变量管理
- **faker** - 测试数据生成
- **pytest-xdist** - 分布式测试

## 📊 项目进度

- [x] 第一阶段：技术选型 + 环境部署
- [x] 第二阶段：框架核心能力
- [x] 第三阶段：CI/CD集成
- [ ] 持续完善与优化

## 🔄 CI/CD工作流

项目已配置GitHub Actions，每次提交代码时自动执行：

```
代码提交 → 环境搭建 → 运行测试 → 生成报告 → 失败通知
```

具体配置见 `.github/workflows/tests.yml`

## 💬 反馈与贡献

欢迎提issue或PR来改进本项目！

## 📝 License

MIT License

---

**更新日期**：2024年
**作者**：emmm-up
