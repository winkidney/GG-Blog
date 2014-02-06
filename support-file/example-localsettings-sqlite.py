# coding:utf-8
# localsettings to protect my info
# in folder pycms
import os
db_root = os.path.join(os.path.dirname(__file__), '').replace('\\', '/')
####
SECRET_KEY = '_c@$un4*ihb4(&hf&556485qi@)yc-x=rw17h05jhe!h#fg^3r'
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'
        'NAME': db_root+'pycms.db',
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}
######多说########
DUOSHUO_SECRET = '578c296aae128ca54179e847cda351f4'
DUOSHUO_SHORT_NAME = 'ggblog'

#########################used by createdb.py##############################
# db create settings
dbname = 'pycms'
root_username = 'root'
root_passwd = '19921226'
new_username = 'pycms'
passwd_to_set = '19921226'
# super user info
su_name = 'winkidney'
su_email = "winkidney@gmail.com"
su_passwd = "19921226"
##########################ebd of createdb.py used#########################
