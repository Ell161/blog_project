from django.forms import ModelForm, TextInput, Textarea, CheckboxInput, FileInput
from .models import BlogPost


class BlogPostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['page_picture'].widget = FileInput()
        self.fields['is_published'].widget = CheckboxInput(attrs={
            'type': 'checkbox',
            'label': 'Опубликовать'})
        self.fields['title'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название страницы'})
        self.fields['text'].widget = Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Содержание'})

    class Meta:
        model = BlogPost
        fields = ('page_picture', 'is_published', 'title', 'text',)

