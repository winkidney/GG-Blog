#coding:utf-8
from django import forms

class ReplyForm(forms.Form):
    r_username =forms.CharField(max_length=20,required=True)
    r_email = forms.EmailField(required=True)
    r_website = forms.CharField(required=False)
    r_message = forms.CharField(required=True,widget=forms.Textarea)

class ReplyFormLogined(forms.Form):
    comment_content = forms.CharField(required=True,widget=forms.Textarea)