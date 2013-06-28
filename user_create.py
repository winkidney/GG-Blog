#coding:utf-8
username = 'username'
email = "winkidney@hotmail.com"
password = "passwd"
from django.contrib.auth.models import User
user = User.objects.create_superuser(username, email, password)
#user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
user.save()