import os
import yaml
from typing import Any, Optional, List

class Config:
    CONFIG_FILE = "/etc/.mycmd.conf"

    def __init__(self):
        self._config = self._load_config()

    def _load_config(self) -> dict:
        """加载配置文件"""
        if not os.path.exists(self.CONFIG_FILE):
            raise FileNotFoundError(f"配置文件不存在: {self.CONFIG_FILE}")
        
        with open(self.CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f)

    def get(self, module: str, key: str) -> Optional[Any]:
        """获取指定模块的配置项"""
        try:
            value = self._config.get(module, {}).get(key)
            if value is None:
                raise KeyError(f"未找到配置项 {module}.{key}")
            
            # 展开波浪号为用户主目录
            if isinstance(value, str) and value.startswith('~'):
                value = os.path.expanduser(value)
                
            return value
        except Exception as e:
            raise KeyError(f"读取配置项 {module}.{key} 失败: {str(e)}")

    def validate(self, module: str, required_keys: List[str]):
        """验证指定模块的必需配置项"""
        for key in required_keys:
            self.get(module, key)

# 创建全局配置实例
config = Config() 