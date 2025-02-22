from django import forms
from .models import Advertisement, Response
from ckeditor.widgets import CKEditorWidget

class AdvertisementForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text'] 