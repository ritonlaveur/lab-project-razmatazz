from django.shortcuts import render
from django.http import Http404
from forum.models import Post
from forum.models import Comment

from django.utils import timezone
from django.shortcuts import redirect

from .forms import PostForm
from .forms import CommentForm

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
   
def comment_new(request,id):
   if request.method == "POST":
      form = CommentForm(request.POST)
      if form.is_valid():
         comment = form.save(commit=False)
         comment.post = Post.objects.get(id=id)
         comment.author = request.user
         comment.date = timezone.now()
         comment.save()
         return  redirect('post_detail',id=id)
   else:
      form = CommentForm()
   
   post = Post.objects.get(id=id)
   return render(request,'forum/comment_edit.html',{'form':form,'post':post})


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
   
def post_delete(request,id):
   
   post = Post.objects.get(id=id)
   post.delete()

   return redirect('index')

