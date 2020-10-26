from .base import *
import pymysql

pymysql.install_as_MySQLdb()

SHELL_PLUS = "ipython"

# ------------------------------------
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'  # Broker配置，使用Redis作为消息中间件
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # BACKEND配置，这里使用redis
CELERY_RESULT_SERIALIZER = 'json'  # 结果序列化方案
# ------------------------------------

DEBUG = True

INSTALLED_APPS += ['user_sys',
                   'demo',
                   'rest_framework',
                   'django_celery_beat',
                   'django_celery_results',
                   'guardian',
                   'drf_yasg',
                   'django_extensions']
# AttributeError: Manager isn't available; 'auth.User' has been swapped for 'app1.Test_user_model'


AUTH_USER_MODEL = "user_sys.CustomizeUser"  # "app1.Test_user_model"

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': "user_sys.utility.exception_handler"
}

MIDDLEWARE += []

#In [1]: from django.core.management import utils
#In [2]: utils.get_random_secret_key()
#SECRET_KEY =

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'edit_log_2020_10_26_14_11_13',
        'USER': 'root',
        'PASSWORD': '123123',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

MEDIA_ROOT = os.path.join(BASE_DIR,'upload_files')
MEDIA_URL = '/media/'
TARGET_FILE_DIRECTORY = os.path.abspath(os.path.join(BASE_DIR, "../tmpfiles"))

#日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 保留默认的logger
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'  # 省略个asctime
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 配置处理器和参数
        'console': {  # (((打印处理器)))
            # 实际开发建议使用WARNING
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # (((使用filter))) 下面则没使用
            'class': 'logging.StreamHandler',
            'formatter': 'simple'  # 格式选择前面定义的simple版本
        },
        'file': {  # (((文件处理器)))          #elk也就抓这里的数据.
            # 实际开发建议使用WARNING
            'level': 'WARNING',  # 配置日志级别
            'class': 'logging.handlers.RotatingFileHandler',  # 配置处理器
            # 日志位置,日志文件名,日志保存目录必须手动创建，注：这里的文件路径要注意BASE_DIR代表的是小luffyapi
            'filename': os.path.join(BASE_DIR, "logs", "a_django_demo.log"),  # 当前目录/logs目录/pipi.log
            # 日志文件的最大值,这里我们设置300M    #配置文件大小
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10  #配置文件数量
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',  # 配置输出格式
            # 文件内容编码
            'encoding': 'utf-8'  # 配置输出编码
        },
    },
    # 日志对象
    'loggers': {  # (((配置整个日志对象)))
        'django': {  # (((给logger命名用以区分, 可以配置多个logger)))
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}
