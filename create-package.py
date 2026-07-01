#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化测试框架 - 项目打包脚本

功能：
  - 自动打包项目为ZIP文件
  - 生成文件校验和（MD5/SHA256）
  - 创建打包日志
  - 支持排除指定目录/文件

使用方式：
  python3 create-package.py [output_dir]

示例：
  python3 create-package.py ./dist
  python3 create-package.py /home/user/packages
"""

import os
import sys
import shutil
import zipfile
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Tuple


class Colors:
    """ANSI颜色常量"""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


class PackageCreator:
    """项目打包器"""

    def __init__(self, project_root: str = ".", output_dir: str = "."):
        self.project_root = Path(project_root).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成带时间戳的包名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.package_name = f"automated-test-framework_{timestamp}"
        self.zip_path = self.output_dir / f"{self.package_name}.zip"
        self.log_file = self.output_dir / f"{self.package_name}_log.txt"
        self.md5_file = self.output_dir / f"{self.package_name}.zip.md5"
        self.sha256_file = self.output_dir / f"{self.package_name}.zip.sha256"
        
        self.logs = []
        self.excluded_items = {
            "__pycache__",
            ".git",
            ".pytest_cache",
            ".idea",
            ".vscode",
            "venv",
            "env",
            ".env",
            "dist",
            "build",
            "*.egg-info",
            ".DS_Store",
            "allure-results",
            "htmlcov",
            "logs",
        }

    def log(self, message: str, level: str = "INFO") -> None:
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if level == "INFO":
            color = Colors.CYAN
            prefix = "[INFO]"
        elif level == "SUCCESS":
            color = Colors.GREEN
            prefix = "[✓]"
        elif level == "ERROR":
            color = Colors.RED
            prefix = "[✗]"
        elif level == "WARN":
            color = Colors.YELLOW
            prefix = "[!]"
        else:
            color = Colors.ENDC
            prefix = "[LOG]"

        log_line = f"{timestamp} {prefix} {message}"
        print(f"{color}{log_line}{Colors.ENDC}")
        self.logs.append(log_line)

    def _should_exclude(self, path: Path) -> bool:
        """检查路径是否应被排除"""
        # 检查目录名
        if path.name in self.excluded_items:
            return True
        
        # 检查隐藏文件（以点开头）
        if path.name.startswith(".") and path.name not in {".env.example", ".gitignore"}:
            return True
        
        # 检查.log文件
        if path.suffix == ".log":
            return True
            
        return False

    def create_package(self) -> bool:
        """创建项目包"""
        self.log("="*70, "INFO")
        self.log("🚀 开始创建项目包", "INFO")
        self.log("="*70, "INFO")
        self.log(f"项目路径: {self.project_root}", "INFO")
        self.log(f"输出目录: {self.output_dir}", "INFO")
        self.log(f"包名: {self.package_name}", "INFO")
        self.log("", "INFO")

        try:
            # 创建ZIP文件
            self.log("📦 创建ZIP文件...", "INFO")
            file_count = self._create_zip()
            self.log(f"✓ 已添加 {file_count} 个文件到ZIP", "SUCCESS")
            
            # 计算文件大小
            file_size = self.zip_path.stat().st_size
            size_mb = file_size / (1024 * 1024)
            self.log(f"✓ 文件大小: {size_mb:.2f} MB", "SUCCESS")
            self.log("", "INFO")

            # 计算校验和
            self.log("🔐 计算校验和...", "INFO")
            md5_hash = self._calculate_hash("md5")
            sha256_hash = self._calculate_hash("sha256")
            self.log(f"✓ MD5: {md5_hash}", "SUCCESS")
            self.log(f"✓ SHA256: {sha256_hash}", "SUCCESS")
            
            # 保存校验和
            self._save_checksums(md5_hash, sha256_hash)
            self.log("", "INFO")

            # 保存日志
            self.log("💾 保存日志文件...", "INFO")
            self._save_logs()
            
            # 打印摘要
            self._print_summary(file_count, size_mb, md5_hash)
            
            return True

        except Exception as e:
            self.log(f"打包失败: {str(e)}", "ERROR")
            self._save_logs()
            return False

    def _create_zip(self) -> int:
        """创建ZIP文件"""
        file_count = 0
        
        with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(self.project_root):
                # 移除被排除的目录
                dirs[:] = [d for d in dirs if not self._should_exclude(Path(root) / d)]
                
                # 添加文件
                for file in files:
                    file_path = Path(root) / file
                    
                    if self._should_exclude(file_path):
                        continue
                    
                    # 计算相对路径（用于ZIP内的路径）
                    arcname = file_path.relative_to(self.project_root.parent)
                    
                    try:
                        zf.write(file_path, arcname)
                        file_count += 1
                    except Exception as e:
                        self.log(f"⚠️ 无法添加文件 {file_path}: {str(e)}", "WARN")
        
        return file_count

    def _calculate_hash(self, hash_type: str) -> str:
        """计算文件哈希值"""
        if hash_type == "md5":
            hasher = hashlib.md5()
        elif hash_type == "sha256":
            hasher = hashlib.sha256()
        else:
            raise ValueError(f"未知的哈希类型: {hash_type}")
        
        # 分块读取文件以节省内存
        with open(self.zip_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        
        return hasher.hexdigest()

    def _save_checksums(self, md5_hash: str, sha256_hash: str) -> None:
        """保存校验和文件"""
        # MD5文件
        with open(self.md5_file, 'w') as f:
            f.write(f"{md5_hash}  {self.zip_path.name}\n")
        
        # SHA256文件
        with open(self.sha256_file, 'w') as f:
            f.write(f"{sha256_hash}  {self.zip_path.name}\n")
        
        self.log(f"✓ 校验和文件已保存", "SUCCESS")

    def _save_logs(self) -> None:
        """保存日志文件"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(self.logs))
            self.log(f"✓ 日志文件: {self.log_file}", "SUCCESS")
        except Exception as e:
            self.log(f"保存日志失败: {str(e)}", "ERROR")

    def _print_summary(self, file_count: int, size_mb: float, md5_hash: str) -> None:
        """打印总结"""
        self.log("", "INFO")
        self.log("="*70, "INFO")
        self.log("✅ 打包完成！", "SUCCESS")
        self.log("="*70, "INFO")
        self.log("", "INFO")
        self.log("📊 打包统计:", "INFO")
        self.log(f"  📁 文件总数: {file_count}", "INFO")
        self.log(f"  💾 包大小: {size_mb:.2f} MB", "INFO")
        self.log(f"  🔐 MD5校验和: {md5_hash}", "INFO")
        self.log("", "INFO")
        self.log("📦 输出文件:", "INFO")
        self.log(f"  • {self.zip_path.name}", "INFO")
        self.log(f"  • {self.md5_file.name}", "INFO")
        self.log(f"  • {self.sha256_file.name}", "INFO")
        self.log(f"  • {self.log_file.name}", "INFO")
        self.log("", "INFO")
        self.log(f"📂 输出目录: {self.output_dir}", "INFO")
        self.log("", "INFO")
        self.log("🚀 下一步:", "INFO")
        self.log("  1. 验证校验和: md5sum -c *.md5", "INFO")
        self.log("  2. 上传到服务器或分享", "INFO")
        self.log("  3. 解压使用: unzip *.zip", "INFO")
        self.log("", "INFO")
        self.log("="*70, "INFO")


def main():
    """主函数"""
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("""
    ╔═════════════════════════════════════════════════════╗
    ║  Automated Test Framework - Package Creator       ║
    ║             Version 1.0.0                          ║
    ╚═════════════════════════════════════════════════════╝
    """)
    print(Colors.ENDC)

    # 获取输出目录
    output_dir = "."
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]

    # 创建打包器
    creator = PackageCreator(project_root=".", output_dir=output_dir)
    
    # 创建包
    success = creator.create_package()
    
    # 返回状态码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
