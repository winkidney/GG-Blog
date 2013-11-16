#coding:utf-8
from django import forms

class ReplyForm(forms.Form):
    fnext = forms.CharField(required=True)
    fusername =forms.CharField(max_length=20,required=True)
    femail = forms.EmailField(required=True)
    fwebsite = forms.CharField(required=False)
    fmessage = forms.CharField(required=True,widget=forms.Textarea)

class ReplyFormLogined(forms.Form):
    comment_content = forms.CharField(required=True,widget=forms.Textarea)