from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget



class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'description', 'photo', 'category']
    description = forms.CharField(widget=CKEditorWidget(attrs={
        'placeholder': 'Use <strong> tag for text bold , </br> for next line,'
    }))
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email','comment_text']  # Field from Comment model
        
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
