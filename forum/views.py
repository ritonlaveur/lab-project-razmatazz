from django.shortcuts import render
from forum.models import Post

def index(request):
   posts = Post.objects
   return render(request,'inventory/index.html',{
       'posts' : posts,
   })

