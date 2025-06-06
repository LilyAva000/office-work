import yaml
from pathlib import Path

# 只加载一次错误码配置
ERRORS = yaml.safe_load(Path("config/error_config.yaml").read_text(encoding="utf-8"))

def get_error(key: str) -> str:
    err = ERRORS.get(key)
    if not err:
        return f"Unknown error key: {key}"
    return err["code"],err["message"]

