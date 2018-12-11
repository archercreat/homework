from django.forms import ModelForm, HiddenInput
from blog.models import Comment, Post

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['reply_to', 'post', 'text']
		widgets = {
			'post': HiddenInput()
		}

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
