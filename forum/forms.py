from django import forms
from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title','text',)
<<<<<<< HEAD

=======
        
>>>>>>> ccae6210697fbedb3e5b15e3364a08ee0500fd10

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('title','text',)