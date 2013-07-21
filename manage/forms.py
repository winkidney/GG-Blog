#coding:utf-8
from django import forms

class MakePostForm(forms.Form):
    title = forms.CharField()
    short_title = form.CharField(required=False)
    cover_url = form.CharField(required=False)
    