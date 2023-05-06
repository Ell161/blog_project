from django.forms import ModelForm, TextInput, Textarea
from .models import BlogPost


class BlogPostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название страницы'})
        self.fields['text'].widget = Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Содержание'})

    class Meta:
        model = BlogPost
        fields = ('title', 'text',)

