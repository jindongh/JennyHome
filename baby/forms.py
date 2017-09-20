from django import forms
from .models import Photo, Gallery

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('name', 'description', 'is_public',)

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('description', 'image',)
