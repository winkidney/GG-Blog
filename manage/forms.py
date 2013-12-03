# coding:utf-8
from django import forms
from blog.models import Tags, ThreadTypes


class MakePostForm(forms.Form):

    """all varialbes in this form return unicode object"""
    title = forms.CharField(max_length=50, required=True)
    short_title = forms.CharField(max_length=50, required=False)
    cover_url = forms.URLField(max_length=200, required=False)
    upload = forms.FileField(required=False)
    introduction = forms.CharField(max_length=500, required=False)
    content = forms.CharField(required=True)
    commentnotshow = forms.BooleanField(required=False)
    tags = forms.MultipleChoiceField(required=False)
    threadtypeid = forms.ChoiceField(widget=forms.Select, required=True)

    def __init__(self, *args, **kwargs):
        super(MakePostForm, self).__init__(*args, **kwargs)
        thtid_choices = []  # 分类
        for threadtype in ThreadTypes.objects.all():
            if threadtype.name == u'未分类' or threadtype.parent_id != 0:
                thtid_choices.append((unicode(threadtype.id), threadtype.name))
        self.fields['threadtypeid'].choices = thtid_choices
        tags_choices = []
        for tag in Tags.objects.all():
            tags_choices.append((unicode(tag.id), tag.tagname))
        self.fields['tags'].choices = tags_choices


class ModifyPostForm(MakePostForm):
    id = forms.IntegerField(widget=forms.HiddenInput, required=True)
