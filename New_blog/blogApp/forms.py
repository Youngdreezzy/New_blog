from django import forms
from .models import Blog
from .models import Comment


class BlogForm(forms.ModelForm):
    blog_title = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Blog
        fields = ['blog_title', 'content', 'image']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control mb-2'}),
            'author': forms.Select(attrs={'class': 'form-control mb-2'}),  
            'image': forms.ClearableFileInput(attrs={'class': 'form-control mb-2'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']