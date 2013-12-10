# coding:utf-8
# seetings of pycms
# Django settings for pycms project.
import os

# Make this unique, and don't share it with anybody.
try:
    from localsettings import SECRET_KEY
except:
    SECRET_KEY = ''


################全局静态设置by kidney######################
# 多说评论设置
#DUOSHUO_SECRET = '你的多说secret'
#DUOSHUO_SHORT_NAME = '你的多说short name'
##########nginx#########
#FORCE_SCRIPT_NAME = "/"
###########nginx end#######



# 全局静态文件路径设置（应当跟STATIC_ROOT等价）,值为绝对路径
# 统一了路径和url风格为"/****"，前面有'/'后面不带'/'，和django默认url风格相反
MY_STATIC_ROOT = os.path.join(
    os.path.dirname(__file__),
    'static').replace('\\',
                      '/')
MY_MEDIA_ROOT = os.path.join(
    os.path.dirname(__file__),
    'static/upload').replace('\\',
                             '/')
MY_MEDIA_URL = '/static/upload'
# blog_seetings（blog所用到的固定设置，安装相关）
BLOG_ROOT_URL = ''
GLOBA_STATIC_URL = '/static'
BLOG_STATIC_URL = GLOBA_STATIC_URL
BLOG_AMDMIN_STATIC_URL = BLOG_STATIC_URL + '/share/myadmin'
BLOG_LOGIN_URL = BLOG_ROOT_URL + '/login'
BLOG_LOGOUT_URL = BLOG_ROOT_URL + '/logout'
BLOG_ARTICLES_URL = BLOG_ROOT_URL + '/articles'
ARCHIVES_PER_PAGE = 10
BLOG_PAGE_URL = BLOG_ROOT_URL + '/page'
BLOG_THREADTYPE_URL = BLOG_ROOT_URL + '/threadtype'
BLOG_MANAGE_URL = BLOG_ROOT_URL + '/admin'
BLOG_ARCHIVES_URL = BLOG_ROOT_URL + '/archives'
BLOG_EDIT_URL = BLOG_MANAGE_URL + '/blog/posts'
BLOG_TAGS_URL = BLOG_ROOT_URL + '/tags'
BLOG_COMMENT_URL = BLOG_ROOT_URL + '/makecomment'
ADMIN_NEW_POST = BLOG_MANAGE_URL + '/blog/posts/add'
# 模板相关
TEMPLATE_ROOT_URL = BLOG_STATIC_URL + '/blog/front-template'
CUR_TEMPLATE_NAME = 'default'
CUR_TEMPLATE_DIR = os.path.join(
    os.path.dirname(__file__),
    'templates').replace('\\',
                         '/') + '/' + CUR_TEMPLATE_NAME
CUR_TEMPLATE_URL = TEMPLATE_ROOT_URL + '/' + CUR_TEMPLATE_NAME

# 模板路径，都是相对于CUR_TEMPLATE_DIR的值
LOGIN_TEMPLATE = 'blog/login/login_django.html'
JUMP_TEMPLATE = 'blog/login/auto_jump.html'
REMIND_TEMPLATE = 'blog/login/remind.html'
#侧边栏快捷功能菜单
SHORTCUT_MENU = [['后台管理',BLOG_MANAGE_URL],
                 ['发表新文章',ADMIN_NEW_POST],
                 ['退出GG-BLOG',BLOG_LOGOUT_URL],
                 ]
#快捷功能菜单结束

# 上传文件相关
FILE_UPLOAD_ALLOW = (
    'jpg',
    'jpeg',
    'bmp',
    'gif',
    'png',
    "rar",
    "doc",
    "docx",
    "zip",
    "pdf",
    "txt",
    "swf",
    "wmv")
IMG_FILE_EXT = ('jpg', 'jpeg', 'bmp', 'gif', 'png')
# 多说
try:
    from pycms.localsettings import DUOSHUO_SECRET, DUOSHUO_SHORT_NAME
except:
    DUOSHUO_SECRET = ''
    DUOSHUO_SHORT_NAME = ''
###################全局静态设置完毕##########################


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
try:
    from localsettings import DEBUG, ALLOWED_HOSTS
except:
    DEBUG = True
    ALLOWED_HOSTS = []
###################
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('winkidney', 'winkidney@gmail.com'),
)

MANAGERS = ADMINS

try:
    from localsettings import DATABASES
except:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            # Set to empty string for localhost. Not used with sqlite3.
            'HOST': '',
            # Set to empty string for default. Not used with sqlite3.
            'PORT': '3306',
        }
    }


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#MEDIA_ROOT = '/home/www/static/upload/'
MEDIA_ROOT = MY_STATIC_ROOT + '/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/static/upload/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = '/home/www/static/'
STATIC_ROOT = '/home/wwwroot/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = GLOBA_STATIC_URL + '/'

# Additional locations of static files
STATICFILES_DIRS = (
    MY_STATIC_ROOT + '/',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request"
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',

    #     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'blog.middleware.data_md',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pycms.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pycms.wsgi.application'

TEMPLATE_DIRS = (
    CUR_TEMPLATE_DIR,
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    # my own
    'blog',
    # 多说评论组件
    'duoshuo',
    # the 富文本编辑器
    #'tinymce',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            # my logger settings
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/home/wwwlogs/all.log',  # 或者直接写路径
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
                #'formatter':'standard',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                #'formatter': 'standard'
            },
            # my logger ending
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'default'],
                'level': 'DEBUG',
                'propagate': False
            },
            'django.request': {
                'handlers': ['mail_admins', 'default'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }
else:
    pass
