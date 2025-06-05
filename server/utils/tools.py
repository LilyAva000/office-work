import os
import datetime
from loguru import logger


def _init_logger():
    log_dir = "static/logs/query_process_logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    log_file = os.path.join(log_dir, f"query_{timestamp}.log")
    logger.add(
        log_file,
        rotation="50 MB",
        format="{time} | {level} | {message}",
        enqueue=True,   # 异步日志
        backtrace=True,  # 捕获异常
        diagnose=True,  # 并输出堆栈信息
        retention="7 days",  # 日志保留7天
    )
    logger.info(f"日志初始化完成，日志文件路径：{log_file}")
