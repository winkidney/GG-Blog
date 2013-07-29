#coding:utf-8
from django import forms

class ReplyForm(forms.Form):
    comment_author = forms.CharField(max_length=20,required=True)
    comment_author_email = forms.EmailField(required=True)
    comment_author_url = forms.CharField(required=False)
    #有大问题= =
    #comment_content = forms.TextInput()