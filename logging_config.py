import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """配置日志系统"""
    # 创建logs目录
    os.makedirs('logs', exist_ok=True)
    
    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # 控制台处理器 - 只显示INFO及以上级别
            logging.StreamHandler()
        ]
    )
    
    # 创建Flask应用日志记录器
    app_logger = logging.getLogger('KittenTTS')
    app_logger.setLevel(logging.INFO)
    
    # 应用日志文件处理器（带轮转）
    app_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    app_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app_logger.addHandler(app_handler)
    
    # 创建访问日志记录器
    access_logger = logging.getLogger('access')
    access_logger.setLevel(logging.INFO)
    
    # 访问日志文件处理器（带轮转）
    access_handler = RotatingFileHandler(
        'logs/access.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    access_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    access_logger.addHandler(access_handler)
    
    # 创建错误日志记录器
    error_logger = logging.getLogger('error')
    error_logger.setLevel(logging.ERROR)
    
    # 错误日志文件处理器（带轮转）
    error_handler = RotatingFileHandler(
        'logs/error.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    error_logger.addHandler(error_handler)
    
    return app_logger, access_logger, error_logger

def log_startup_info(app_logger):
    """记录启动信息"""
    app_logger.info("=" * 60)
    app_logger.info("🚀 KittenTTS Web应用启动")
    app_logger.info("=" * 60)
    app_logger.info("📝 日志文件位置:")
    app_logger.info("  - 应用日志: logs/app.log")
    app_logger.info("  - 访问日志: logs/access.log")
    app_logger.info("  - 错误日志: logs/error.log")
    app_logger.info("📊 日志轮转: 每个文件最大10MB，保留5个备份")
    app_logger.info("=" * 60)

def log_shutdown_info(app_logger):
    """记录关闭信息"""
    app_logger.info("=" * 60)
    app_logger.info("🛑 KittenTTS Web应用关闭")
    app_logger.info("=" * 60)
