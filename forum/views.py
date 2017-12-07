from django.shortcuts import render
from django.http import Http404
from forum.models import Post
from forum.models import Comment

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
