import logging

# 日志配置
CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(levelname)s][%(pathname)s %(lineno)s]=>%(message)s'  # 日志格式
        },
        'simple': {
            'format': '[%(asctime)s][%(levelname)s]=>%(message)s'  # 日志格式
        },
    },
    'filters': {
        # 过滤器,根据需求配置
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',  #
            'filename': 'cyeap.log',
            'formatter': 'simple',
            'encoding': 'utf8',
            'when': 'midnight',  # 半夜0点的时候分割日志
            'interval': 1,
            'backupCount': 30,  # 最大备份30个日志文件
        },
        'email': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'email'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

logger = logging.getLogger("django")
logger.error("aaa")

