#coding:utf-8
from django import forms

class ReplyForm(forms.Form):
    comment_author = forms.CharField(max_length=20,required=True)
    comment_author_email = forms.EmailField(required=True)
    comment_author_url = forms.CharField(required=False)
    comment_content = forms.CharField(required=True,widget=forms.Textarea)

class ReplyFormLogined(forms.Form):
    comment_content = forms.CharField(required=True,widget=forms.Textarea)