# coding:utf-8
# localsettings to protect my info
# in folder pycms
####
SECRET_KEY = '_c@$un4*ihb4(&hf&556485qi@)yc-x=rw17h05jhe!h#fg^3r'
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pycms',
        'USER': 'pycms',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '3306',
    }
}
######多说########
DUOSHUO_SECRET = 'your duoshuo secret'
DUOSHUO_SHORT_NAME = 'your short name'

#########################used by createdb.py##############################
# db create settings
dbname = 'pycms'
root_username = 'root'
root_passwd = 'your toor pwd'
new_username = 'you new db user name'
passwd_to_set = 'your new db user pwd'
# super user info
su_name = 'blog super user name'
su_email = "email"
su_passwd = "blog super user name"
##########################ebd of createdb.py used#########################
