from django.shortcuts import render
from django.http import Http404
from forum.models import Post
from forum.models import Comment

from django.utils import timezone
from django.shortcuts import redirect

from .forms import PostForm


def post_new(request):
   if request.method == "POST":
      form = PostForm(request.POST)
      if form.is_valid():
         post = form.save(commit=False)
         post.author = request.user
         post.date = timezone.now()
         post.save()
         return redirect('post_detail', id=post.id)
   else:
      form = PostForm()
   
   return render(request,'forum/post_edit.html', {'form':form})

def index(request):
   posts = Post.objects.all()
   return render(request,'forum/index.html',{
       'posts' : posts,
   })
   
def post_detail(request,id):
   try:
      post = Post.objects.get(id=id)
      comments = Comment.objects.filter(post__id=id)
   except Post.DoesNotExist:
      raise Http404('This post does not exist')
   return render(request,'forum/post_detail.html',{
      'post' : post,
      'comments' : comments
   })
   

