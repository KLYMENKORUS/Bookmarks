from django import forms
from .models import Image, Comment
from betterforms.multiform import MultiModelForm


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'image')


class CommentImageForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)







